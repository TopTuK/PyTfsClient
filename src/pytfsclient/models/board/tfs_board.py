from typing import List
from ..client_error import ClientError
from .tfs_board_column import BoardColumn
from .tfs_board_row import BoardRow

class Board:
    '''
    Board model class contains infromation about project team board
    '''

    @property
    def id(self) -> str:
        '''
        Returns:
            ID of TFS/Azure Team
        '''
        return self.__id

    @property
    def name(self) -> str:
        '''
        Returns:
            Name of TFS/Azure Team
        '''
        return self.__name

    @property
    def url(self) -> str:
        '''
        Returns:
            URL of TFS/Azure Team
        '''
        return self.__url
    
    @property
    def revision(self) -> int:
        '''
        Returns:
            Revision of board
        '''
        return self.__revision
    
    @property
    def is_valid(self) -> bool:
        '''
        Returns:
            Validation of board
        '''
        return self.__is_valid
    
    @property
    def can_edit(self) -> bool:
        '''
        Returns:
            Possibility for modification of board
        '''
        return self.__can_edit
    
    @property
    def columns(self) -> List[BoardColumn]:
        '''
        Returns:
            Columns for board (List[BoardColumn])
        '''
        return self.__columns
    
    @property
    def rows(self) -> List[BoardRow]:
        '''
        Returns:
            Rows for board (List[BoardRow])
        '''
        return self.__rows
    
    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates instance of project team board from given json object

        Args:
            json_item (object): JSON object with attributes such as 'id', 'name', etc.

        Returns:
            Instance of Board class
        '''

        board = cls()

        try:
            board.__id = json_item['id']
            board.__name = json_item['name']
            board.__url = json_item['url']

            board.__revision = json_item['revision']
            board.__is_valid = json_item['isValid']
            board.__can_edit = json_item['canEdit']

            board.__columns = [BoardColumn.from_json(j_item) for j_item in json_item['columns']]
            board.__rows = [BoardRow.from_json(j_item) for j_item in json_item['rows']]

            return board
        except Exception as ex:
            raise ClientError(ex)