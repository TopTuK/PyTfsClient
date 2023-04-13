from enum import Enum
from typing import List, Dict
from .tfs_update_relations_result import UpdateRelationsResult
from .tfs_workitem_relation import WorkitemRelation
from .tfs_workitem_changes import WorkitemChange
from ..client_error import ClientError

_IgnoreFields = [
    'System.Id',
    'System.WorkItemType'
]

class UpdateFieldsResult(Enum):
    '''
    ENUM: update workitem fields result.

    Values:
    - UPDATE_EXCEPTION: exception raised
    - UPDATE_FAIL: Fail to get result. Fields are not updated.
    - UPDATE_EMPTY: Nothing to update result
    - UPDATE_SUCCESS: Fields successfully updated
    '''

    UPDATE_EXCEPTION = 1
    UPDATE_FAIL = 2
    UPDATE_EMPTY = 3

    UPDATE_SUCCESS = 0

class Workitem:
    '''
    Workitem model class. Contains information about properties of workitem.
    '''

    ### Properties region ###

    @property
    def id(self) -> int:
        '''
        Returns:
            Id of workitem: int
        '''

        return self.__id
    
    @property
    def url(self) -> str:
        '''
        Returns:
            URL of workitem.
        '''

        return self.__url
    
    @property
    def revision(self) -> int:
        '''
        Returns:
            Current revision of workitem: int
        '''

        return self.__fields['System.Rev'] if 'System.Rev' in self.__fields else None
    
    @property
    def type_name(self) -> str:
        '''
        Returns:
            Type name of workitem: str
        '''

        return self.__type_name
    
    @property
    def title(self) -> str:
        '''
        Returns:
            Current title of workitem. Can be edited.
            None if workitem doesn't contain title property.
        '''

        if 'System.Title' in self.__updated_fields:
            return self.__updated_fields['System.Title']
        
        return self.__fields['System.Title'] if 'System.Title' in self.__fields else None
    
    @title.setter
    def title(self, value: str) -> None:
        '''
        Set title property
        '''

        self.__updated_fields['System.Title'] = value

    @property
    def description(self) -> str:
        '''
        Returns:
            Description property of workitem. Can be edited.
            If workitem does not contain 'System.Description' property returns None
        '''

        if 'System.Description' in self.__updated_fields:
            return self.__updated_fields['System.Description']

        return self.__fields['System.Description'] if 'System.Description' in self.__fields else None

    @description.setter
    def description(self, value: str) -> None:
        self.__updated_fields['System.Description'] = value

    @property
    def assigned_to(self) -> str:
        '''
        Returns:
            AssignedTo property of workitem: str
            If workitem contains AssignedTo property then returns 'displayName'.
            If workitem doesn't contain AssignedTo property then returns None.
        '''

        if 'System.AssignedTo' in self.__updated_fields:
            return self.__updated_fields['System.AssignedTo']

        if 'System.AssignedTo' in self.__fields:
            user = self.__fields['System.AssignedTo']
            if 'displayName' in user:
                return user['displayName']
            else:
                return str(user)

        return None
    
    @property
    def fields_keys(self) -> List[str]:
        '''
        Returns:
            List of fields names of workitem (properties names).
        '''

        return self.__fields.keys()
    
    @property
    def fields(self) -> Dict[str, str]:
        '''
        Returns:
            Dictonary(str, str) of fields and values
        '''

        # Merge two dictonaries
        # python 3.9 and higher (z = x | y)
        # Using z = { **x, **y }
        return { **self.__updated_fields, **self.__fields }
    
    def __getitem__(self, fld_name: str) -> str:
        '''
        Returns:
            Value of field of workitem.
            key (str): field name
        '''

        if not fld_name:
            raise ClientError('Field name can\'t be None')

        if fld_name in self.__updated_fields:
            return self.__updated_fields[fld_name]
        
        return self.__fields[fld_name] if fld_name in self.__fields else None
    
    def __setitem__(self, fld_name: str, fld_value: str) -> None:
        '''
        Sets workitem property value.

        Args:
            fld_name (str): property name. Can't be None.
            fld_value (str): property value. Can't be None.
        '''

        if not fld_name:
            raise ClientError('Field name can\'t be None')
        
        if not fld_value:
            raise ClientError('Field value can\'t be None')

        self.__updated_fields[fld_name] = fld_value

    @property
    def relations(self) -> List[WorkitemRelation]:
        '''
        Returns:
            List of relations of workitem: List[WorkitemRelation]
        '''

        return self.__relations
    
    ### END PROPERTY REGION ###

    # Update internal workitem fields
    def update_fields(self) -> UpdateFieldsResult:
        '''
        Updates on server values of fields of workitem.
        
        Returns:
            Result of operation: UpdateFieldsResult
        '''

        if len(self.__updated_fields) == 0:
            return UpdateFieldsResult.UPDATE_EMPTY
        
        try:
            # update workitem fields
            item = self.__client.update_workitem_fields(self.id, self.__updated_fields, expand='fields')

            if not item:
                return UpdateFieldsResult.UPDATE_FAIL
            
            self.__updated_fields.clear()
            self.__fields = item.__fields

            return UpdateFieldsResult.UPDATE_SUCCESS
        except:
            return UpdateFieldsResult.UPDATE_EXCEPTION
    
    def get_changes(self, skip: int = 0, top: int = -1) -> List[WorkitemChange]:
        '''
        Get history changes of workitem.

        Returns:
            workitem changes history: List[WorkitemChange]
        '''

        return self.__client.get_workitem_changes(self.id, skip, top)

    ### RELATION REGION ###

    def add_relation(self, destination_workitem, relation_type_name: str, \
        relation_attributes = None) -> UpdateRelationsResult:
        '''
        Adds relation to workitem.

        Args:
            destination_workitem (int, Workitem): destination workitem
            relation_type_name (str): relation type name
            relation_attributes: relation attributes
        
        Returns:
            Update relations result: UpdateRelationsResult
        '''

        try:
            item = self.__client.add_relation(self.id, destination_workitem, relation_type_name, \
                relation_attributes)
            
            if not item:
                return UpdateRelationsResult.UPDATE_FAIL

            self.__relations = item.__relations
            return UpdateRelationsResult.UPDATE_SUCCESS
        except:
            return UpdateRelationsResult.UPDATE_EXCEPTION

    ### END RELATION REGION ###

    @classmethod
    def from_json(cls, client, json_item):
        '''
        Classmethod creates Workitem instance from given json item.

        Args:
            client (WorkitemClient): WorkitemClient instance
            json_item (object): JSON object with attributes

        Returns:
            Workitem class instance
        
        Raises:
            ClientError with information about exception
        '''

        if not client:
            raise ClientError('client is None')
        
        wi = cls()

        try:
            wi.__client = client # WorkitemClient
            wi.__raw = json_item

            wi.__id = json_item['id']
            wi.__url = json_item['url']

            wi.__updated_fields = {}

            # Fields
            if 'fields' in json_item:
                wi.__fields = { fld : value for (fld, value) in json_item['fields'].items() if fld not in _IgnoreFields }
                wi.__type_name = json_item['fields']['System.WorkItemType'] if 'System.WorkItemType' in json_item['fields'] else None
            else:
                wi.__fields = {}
                wi.__type_name = None

            # Relations
            wi.__relations = None
            if 'relations' in json_item:
                wi.__relations = [WorkitemRelation.from_json(json_relation) for json_relation in json_item['relations']]
            else:
                wi.__relations = []
                
        except Exception as ex:
            raise ClientError(ex)

        return wi
    
