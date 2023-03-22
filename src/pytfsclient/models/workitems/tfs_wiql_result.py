from typing import List

from pytfsclient.models.workitems.tfs_workitem import Workitem

class WiqlResult:
    """
    Result of WIQL query to TFS
    """

    @property
    def is_empty(self) -> bool:
        """
        Return True if WIQL query has no any result
        """
        return not (len(self.item_ids) > 0)
    
    @property
    def item_ids(self) -> List[int]:
        """
        List of ids of WIQL query result
        """
        return self.__ids
    
    @property
    def workitems(self) -> List[Workitem]:
        """
        Return list of TFS workitems.
        """
        return self.__client.get_workitems(self.item_ids)
    
    @classmethod
    def from_json(cls, tfs_client, json_response):
        """
        Creates TfsWiqlResult from given json object

        :param: tfs_client (TfsWorkitem): TfsWorkitemClient object. Can't be None.
        :param: json_response: json response from TFS Server. It should have list of workItems with id attribute
        :return: TfsWiqlResult instance
        """

        wiql = cls()

        wiql.__client = tfs_client

        if 'workItems' in json_response:
            wiql.__ids = [int(item['id']) for item in json_response['workItems']]
        else:
            wiql.__ids = []

        return wiql
    