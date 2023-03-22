from enum import Enum
from typing import List, Dict
from pytfsclient.models.workitems.tfs_update_relations_result import UpdateRelationsResult
from pytfsclient.models.workitems.tfs_workitem_relation import WorkitemRelation

_IgnoreFields = [
    'System.Id',
    'System.WorkItemType'
]

class UpdateFieldsResult(Enum):
    """
    Update workitem fields result.

    Enum values:
    - UPDATE_EXCEPTION: exception raised
    - UPDATE_FAIL: Fail to get result. Fields are not updated.
    - UPDATE_EMPTY: Nothing to update result
    - UPDATE_SUCCESS: Fields successfully updated
    """
    UPDATE_EXCEPTION = 1
    UPDATE_FAIL = 2
    UPDATE_EMPTY = 3

    UPDATE_SUCCESS = 0

class Workitem:
    """
    Workitem model class. Contains properties of workitem
    """

    ### Properties region ###

    @property
    def id(self) -> int:
        """
        Id of workitem
        """
        return self.__id
    
    @property
    def url(self) -> str:
        """
        URL of workitem
        """
        return self.__url
    
    @property
    def revision(self) -> int:
        """
        Revision of workitem.
        """
        return self.__fields['System.Rev'] if 'System.Rev' in self.__fields else None
    
    @property
    def type_name(self) -> str:
        """
        Returns type name of workitem.
        """
        return self.__type_name
    
    @property
    def title(self) -> str:
        """
        Current title of workitem. Can be edited.
        Returns None if workitem doesn't contain title
        """
        if 'System.Title' in self.__updated_fields:
            return self.__updated_fields['System.Title']
        
        return self.__fields['System.Title'] if 'System.Title' in self.__fields else None
    
    @title.setter
    def title(self, value: str) -> None:
        self.__updated_fields['System.Title'] = value

    @property
    def description(self) -> str:
        """
        Returns description property of workitem. Can be edited.
        If workitem does not contain 'System.Description' property by default then retuns None
        """
        if 'System.Description' in self.__updated_fields:
            return self.__updated_fields['System.Description']

        return self.__fields['System.Description'] if 'System.Description' in self.__fields else None

    @description.setter
    def description(self, value: str) -> None:
        self.__updated_fields['System.Description'] = value

    @property
    def assigned_to(self) -> str:
        """
        Return AssignedTo property of workitem. 
        If workitem contains AssignedTo property then returns 'displayName'.
        If workitem doesn't contain AssignedTo property then returns None.
        """
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
        """
        Returns current list of fields names of workitem (properties names)
        """
        return self.__fields.keys()
    
    @property
    def fields(self) -> Dict[str, str]:
        """
        Returns Dictonary(str, str) of
        """
        # Merge two dictonaries
        # python 3.9 and higher (z = x | y)
        # Using z = { **x, **y }
        return { **self.__updated_fields, **self.__fields }
    
    def __getitem__(self, fld_name: str) -> str:
        """
        Returns value of field of workitem.
        :param: fld_name (str) - field name
        """
        assert fld_name, 'Field name can\'t be None'

        if fld_name in self.__updated_fields:
            return self.__updated_fields[fld_name]
        
        return self.__fields[fld_name] if fld_name in self.__fields else None
    
    def __setitem__(self, fld_name: str, fld_value: str) -> None:
        """
        Sets workitem property value.

        :param: fld_name (str): property name. Can't be None.
        :param: fld_value (str): property value. Can't be None.
        """
        assert fld_name, 'Field name can\'t be None'
        assert fld_value, 'Field value can\'t be None'

        self.__updated_fields[fld_name] = fld_value

    @property
    def relations(self) -> List[WorkitemRelation]:
        """
        Returns list of relations (TfsWorkitemRelation) of workitem
        """
        return self.__relations
    
    ### END PROPERTY REGION ###

    # Update internal workitem fields
    def update_fields(self) -> UpdateFieldsResult:
        """
        """
        
        pass

    ### RELATION REGION ###

    def add_relation(self, destination_workitem, relation_type_name: str, \
        relation_attributes = None) -> UpdateRelationsResult:
        """
        """

        pass

    ### END RELATION REGION ###

    @classmethod
    def from_json(cls, client, json_item):
        """
        Creates TfsWorkitem instance from given json item instance.
        """
        
        wi = cls()

        wi.__client = client
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

        return wi
    
