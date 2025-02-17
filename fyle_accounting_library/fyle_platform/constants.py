from .enums import ExpenseImportSourceEnum

REIMBURSABLE_IMPORT_STATE = {
    'PAYMENT_PROCESSING': ['PAYMENT_PROCESSING', 'PAID'],
    'PAID': ['PAID']
}

CCC_IMPORT_STATE = {
    'APPROVED': ['APPROVED', 'PAYMENT_PROCESSING', 'PAID'],
    'PAID': ['PAID']
}

IMPORTED_FROM_CHOICES =  (
    (ExpenseImportSourceEnum.WEBHOOK, 'WEBHOOK'),
    (ExpenseImportSourceEnum.DASHBOARD_SYNC, 'DASHBOARD_SYNC'),
    (ExpenseImportSourceEnum.DIRECT_EXPORT, 'DIRECT_EXPORT'),
    (ExpenseImportSourceEnum.BACKGROUND_SCHEDULE, 'BACKGROUND_SCHEDULE')
)
