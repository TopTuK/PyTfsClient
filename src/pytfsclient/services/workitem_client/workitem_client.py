from typing import List
from pytfsclient.models.workitems.tfs_wiql_result import WiqlResult
from pytfsclient.models.workitems.tfs_workitem import Workitem
from pytfsclient.models.workitems.tfs_workitem_relation import WorkitemRelation
from pytfsclient.services.base_client import BaseClient
from pytfsclient.services.client_connection import ClientConnection

class WorkitemClient(BaseClient):
    """
    TFS Workitem Client facade for managing workitems and relations
    """

    # Constructor
    def __init__(self, client_connection: ClientConnection) -> None:
        super().__init__(client_connection)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-6.0
    def get_workitems(self, item_ids, item_fields: List[str] = None, expand: str = 'All', batch_size: int = 50) -> List[Workitem]:
        """
        """
        pass

    def get_single_workitem(self, item_id, item_fields: List[str] = None) -> Workitem:
        """
        """
        pass

    # return dictonary with standart query params
    @staticmethod
    def _make_query_params(expand: str, bypass_rules: bool, suppress_notifications: bool, validate_only: bool) -> dict:
        """
        Return dictonary with standart query params
        """

        return {
            'api-version' : BaseClient.api_version,
            '$expand' : expand,
            'bypassRules' : str(bypass_rules),
            'suppressNotifications' : str(bypass_rules),
            'validateOnly' : str(validate_only)
        }
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-6.0
    def create_workitem(self, type_name: str, item_fields: List[dict] = None, item_relations: List[WorkitemRelation] = None, \
        expand: str = 'All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> Workitem:
        """
        """

        pass

    def copy_workitem(self, source_item, item_fields: List[str] = None, item_ignore_fileds: List[str] = None) -> Workitem:
        """
        """

        pass

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.0
    def update_workitem_fields(self, workitem, item_fields: List[dict], \
        expand: str='All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> Workitem:
        """
        """

        pass

    ### REGION MANAGING RELATIONS ###

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.0#add-a-link
    def add_relation(self, source_workitem, destination_workitem, relation_type_name: str, \
        relation_attributes = None, \
        expand: str = 'All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> Workitem:
        """
        """

        pass

    def remove_relation(self, workitem: Workitem, relation: WorkitemRelation, \
        expand='All', bypass_rules=False, \
        suppress_notifications=False, validate_only=False) -> Workitem:
        """
        """

        pass

    ### END REGION MANAGING RELATIONS ###

    ### REGION QUERIES (WIQL) ###

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/queries/get?view=azure-devops-rest-6.0
    def run_saved_query(self, query_id: str) -> WiqlResult:
        """
        """

        pass

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
    def run_wiql(self, query: str, max_top: int = -1) -> WiqlResult:
        """
        """

        pass

    ### END REGION QUERIES (WIQL) ###

