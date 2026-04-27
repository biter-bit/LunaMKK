from enum import Enum

class StatusTask(str, Enum):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'



class Exchange(str, Enum):
    PAYMENT_EVENTS = 'payment.events'

class RoutingKey(str, Enum):
    PAYMENT_CREATED = 'payment.create'