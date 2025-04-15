class ExpenseImportSourceEnum:
    """
    Enum for Expense Import Source
    """
    WEBHOOK = 'WEBHOOK'
    DASHBOARD_SYNC = 'DASHBOARD_SYNC'
    DIRECT_EXPORT = 'DIRECT_EXPORT'
    BACKGROUND_SCHEDULE = 'BACKGROUND_SCHEDULE'
    INTERNAL = 'INTERNAL'


class ExpenseStateEnum:
    """
    Enum for Expense State
    """
    PAYMENT_PROCESSING = 'PAYMENT_PROCESSING'
    PAID = 'PAID'
    APPROVED = 'APPROVED'


class RoutingKeyEnum:
    """
    Enum for Routing Key
    """
    EXPORT = 'exports.p1'
    UPLOAD_S3 = 'upload.s3'


class SourceAccountTypeEnum:
    """
    Enum for Source Account Type
    """
    PERSONAL_CASH_ACCOUNT = 'PERSONAL_CASH_ACCOUNT'
    PERSONAL_CORPORATE_CREDIT_CARD_ACCOUNT = 'PERSONAL_CORPORATE_CREDIT_CARD_ACCOUNT'
