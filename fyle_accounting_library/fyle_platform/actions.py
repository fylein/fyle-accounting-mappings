import logging
import importlib
from typing import Optional, List
from datetime import datetime, timedelta

from fyle.platform.exceptions import InternalServerError, InvalidTokenError
from fyle_integrations_platform_connector import PlatformConnector

from fyle_accounting_mappings.models import ExpenseAttribute
from fyle_integrations_imports.models import ImportLog
from fyle_accounting_library.common_resources.helpers import get_current_utc_datetime
from fyle_accounting_library.fyle_platform.enums import (
    DefaultFyleConditionsEnum,
    DefaultExpenseAttributeTypeEnum,
    ExpenseFilterCustomFieldTypeEnum,
    DefaultExpenseAttributeDetailEnum
)

workspace_models = importlib.import_module("apps.workspaces.models")
Workspace = workspace_models.Workspace
FyleCredential = workspace_models.FyleCredential

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def check_interval_and_sync_dimension(workspace_id: int, payload: dict) -> None:
    """
    Check Interval and Sync Dimension
    :param workspace_id: Workspace ID
    :param payload: Payload
    :return: None
    """
    workspace = Workspace.objects.get(pk=workspace_id)
    current_utc_datetime = get_current_utc_datetime()
    is_sync_required = (
        payload.get('refresh')
        or workspace.source_synced_at is None
        or (current_utc_datetime - workspace.source_synced_at).days > 0
    )

    if is_sync_required:
        logger.info(f"Syncing Fyle dimensions for workspace {workspace_id}")
        fyle_credentials = FyleCredential.objects.get(workspace_id=workspace_id)
        platform = PlatformConnector(fyle_credentials)
        platform.import_fyle_dimensions()
        workspace.source_synced_at = current_utc_datetime
        workspace.save(update_fields=['source_synced_at', 'updated_at'])
    else:
        logger.info(f"Skipping Fyle dimensions sync for workspace {workspace_id}")


def get_expense_fields(workspace_id: int) -> list[dict]:
    """
    Get Expense Fields
    :param workspace_id: Workspace ID
    :return: List of Expense Fields
    """
    fyle_credentails = FyleCredential.objects.get(workspace_id=workspace_id)
    platform = PlatformConnector(fyle_credentails)
    custom_fields = platform.expense_custom_fields.list_all()

    response = [condition.value for condition in DefaultFyleConditionsEnum]
    custom_field_type_list = [field.value for field in ExpenseFilterCustomFieldTypeEnum]

    for custom_field in custom_fields:
        if custom_field['type'] in custom_field_type_list:
            response.append({
                'field_name': custom_field['field_name'],
                'type': custom_field['type'],
                'is_custom': custom_field['is_custom']
            })

    return response


def get_expense_attribute_types(workspace_id: int) -> list[dict]:
    """
    Get Expense Attribute Fields
    :param workspace_id: Workspace ID
    :return: List of Expense Attribute Fields
    """
    attribute_type_list = [field.value for field in DefaultExpenseAttributeTypeEnum]
    attributes = (
        ExpenseAttribute.objects.filter(workspace_id=workspace_id)
        .exclude(attribute_type__in=attribute_type_list)
        .values('attribute_type', 'display_name')
        .distinct()
    )

    expense_attributes = [DefaultExpenseAttributeDetailEnum.PROJECT.value, DefaultExpenseAttributeDetailEnum.COST_CENTER.value]

    for attribute in attributes:
        expense_attributes.append(attribute)

    return expense_attributes


def get_employee_expense_attribute(value: str, workspace_id: int) -> Optional[ExpenseAttribute]:
    """
    Get employee expense attribute
    :param value: Employee email
    :param workspace_id: Workspace ID
    :return: ExpenseAttribute or None
    """
    return ExpenseAttribute.objects.filter(
        attribute_type='EMPLOYEE',
        value=value,
        workspace_id=workspace_id
    ).first()


def sync_inactive_employee(employee_email: str, workspace_id: int) -> Optional[ExpenseAttribute]:
    """
    Sync inactive employee from Fyle to expense attributes.
    Use when an expense references an inactive employee not yet present in ExpenseAttribute.
    :param employee_email: Employee email address
    :param workspace_id: Workspace ID
    :return: ExpenseAttribute if synced successfully, None otherwise
    """
    try:
        fyle_credentials = FyleCredential.objects.get(workspace_id=workspace_id)
        platform = PlatformConnector(fyle_credentials=fyle_credentials)

        fyle_employee = platform.employees.get_employee_by_email(employee_email)
        if len(fyle_employee):
            fyle_employee = fyle_employee[0]
            attribute = {
                'attribute_type': 'EMPLOYEE',
                'display_name': 'Employee',
                'value': fyle_employee['user']['email'],
                'source_id': fyle_employee['id'],
                'active': True if fyle_employee['is_enabled'] and fyle_employee['has_accepted_invite'] else False,
                'detail': {
                    'user_id': fyle_employee['user_id'],
                    'employee_code': fyle_employee['code'],
                    'full_name': fyle_employee['user']['full_name'],
                    'location': fyle_employee['location'],
                    'department': fyle_employee['department']['name'] if fyle_employee['department'] else None,
                    'department_id': fyle_employee['department_id'],
                    'department_code': fyle_employee['department']['code'] if fyle_employee['department'] else None
                }
            }
            ExpenseAttribute.bulk_create_or_update_expense_attributes([attribute], 'EMPLOYEE', workspace_id, True)
            return get_employee_expense_attribute(employee_email, workspace_id)
    except (InvalidTokenError, InternalServerError) as e:
        logger.info('Invalid Fyle refresh token or internal server error for workspace %s: %s', workspace_id, str(e))
        return None

    except Exception as e:
        logger.error('Error syncing inactive employee for workspace_id %s: %s', workspace_id, str(e))
        return None


def reset_stuck_imports(workspace_ids_list: List[int]):
    """
    Reset stuck imports for a list of workspaces
    """
    import_logs = ImportLog.objects.filter(workspace_id__in=workspace_ids_list, status='IN_PROGRESS', updated_at__lt=datetime.now() - timedelta(minutes=120))
    if import_logs.exists():
        logger.info('Stuck import logs found: %s', import_logs.count())
        import_logs.update(status='FAILED', updated_at=datetime.now())
