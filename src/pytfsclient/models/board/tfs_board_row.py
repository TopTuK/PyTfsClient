from ..client_error import ClientError

class BoardRow:
    '''
    Board Row class
    '''

    @property
    def id(self) -> str:
        '''
        '''
        return self.__id
    
    @property
    def name(self) -> str:
        '''
        '''
        return self.__name
    
    @property
    def color(self) -> str:
        '''
        '''
        return self.__color
    
    @classmethod
    def from_json(cls, json_item):
        '''
        '''

        row = cls()

        try:
            row.__id = json_item['id']
            row.__name = json_item['name']
            row.__color = json_item['color']

            return row
        except Exception as ex:
            raise ClientError(ex)