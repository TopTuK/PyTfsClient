from typing import List
from urllib.error import HTTPError
from .http_client import HttpClient
from .tfs_client import API_VERSION, TfsBaseClient, TfsClientError, batch
from .tfs_workitem_model import TfsWorkitem
from .tfs_wiql_model import TfsWiqlResult
from .tfs_workitem_relation_model import TfsWorkitemRelation

_WORKITEM_URL = 'wit/workitems'
_WIQL_URL = 'wit/wiql'
_QUERY_URL = 'wit/queries'

class TfsWorkitemClient:
    """
    TFS workitem client facade for managing workitems and relations
    Should be created with TfsClientFactory.
    """

    def __init__(self, client: TfsBaseClient) -> None:
        self.__client: TfsBaseClient = client
        self.__http: HttpClient = client.http_client
    
    @property
    def client(self) -> TfsBaseClient:
        """
        TfsBaseClient instance
        """
        return self.__client

    def _get_items(self, request_url: str, query_params, under_project: bool = False) -> List[TfsWorkitem]:
        """
        Return list of TFSWorkitem or raise an exception
        """

        url = (self.client.project_url + '/' + request_url) if under_project else (self.client.api_url + '/' + request_url)

        try:
            response = self.__http.get(url, query_params=query_params)
            
            if not response:
                raise TfsClientError('TfsWorkitemClient::get_items: can\'t get response from TFS server')
            
            json_items = response.json()
            if 'value' in json_items:
                json_items = json_items['value']
                return [TfsWorkitem.from_json(self, json_item=json_item) for json_item in json_items]
            else:
                raise TfsClientError('TfsWorkitemClient::get_items: json http response has no value attribute')
        except ValueError as ex:
            raise TfsClientError('TfsWorkitemClient::get_items: EXCEPTION raised, http response is not json. Msg: {}'.format(ex))
        except HTTPError as ex:
            raise TfsClientError('TfsWorkitemClient::get_items: EXCEPTION raised. Got http error', ex)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::get_items: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-6.0
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

        if isinstance(item_ids, int):
            item_ids = [item_ids]
        if isinstance(item_ids, str):
            item_ids = [int(item_ids)]

        query_params = {
            '$expand' : expand,
            'api-version' : API_VERSION
        }

        if item_fields:
            query_params['fields'] = ','.join(item_fields)
        
        workitems = list()
        for items in batch(list(item_ids), batch_size):
            query_params['ids'] = ','.join(map(str, items))

            workitems += self._get_items(_WORKITEM_URL, query_params=query_params)
        
        return workitems
    
    def get_single_workitem(self, item_id, item_fields: List[str] = None) -> TfsWorkitem:
        """
        Get TFS workitem

        :param: item_id (str | int): id of requesting item. Can't be None.
        :param: item_fields: list of requested fields for TFS workitems. if None then all fields
        :return: TfsWorkitem instance
        """
        assert item_id, 'TfsWorkitemClient::get_single_workitem: item_id can\'t be None'

        return self.get_workitems(item_ids=item_id, item_fields=item_fields)[0]
    
    # return dictonary with standart query params
    @staticmethod
    def __make_query_params(expand: str, bypass_rules: bool, suppress_notifications: bool, validate_only: bool) -> dict:
        '''Return dictonary with standart query params'''
        return {
            'api-version' : API_VERSION,
            '$expand' : expand,
            'bypassRules' : str(bypass_rules),
            'suppressNotifications' : str(bypass_rules),
            'validateOnly' : str(validate_only)
        }
    
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

        # request url
        request_url = '{}/{}/${}'.format(self.client.project_url, _WORKITEM_URL, type_name)

        # query params
        query_params = TfsWorkitemClient.__make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body. Missing @from parametr!
        request_body = [dict(op='add', path='/fields/{}'.format(name), value=value) for name, value in item_fields.items()] \
            if item_fields else []
        
        # extend request body with relations
        # relation = dict(rel=relation_type, url=destination_item_url, attributes=relation_attributes)
        if item_relations:
            for relation in item_relations:
                rel = dict(rel=relation.relation_name, url=relation.url, attributes=None)
                request_body.append(dict(op='add', path='/relations/-', value=rel))
        
        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            response = self.__http.post_json(resource=request_url, json_data=request_body, \
                query_params=query_params, custom_headers=custom_headers)
            
            if response:
                return TfsWorkitem.from_json(self, response.json())
            else:
                raise TfsClientError('TfsWorkitemClient::create_workitem: can\'t create workitem')
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::create_workitem: EXCEPTION raised. Msg: {}'.format(ex))
    
    def copy_workitem(self, source_item, item_fields: List[str] = None) -> TfsWorkitem:
        """
        Creates copy of given workitem.

        :param: source_item: id OR TfsWorkitem instance of a workitem to copy. Can't be None.
        :param: item_fields: list of fields to copy. if None then all fields except ignorable.
        :return: TfsWorkitem copy of given workitem
        """
        assert source_item, 'TfsWorkitemClient::copy_workitem: source_item can\'t be None'

        if isinstance(source_item, int):
            source_item = self.get_single_workitem(source_item)
        
        if (not isinstance(source_item, TfsWorkitem)) or (source_item is None):
            raise TfsClientError('TfsWorkitemClient::copy_workitem: source item is None')

        def copy_wi_fields():
            ignore_fields = [
                'System.TeamProject',
                'System.AreaId',
                'System.AreaPath',
                'System.AreaLevel1',
                'System.AreaLevel2',
                'System.AreaLevel3',
                'System.AreaLevel4',
                'System.Id',
                'System.NodeName',
                'System.Rev',
                'System.AutorizedDate',
                'System.RevisedDate',
                'System.IterationId',
                'System.IterationLevel1',
                'System.IterationLevel2',
                'System.IterationLevel3',
                'System.IterationLevel4',
                'System.CreatedBy',
                'System.ChangedDate',
                'System.ChangedBy',
                'System.AuthorizedAs',
                'System.AuthorizedDate',
                'System.Watermark',
                'System.BoardColumn'
            ]

            source_item_fields = source_item.fields

            fields = {}
            for fld_name, fld_value in source_item_fields.items():
                if fld_name in ignore_fields:
                    continue

                fields[fld_name] = item_fields[fld_name] if fld_name in item_fields else fld_value

            return fields

        item_type_name = source_item.type_name
        fields = copy_wi_fields()

        try:
            return self.create_workitem(item_type_name, item_fields=fields)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::copy_workitem: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.0
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

        if isinstance(workitem, int):
            workitem = self.get_single_workitem(workitem)
        
        if (not isinstance(workitem, TfsWorkitem)) or (workitem is None):
            raise TfsClientError('TfsWorkitemClient::update_workitem_fields: workitem is None')
        
        # request url
        request_url = '{}/{}/{}'.format(self.client.project_url, _WORKITEM_URL, workitem.id)

        # query params
        query_params = TfsWorkitemClient.__make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body
        request_body = [dict(op='add', path='/fields/{}'.format(name), value=value) for name, value in item_fields.items()] \
            if item_fields else []
        
        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            response = self.__http.patch_json(request_url, request_body, \
                query_params=query_params, custom_headers=custom_headers)
            
            if response:
                return TfsWorkitem.from_json(self, response.json())
            else:
                raise TfsClientError('TfsWorkitemClient::update_workitem_fields: can\'t update workitem fields. Response has error')
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::update_workitem_fields: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    ### RELATIONS

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.0#add-a-link
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

        if isinstance(source_workitem, TfsWorkitem):
            source_workitem = source_workitem.id
        
        if (not isinstance(source_workitem, int)):
            raise TfsClientError('TfsWorkitemClient::add_relation: can\'t get id of source workitem')
        
        if isinstance(destination_workitem, int):
            destination_workitem = self.get_single_workitem(destination_workitem)
        
        if (not destination_workitem) or (not isinstance(destination_workitem, TfsWorkitem)):
            raise TfsClientError('TfsWorkitemClient::add_relation: can\'t get destination workitem')
        
        # request url
        request_url = '{}/{}/{}'.format(self.client.project_url, _WORKITEM_URL, source_workitem)

        # query params
        query_params = TfsWorkitemClient.__make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body
        request_body = [dict(op='Add', path='/relations/-', \
            value=dict(rel=relation_type_name, url=destination_workitem.url, attributes=relation_attributes))]
        
        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            response = self.__http.patch_json(request_url, request_body, \
                query_params=query_params, custom_headers=custom_headers)
            
            if not response:
                raise TfsClientError('TfsWorkitemClient::add_relation: can\'t get response from TFS server')
            
            json_item = response.json()
            return TfsWorkitem.from_json(self, json_item=json_item)
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

        # Find relation index
        relation_idx = -1
        for idx, rel in enumerate(workitem.relations):
            if (rel.relation_name == relation.relation_name) and (rel.destination_id == relation.destination_id):
                relation_idx = idx
                break

        if relation_idx < 0:
            raise TfsClientError('TfsWorkitemClient::remove_relation: can\'t find relation index')

        # request url
        request_url = '{}/{}/{}'.format(self.client.project_url, _WORKITEM_URL, workitem.id)

        # query params
        query_params = TfsWorkitemClient.__make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body
        request_body = [
            dict(op='test', path='/rev', value=workitem.revision),
            dict(op='remove', path='/relations/{}'.format(relation_idx))
        ]

        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            response = self.__http.patch_json(request_url, request_body, \
                query_params=query_params, custom_headers=custom_headers)

            if not response:
                raise TfsClientError('TfsWorkitemClient::remove_relation: can\'t get response from TFS server')
            
            json_item = response.json()
            return TfsWorkitem.from_json(self, json_item=json_item)
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
        
        # request url
        request_url = '{}/{}/{}'.format(self.client.project_url, _QUERY_URL, query_id)

        # query params
        query_params = {
            'api-version' : API_VERSION,
            '$expand' : 'clauses'
        }

        try:
            response = self.__http.get(request_url, query_params=query_params)
            
            if not response:
                raise TfsClientError('TfsWorkitemClient::run_saved_query: can\'t get response from TFS Server')
            
            response = response.json()
            if 'wiql' in response:
                return self.run_wiql(str(response['wiql']))
            else:
                raise TfsClientError('TfsWorkitemClient::run_saved_query: response doesn\'t have wiql attribute')
        except ValueError as ex:
            raise TfsClientError('TfsWorkitemClient::run_saved_query: response is not json. Msg: {}'.format(ex), ex)
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::run_saved_query: EXCEPTION raised. Msg: {}'.format(ex), ex)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
    def run_wiql(self, query: str, max_top: int = -1) -> TfsWiqlResult:
        """
        Gets the results of the query given its WIQL.

        :param: query (str): The text of the WIQL query. Can't be None.
        :param: max_top (int): The max number of results to return.
        :return: TfsWiqlResult instance.
        """
        assert query, 'TfsWorkitemClient::run_wiql: query can\'t be None'

        # request url
        request_url = '{}/{}'.format(self.client.project_url, _WIQL_URL)

        # query params
        query_params = {
            'api-version' : API_VERSION
        }

        # request body
        request_body = {
            'query' : query
        }

        if max_top > 0:
            request_body['$top'] = str(max_top)
        
        try:
            response = self.__http.post_json(request_url, request_body, query_params=query_params)

            if not response:
                raise TfsClientError('TfsWorkitemClient::run_wiql: can\'t get response from TFS Server')
            
            return TfsWiqlResult.from_json(self, response.json())
        except ValueError as ex:
            raise TfsClientError('TfsWorkitemClient::run_wiql: response is not json. Msg: {}'.format(ex), ex)    
        except Exception as ex:
            raise TfsClientError('TfsWorkitemClient::run_wiql: EXCEPTION raised. Msg: {}'.format(ex), ex)

    ### END WIQL REGION