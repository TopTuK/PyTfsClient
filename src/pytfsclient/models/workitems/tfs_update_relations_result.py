from enum import Enum

class UpdateRelationsResult(Enum):
    '''
    ENUM: update workitem relations result.

    Enum values:
    - UPDATE_EXCEPTION: exception raised
    - UPDATE_FAIL: Failed to update relations
    - UPDATE_SUCCESS: Relations successfully updated
    '''

    UPDATE_EXCEPTION = 1
    UPDATE_FAIL = 2
    
    UPDATE_SUCCESS = 0