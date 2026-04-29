from enum import Enum

class StatusTask(str, Enum):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

class StatusPayment(str, Enum):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

class StatusEvent(str, Enum):
    """Название события бизнес-логики"""
    PAYMENT_EVENTS = 'payment.create'

class RoutingKey(str, Enum):
    """Ключ, по которому exchange решает, куда слать сообщение"""
    PAYMENT_CREATED = 'payment.create'