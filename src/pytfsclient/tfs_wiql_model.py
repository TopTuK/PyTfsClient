from typing import List
from .tfs_workitem_model import TfsWorkitem
from .models.workitems.tfs_wiql_result import WiqlResult

class TfsWiqlResult:
    """
    Result of WIQL query to TFS
    """

    @property
    def is_empty(self) -> bool:
        """
        Return True if WIQL query has no any result
        """
        
        return self.__wiql_result.is_empty

    @property
    def item_ids(self) -> List[int]:
        """
        List of ids of WIQL query result
        """

        return self.__wiql_result.item_ids
    
    @property
    def workitems(self) -> List[TfsWorkitem]:
        """
        Return list of TFS workitems. Calls TfsWorkitemClient::get_workitems() function
        """
        items = self.__wiql_result.workitems
        
        return [TfsWorkitem.from_workitem(item) for item in items]
    
    @classmethod
    def from_wiql_result(cls, wiql_result: WiqlResult):
        wiql = cls()

        wiql.__wiql_result: WiqlResult = wiql_result

        return wiql