from collections import defaultdict
from typing import List
from .tfs_client import TfsBaseClient, TfsClientError
from .tfs_workitem_model import TfsWorkitem
from .tfs_wiql_model import TfsWiqlResult
from .tfs_workitem_relation_model import TfsWorkitemRelation

from .client_factory import ClientFactory
from .services.workitem_client.workitem_client import WorkitemClient
from .models.workitems.tfs_workitem_relation import WorkitemRelation

class TfsWorkitemClient:
    """
    TFS workitem client facade for managing workitems and relations
    Should be created with TfsClientFactory.
    """

    def __init__(self, client: TfsBaseClient) -> None:
        self.__client: TfsBaseClient = client
        self.__wi_client: WorkitemClient = ClientFactory.get_workitem_client(client.client_connection)
    
    @property
    def client(self) -> TfsBaseClient:
        """
        TfsBaseClient instance
        """
        return self.__client

    def get_workitems(self, item_ids, item_fields: List[str] = None, expand: str = 'All', batch_size: int = 50) -> List[TfsWorkitem]:
        """
        Return list of TfsWorkitems for given list of item ids.

        :param: item_ids: one id or list of item ids. Each id should be int or str.
        :param: item_fields: list of requested fields for TFS workitems. if None then all fields
        :param: expand (str): The expand parameters for work item attributes. Possible options are { None, Relations, Fields, Links, All }.
        :param: batch_size (int): number of requesting workitems for one iteration.
        :return: list of TfsWorkitems
        """
        assert item_ids, 'TfsWorkitemClient::get_workitems: item ids can\'t be None'

        items = self.__wi_client.get_workitems(item_ids, item_fields, expand, batch_size)
        return [TfsWorkitem.from_workitem(item) for item in items]
    
    def get_single_workitem(self, item_id, item_fields: List[str] = None) -> TfsWorkitem:
        """
        Get TFS workitem

        :param: item_id (str | int): id of requesting item. Can't be None.
        :param: item_fields: list of requested fields for TFS workitems. if None then all fields
        :return: TfsWorkitem instance
        """
        assert item_id, 'TfsWorkitemClient::get_single_workitem: item_id can\'t be None'

        return self.get_workitems(item_ids=item_id, item_fields=item_fields)[0]
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-6.0
    def create_workitem(self, type_name: str, item_fields: List[dict] = None, item_relations: List[TfsWorkitemRelation] = None, \
        expand: str = 'All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> TfsWorkitem:
        """
        Creates workitem of given type, properties and relations

        :param: type_name (str): The work item type of the work item to create. Look TfsWorkitemTypes map for built-in types.
        :param: item_fields: list of dictonary, where { key: field name, value: field value }. E.g. ['System.Title', 'Item title']
        :param: item_relations: list of TfsWorkitemRelation.
        :param: expand (str): The expand parameters for work item attributes. Possible options are { None, Relations, Fields, Links, All }.
        :param: bypass_rules (bool): Do not enforce the work item type rules on this update.
        :param: suppress_notifications (bool): Do not fire any notifications for this change
        :param: validate_only (bool): Indicate if you only want to validate the changes without saving the work item
        :return: TfsWorkitem instance
        """
        assert type_name, 'TfsWorkitemClient::create_workitem: item type name can\'t be None'

        fields = defaultdict(str)
        if item_fields:
            for fld_dict in item_fields:
                for k, v in fld_dict.items():
                    fields[k] = v

        relations = None
        if item_relations:
            relations = list()
            for rel in item_relations:
                wi = self.__wi_client.get_single_workitem(rel.destination_id)
                relations.append(WorkitemRelation.create(rel.relation_name, wi))

        item = self.__wi_client.create_workitem(type_name, fields, relations, expand, bypass_rules, suppress_notifications, validate_only)
        return TfsWorkitem.from_workitem(item)

    def copy_workitem(self, source_item, item_fields: List[str] = None, item_ignore_fileds: List[str] = None) -> TfsWorkitem:
        """
        Creates copy of given workitem.

        :param: source_item: id OR TfsWorkitem instance of a workitem to copy. Can't be None.
        :param: item_fields: list of fields to copy. if None then all fields except ignorable.
        :param: item_ignore_fileds: additional list of ignorable fields.
        :return: TfsWorkitem copy of given workitem
        """
        assert source_item, 'TfsWorkitemClient::copy_workitem: source_item can\'t be None'

        try:
            id = None
            if isinstance(source_item, int):
                id = source_item
            elif isinstance(source_item, TfsWorkitem):
                id = source_item.id

            item = self.__wi_client.copy_workitem(id, item_fields, item_ignore_fileds)
            return TfsWorkitem.from_workitem(item)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::copy_workitem: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    def update_workitem_fields(self, workitem, item_fields: List[dict], \
        expand: str='All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> TfsWorkitem:
        """
        Updates fields values for given workitem

        :param: workitem (int | TfsWorkitem): id OR TfsWorkitem instance of workitem. Can't be None.
        :param: fields list of dictonary, where { key: field name, value: field value }. E.g. ['System.Title', 'Item title']. Can't be None.
        :param: expand (str): The expand parameters for work item attributes. Possible options are { None, Relations, Fields, Links, All }.
        :param: bypass_rules (bool): Do not enforce the work item type rules on this update.
        :param: suppress_notifications (bool): Do not fire any notifications for this change
        :param: validate_only (bool): Indicate if you only want to validate the changes without saving the work item
        :return: TfsWorkitem instance with updated fields values.
        """
        assert workitem, 'TfsWorkitemClient::update_workitem_fields: workitem can\'t be None'
        assert item_fields, 'TfsWorkitemClient::update_workitem_fields: item_fields can\'t be None'

        id = None

        if isinstance(workitem, int):
            id = workitem
        elif isinstance(workitem, TfsWorkitem):
            id = workitem.id

        fields = defaultdict(str)
        if item_fields:
            for fld_dict in item_fields:
                for k, v in fld_dict.items():
                    fields[k] = v
        
        try:            
            item = self.__wi_client.update_workitem_fields(id, fields, expand, bypass_rules, suppress_notifications, validate_only)
            return TfsWorkitem.from_workitem(item)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::update_workitem_fields: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    ### RELATIONS

    def add_relation(self, source_workitem, destination_workitem, relation_type_name: str, \
        relation_attributes = None, \
        expand: str = 'All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> TfsWorkitem:
        """
        Add relation link of given type for given workitem to another workitem.

        :param: source_workitem (int | TfsWorkitem): source workitem for relation. Can't be None.
        :param: destination_workitem (int | TfsWorkitem): destination workitem for relation. Can't be None.
        :param: relation_type_name (str): relation type name. Look RelationMap for built-in relation types.
        :param: expand (str): The expand parameters for work item attributes. Possible options are { None, Relations, Fields, Links, All }.
        :param: bypass_rules (bool): Do not enforce the work item type rules on this update.
        :param: suppress_notifications (bool): Do not fire any notifications for this change
        :param: validate_only (bool): Indicate if you only want to validate the changes without saving the work item
        :return: TfsWorkitem instance with new relation.
        """
        assert source_workitem, 'TfsWorkitemClient::add_relation: source workitem can\'t be None'
        assert destination_workitem, 'TfsWorkitemClient::add_relation: destination workitem can\'t be None'
        assert relation_type_name, 'TfsWorkitemClient::add_relation: relation type name can\'t be None'

        source_id = None
        if isinstance(source_workitem, TfsWorkitem):
            source_id = source_workitem.id
        elif isinstance(source_workitem, int):
            source_id = source_workitem

        dest_id = None
        if isinstance(destination_workitem, int):
            dest_id = destination_workitem
        elif isinstance(destination_workitem, int):
            dest_id = destination_workitem

        try:
            item = self.__wi_client.add_relation(source_id, dest_id, relation_type_name, relation_attributes, expand, bypass_rules, suppress_notifications, validate_only)
            return TfsWorkitem.from_workitem(item)
        except ValueError as ex:
            raise TfsClientError('TfsWorkitemClient::add_relation: response is not json. Msg: {}'.format(ex), ex)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::add_relation: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    def remove_relation(self, workitem: TfsWorkitem, relation: TfsWorkitemRelation, \
        expand='All', bypass_rules=False, \
        suppress_notifications=False, validate_only=False) -> TfsWorkitem:
        """
        Remove relation from given workitem. jFYI: Tfs api can remove relation only for given index.

        :param: workitem (TfsWorkitem): source workitem. Can't be None.
        :param: relation (TfsWorkitemRelation): Removed relation to another workitem. Can't be None.
        :param: expand (str): The expand parameters for work item attributes. Possible options are { None, Relations, Fields, Links, All }.
        :param: bypass_rules (bool): Do not enforce the work item type rules on this update.
        :param: suppress_notifications (bool): Do not fire any notifications for this change
        :param: validate_only (bool): Indicate if you only want to validate the changes without saving the work item
        :return: TfsWorkitem instance with removed relation.
        """
        assert workitem, 'TfsWorkitemClient::remove_relation: workitem can\'t be None'
        assert relation, 'TfsWorkitemClient::remove_relation: relation can\'t be None'

        try:
            wi = self.__wi_client.get_single_workitem(workitem.id)
            dest_wi = self.__wi_client.get_single_workitem(relation.destination_id)
            rel = WorkitemRelation.create(relation.relation_name, dest_wi)

            item = self.__wi_client.remove_relation(wi, rel, expand, bypass_rules, suppress_notifications, validate_only)
            return TfsWorkitem.from_workitem(item)
        except ValueError as ex:
            raise TfsClientError('TfsWorkitemClient::remove_relation: response is not json. Msg: {}'.format(ex), ex)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::remove_relation: EXCEPTION raised. Msg: {}'.format(ex), ex)
        
    ### END RELATIONS

    ### WIQL REGION
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/queries/get?view=azure-devops-rest-6.0
    def run_saved_query(self, query_id: str) -> TfsWiqlResult:
        """
        Retrieves an individual query and its children.

        :param: query_id (str): ID or path of the query. Can't be None.
        :return: TfsWiqlResult instance
        """
        assert query_id, 'TfsWorkitemClient::run_saved_query: query id can\'t be None'

        if not isinstance(query_id, str):
            raise TfsClientError('TfsWorkitemClient::run_saved_query: query_id must be string')
        
        res = self.__wi_client.run_saved_query(query_id)
        return TfsWiqlResult.from_wiql_result(res)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
    def run_wiql(self, query: str, max_top: int = -1) -> TfsWiqlResult:
        """
        Gets the results of the query given its WIQL.

        :param: query (str): The text of the WIQL query. Can't be None.
        :param: max_top (int): The max number of results to return.
        :return: TfsWiqlResult instance.
        """
        assert query, 'TfsWorkitemClient::run_wiql: query can\'t be None'

        res = self.__wi_client.run_wiql(query, max_top)
        return TfsWiqlResult.from_wiql_result(res)

    ### END WIQL REGION