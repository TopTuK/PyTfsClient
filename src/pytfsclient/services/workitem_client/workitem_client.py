from typing import List, Dict
from requests import HTTPError
from ...models.client_error import ClientError
from ...models.workitems.tfs_wiql_result import WiqlResult
from ...models.workitems.tfs_workitem import Workitem
from ...models.workitems.tfs_workitem_relation import WorkitemRelation
from ..base_client import BaseClient
from ...client_connection import ClientConnection
from ..helpers.batch_iterable import batch

class WorkitemClient(BaseClient):
    """
    TFS Workitem Client facade for managing workitems and relations
    """

    _WORKITEM_URL = 'wit/workitems'
    _WIQL_URL = 'wit/wiql'
    _QUERY_URL = 'wit/queries'

    # Constructor
    def __init__(self, client_connection: ClientConnection) -> None:
        super().__init__(client_connection)

    def _get_items(self, request_url: str, query_params, under_project: bool = False) -> List[Workitem]:
        """
        Return list of Workitem or raise an exception
        """
        
        url = f'{self.client_connection.project_url}{request_url}' if under_project else f'{self.client_connection.api_url}{request_url}'
        
        try:
            http_response = self.http_client.get(url, query_params=query_params)

            if not http_response:
                raise ClientError('WorkitemClient::get_items: can\'t get response from TFS server')
            
            json_items = http_response.json()
            if 'value' in json_items:
                json_items = json_items['value']
                return [Workitem.from_json(self, json_item=json_item) for json_item in json_items]
            else:
                raise ClientError('WorkitemClient::get_items: json http response has no value attribute')
        except ValueError as ex:
            raise ClientError(f'WorkitemClient::get_items: EXCEPTION raised, http response is not json. Msg: {ex}', ex)
        except HTTPError as ex:
            raise ClientError(f'WorkitemClient::get_items: EXCEPTION raised. Got http error', ex)
        except Exception as ex:
            raise ClientError(f'WorkitemClient::get_items: EXCEPTION raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-6.0
    def get_workitems(self, item_ids, item_fields: List[str] = None, expand: str = 'All', batch_size: int = 50) -> List[Workitem]:
        """
        Return list of Workitems for given list of item ids.
        """
        
        assert item_ids, 'WorkitemClient::get_workitems: item ids can\'t be None'

        if isinstance(item_ids, int):
            item_ids = [item_ids]
        if isinstance(item_ids, str):
            item_ids = [int(item_ids)]

        # Http Query Params
        query_params = {
            '$expand' : expand,
            'api-version' : self.api_version
        }

        # Request filelds
        if item_fields:
            query_params['fields'] = ','.join(item_fields)

        workitems = list()
        for items in batch(list(item_ids), batch_size):
            query_params['ids'] = ','.join(map(str, items))

            workitems += self._get_items(self._WORKITEM_URL, query_params=query_params)
        
        return workitems

    def get_single_workitem(self, item_id, item_fields: List[str] = None) -> Workitem:
        """
        Get TFS workitem
        """
        
        assert item_id, 'WorkitemClient::get_single_workitem: item_id can\'t be None'

        return self.get_workitems(item_ids=item_id, item_fields=item_fields)[0]

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
    def create_workitem(self, type_name: str, \
        item_fields: Dict[str, str] = None, item_relations: List[WorkitemRelation] = None, \
        expand: str = 'All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> Workitem:
        """
        Creates workitem of given type, properties and relations
        """

        assert type_name, 'WorkitemClient::create_workitem: item type name can\'t be None'

        # request url
        request_url = f'{self.client_connection.project_url}/{self._WORKITEM_URL}/${type_name}'

        # query params
        query_params = WorkitemClient._make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body. TODO: Add missing @from param!
        request_body = [dict(op='add', path='/fields/{}'.format(name), value=value) for name, value in item_fields.items()] \
            if item_fields else []
        
        if item_relations:
            # extend request body with relations
            # relation = dict(rel=relation_type, url=destination_item_url, attributes=relation_attributes)
            for relation in item_relations:
                rel = dict(rel=relation.relation_name, url=relation.url, attributes=None)
                request_body.append(dict(op='add', path='/relations/-', value=rel))
        
        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            http_response = self.http_client.post_json(resource=request_url, json_data=request_body,\
                query_params=query_params, custom_headers=custom_headers)
            
            if http_response:
                return Workitem.from_json(self, http_response.json())
            else:
                raise ClientError('WorkitemClient::create_workitem: can\'t create workitem')
        except Exception as ex:
            raise ClientError(f'WorkitemClient::create_workitem: EXCEPTION raised. Msg: {ex}', ex)

    def copy_workitem(self, source_item, item_fields: List[str] = None, item_ignore_fileds: List[str] = None) -> Workitem:
        """
        Creates copy of given workitem
        """

        assert source_item, 'WorkitemClient::copy_workitem: source_item can\'t be None'

        if isinstance(source_item, int):
            source_item = self.get_single_workitem(source_item)
        
        if (not isinstance(source_item, Workitem)) or (source_item is None):
            raise ClientError('WorkitemClient::copy_workitem: source item is None')
        
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
                'System.BoardColumn',
            ]

            source_item_fields = source_item.fields

            fields = {}
            for fld_name, fld_value in source_item_fields.items():
                if item_ignore_fileds:
                    if fld_name in item_ignore_fileds:
                        continue

                if fld_name in ignore_fields:
                    continue

                if item_fields:
                    fields[fld_name] = item_fields[fld_name] if (fld_name in item_fields) else fld_value
                else:
                    fields[fld_name] = fld_value

            return fields

        fields = copy_wi_fields()
        item_type_name = source_item.type_name

        try:
            return self.create_workitem(item_type_name, item_fields=fields)
        except Exception as ex:
            raise ClientError(f'WorkitemClient::copy_workitem: EXCEPTION raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.0
    def update_workitem_fields(self, workitem, item_fields: Dict[str, str], \
        expand: str='All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> Workitem:
        """
        Updates fields values for given workitem
        """

        assert workitem, 'WorkitemClient::update_workitem_fields: workitem can\'t be None'
        assert item_fields, 'WorkitemClient::update_workitem_fields: item_fields can\'t be None'
        
        if isinstance(workitem, int):
            workitem = self.get_single_workitem(workitem)

        if (not isinstance(workitem, Workitem)) or (workitem is None):
            raise ClientError('WorkitemClient::update_workitem_fields: workitem is None')
        
        # request url
        request_url = f'{self.client_connection.project_url}/{self._WORKITEM_URL}/{workitem.id}'

        # query params
        query_params = WorkitemClient._make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body
        request_body = [dict(op='add', path='/fields/{}'.format(name), value=value) for name, value in item_fields.items()] \
            if item_fields else []
        
        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            http_response = self.http_client.patch_json(request_url, request_body, \
                query_params=query_params, custom_headers=custom_headers)
            
            if http_response:
                return Workitem.from_json(self, http_response.json())
            else:
                raise ClientError('WorkitemClient::update_workitem_fields: can\'t update workitem fields. Response has error')
        except Exception as ex:
            raise ClientError(f'WorkitemClient::update_workitem_fields: EXCEPTION raised. Msg: {ex}', ex)

    ### REGION MANAGING RELATIONS ###

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-6.0#add-a-link
    def add_relation(self, source_workitem, destination_workitem, relation_type_name: str, \
        relation_attributes = None, \
        expand: str = 'All', bypass_rules: bool = False, \
        suppress_notifications: bool = False, validate_only: bool = False) -> Workitem:
        """
        Add relation link of given type for given workitem to another workitem
        """

        assert source_workitem, 'WorkitemClient::add_relation: source workitem can\'t be None'
        assert destination_workitem, 'WorkitemClient::add_relation: destination workitem can\'t be None'
        assert relation_type_name, 'WorkitemClient::add_relation: relation type name can\'t be None'

        if isinstance(source_workitem, Workitem):
            source_workitem = source_workitem.id
        
        if (not isinstance(source_workitem, int)):
            raise ClientError('WorkitemClient::add_relation: can\'t get id of source workitem')
        
        if isinstance(destination_workitem, int):
            destination_workitem = self.get_single_workitem(destination_workitem)

        if (not destination_workitem) or (not isinstance(destination_workitem, Workitem)):
            raise ClientError('WorkitemClient::add_relation: can\'t get destination workitem')
        
        # request url
        request_url = f'{self.client_connection.project_url}/{self._WORKITEM_URL}/{source_workitem}'

        # query params
        query_params = WorkitemClient._make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

        # request body
        request_body = [dict(op='Add', path='/relations/-', \
            value=dict(rel=relation_type_name, url=destination_workitem.url, attributes=relation_attributes))]
        
        # custom headers. Media Types: "application/json-patch+json"
        custom_headers = {
            'Content-Type' : 'application/json-patch+json'
        }

        try:
            response = self.http_client.patch_json(request_url, request_body, \
                query_params=query_params, custom_headers=custom_headers)
            
            if not response:
                raise ClientError('TfsWorkitemClient::add_relation: can\'t get response from TFS server')
            
            json_item = response.json()
            return Workitem.from_json(self, json_item=json_item)
        except ValueError as ex:
            raise ClientError(f'TfsWorkitemClient::add_relation: response is not json. Msg: {ex}', ex)
        except Exception as ex:
            raise ClientError(f'TfsWorkitemClient::add_relation: EXCEPTION raised. Msg: {ex}', ex)

    def remove_relation(self, workitem: Workitem, relation: WorkitemRelation, \
        expand='All', bypass_rules=False, \
        suppress_notifications=False, validate_only=False) -> Workitem:
        """
        Remove relation from given workitem. jFYI: Tfs api can remove relation only for given index
        """

        assert workitem, 'WorkitemClient::remove_relation: workitem can\'t be None'
        assert relation, 'WorkitemClient::remove_relation: relation can\'t be None'

        # Find relation index
        relation_idx = -1
        for idx, rel in enumerate(workitem.relations):
            if (rel.relation_name == relation.relation_name) and (rel.destination_id == relation.destination_id):
                relation_idx = idx
                break
        
        if relation_idx < 0:
            raise ClientError('WorkitemClient::remove_relation: can\'t find relation index')
        
        # request url
        request_url = f'{self.client_connection.project_url}/{self._WORKITEM_URL}/{workitem.id}'

        # query params
        query_params = WorkitemClient._make_query_params(expand, bypass_rules, suppress_notifications, validate_only)

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
            http_response = self.http_client.patch_json(request_url, request_body, \
                query_params=query_params, custom_headers=custom_headers)

            if not http_response:
                raise ClientError('WorkitemClient::remove_relation: can\'t get response from TFS server')
            
            json_item = http_response.json()
            return Workitem.from_json(self, json_item=json_item)
        except ValueError as ex:
            raise ClientError(f'WorkitemClient::remove_relation: response is not json. Msg: {ex}', ex)
        except Exception as ex:
            raise ClientError(f'WorkitemClient::remove_relation: EXCEPTION raised. Msg: {ex}', ex)

    ### END REGION MANAGING RELATIONS ###

    ### REGION QUERIES (WIQL) ###

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/queries/get?view=azure-devops-rest-6.0
    def run_saved_query(self, query_id: str) -> WiqlResult:
        """
        Retrieves an individual query and its children
        """

        assert query_id, 'WorkitemClient::run_saved_query: query id can\'t be None'

        if not isinstance(query_id, str):
            raise ClientError('WorkitemClient::run_saved_query: query_id must be string')
        
        # request url
        request_url = f'{self.client_connection.project_url}/{self._QUERY_URL}/{query_id}'

        # query params
        query_params = {
            'api-version' : self.api_version,
            '$expand' : 'clauses',
        }

        try:
            http_response = self.http_client.get(request_url, query_params=query_params)
            
            if not http_response:
                raise ClientError('WorkitemClient::run_saved_query: can\'t get response from TFS Server')
            
            response = http_response.json()
            if 'wiql' in response:
                return self.run_wiql(str(response['wiql']))
            else:
                raise ClientError('WorkitemClient::run_saved_query: response doesn\'t have wiql attribute')
        except ValueError as ex:
            raise ClientError(f'WorkitemClient::run_saved_query: response is not json. Msg: {ex}', ex)
        except Exception as ex:
            raise ClientError(f'WorkitemClient::run_saved_query: EXCEPTION raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
    def run_wiql(self, query: str, max_top: int = -1) -> WiqlResult:
        """
        Gets the results of the query given its WIQL
        """

        assert query, 'WorkitemClient::run_wiql: query can\'t be None'

        # request url
        request_url = f'{self.client_connection.project_url}/{self._WIQL_URL}'

        # query params
        query_params = {
            'api-version' : self.api_version
        }

        # request body
        request_body = {
            'query' : query
        }

        if max_top > 0:
            request_body['$top'] = str(max_top)

        try:
            http_response = self.http_client.post_json(request_url, request_body, query_params=query_params)

            if not http_response:
                raise ClientError('WorkitemClient::run_wiql: can\'t get response from TFS Server')
            
            return WiqlResult.from_json(self, http_response.json())
        except ValueError as ex:
            raise ClientError(f'WorkitemClient::run_wiql: response is not json. Msg: {ex}', ex)    
        except Exception as ex:
            raise ClientError(f'WorkitemClient::run_wiql: EXCEPTION raised. Msg: {ex}', ex)

    ### END REGION QUERIES (WIQL) ###

