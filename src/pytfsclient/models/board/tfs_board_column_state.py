from ..client_error import ClientError

class BoardColumnState:
    '''
    Class containce information of states for workitem for board
    '''

    @property
    def item_type(self) -> str:
        '''
        Returns:
            Woritem type (str) for board column
        '''
        return self.__item_type

    @property
    def item_state(self) -> str:
        '''
        Returns:
            Woritem state (str) for board column
        '''
        return self.__item_state

    @classmethod
    def from_dict_entry(cls, key, value):
        '''
        Classmethod creates instance of BoardColumnState from entry of state mapping dictonary
        '''

        column_state = cls()

        try:
            column_state.__item_type = key
            column_state.__item_state = value

            return column_state
        except Exception as ex:
            raise ClientError(ex)
