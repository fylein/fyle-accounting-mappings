from typing import List, Any

from .constants import REIMBURSABLE_IMPORT_STATE, CCC_IMPORT_STATE
from .models import ExpenseGroupSettingsAdapter


def get_expense_import_states(expense_group_settings: Any, integration_type: str = 'default') -> List[str]:
    """
    Get expense import state
    :param expense_group_settings: expense group settings model instance
    :param integration_type: Type of integration (e.g. 'default', 'xero')
    :return: expense import state
    """
    expense_group_settings = ExpenseGroupSettingsAdapter(expense_group_settings, integration_type)
    expense_import_state = set()

    if expense_group_settings.ccc_expense_state == 'APPROVED':
        expense_import_state = {'APPROVED', 'PAYMENT_PROCESSING', 'PAID'}

    if expense_group_settings.expense_state == 'PAYMENT_PROCESSING':
        expense_import_state.add('PAYMENT_PROCESSING')
        expense_import_state.add('PAID')

    if expense_group_settings.expense_state == 'PAID' or expense_group_settings.ccc_expense_state == 'PAID':
        expense_import_state.add('PAID')

    return list(expense_import_state)


def filter_expenses_based_on_state(expenses: List[Any], expense_group_settings: Any, integration_type: str = 'default'):
    """
    Filter expenses based on the expense state
    :param expenses: list of expenses
    :param expense_group_settings: expense group settings model instance
    :param integration_type: Type of integration (e.g. 'default', 'xero')
    :return: list of filtered expenses
    """
    expense_group_settings = ExpenseGroupSettingsAdapter(expense_group_settings, integration_type)

    allowed_reimbursable_import_state = REIMBURSABLE_IMPORT_STATE.get(expense_group_settings.expense_state)
    reimbursable_expenses = list(filter(lambda expense: expense['fund_source'] == 'PERSONAL' and expense['state'] in allowed_reimbursable_import_state, expenses))

    allowed_ccc_import_state = CCC_IMPORT_STATE.get(expense_group_settings.ccc_expense_state)
    ccc_expenses = list(filter(lambda expense: expense['fund_source'] == 'CCC' and expense['state'] in allowed_ccc_import_state, expenses))

    return reimbursable_expenses + ccc_expenses
