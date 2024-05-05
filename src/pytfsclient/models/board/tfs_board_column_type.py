from enum import Enum

class BoardColumnType(Enum):
    '''
    ENUM: Board column type.

    Enum values:
    - UNKNOWN
    - INCOMING
    - ACTIVE
    - OUTGOING
    '''

    UNKNOWN = 0
    INCOMING = 1
    ACTIVE = 2
    OUTGOING = 3


BOARD_COLUMN_TYPE_MAP = {
    'incoming': BoardColumnType.INCOMING,
    'inProgress': BoardColumnType.ACTIVE,
    'outgoing': BoardColumnType.OUTGOING
}