from typing import List
from .tfs_board_column_type import BoardColumnType, BOARD_COLUMN_TYPE_MAP
from .tfs_board_column_state import BoardColumnState
from ..client_error import ClientError

class BoardColumn:
    '''
    Board Column class
    '''

    @property
    def id(self) -> str:
        '''
        Returns:
            ID of board column
        '''
        return self.__id
    
    @property
    def name(self) -> str:
        '''
        Returns:
            Name of board column
        '''
        return self.__name
    
    @property
    def wip_limit(self) -> int:
        '''
        Returns:
            WIP limit of board column
        '''
        return self.__wip_limit
    
    @property
    def column_type(self) -> BoardColumnType:
        '''
        Returns:
            Board column type (BoardColumnType)
        '''
        return self.__column_type
    
    @property
    def column_state_map(self) -> List[BoardColumnState]:
        '''
        Returns:
            States of workitems (BoardColumnState) for board column
        '''
        return self.__column_state_map
    
    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates instance of board column

        Args:
            json_item (object): JSON object of board column

        Returns:
            Instance of BoardColumn class
        '''

        column = cls()

        try:
            column.__id = json_item['id']
            column.__name = json_item['name']
            column.__wip_limit = json_item['itemLimit']

            column.__column_type = BOARD_COLUMN_TYPE_MAP.get(json_item['columnType'], BoardColumnType.UNKNOWN)
            
            if 'stateMappings' in json_item:
                column.__column_state_map = [BoardColumnState.from_dict_entry(key, value) for key, value in json_item['stateMappings'].items()]
            else:
                column.__column_state_map = []

            return column
        except Exception as ex:
            raise ClientError(ex)