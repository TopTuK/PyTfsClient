from typing import List
from .tfs_workitem import Workitem
from ..client_error import ClientError

class WiqlResult:
    '''
    Result of WIQL query to TFS. Use WorkitemClient::run_saved_query() or WorkitemClient::run_wiql
    '''

    @property
    def is_empty(self) -> bool:
        '''
        Returns:
            True if WIQL query has no any result
        '''

        return not (len(self.item_ids) > 0)
    
    @property
    def item_ids(self) -> List[int]:
        '''
        Returns:
            List of ids of workitems of WIQL query result
        '''

        return self.__ids
    
    @property
    def workitems(self) -> List[Workitem]:
        '''
        Returns:
            List of workitems.
        '''

        return self.__client.get_workitems(self.item_ids) if not self.is_empty else []
    
    @classmethod
    def from_json(cls, tfs_client, json_response):
        '''
        Classmethod creates WiqlResult class instance from given json object.

        Args:
            tfs_client (WorkitemClient): WorkitemClient object. Can't be None.
            json_response (object): json response from TFS Server. It should have list of workItems with id attribute

        Returns:
            WiqlResult class instance

        Raises:
            ClientError if tfs_client is None or invalid json_response
        '''

        if not tfs_client:
            raise ClientError('tfs_client is None')

        wiql = cls()

        try:
            wiql.__client = tfs_client

            if 'workItems' in json_response:
                wiql.__ids = [int(item['id']) for item in json_response['workItems']]
            else:
                wiql.__ids = []
        except Exception as ex:
            raise ClientError(ex)

        return wiql
    