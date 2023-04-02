from enum import Enum
from typing import List, Dict
from .tfs_workitem_relation_model import TfsWorkitemRelation
from .tfs_project_model import TeamMember

from .models.workitems.tfs_workitem import Workitem, UpdateFieldsResult, UpdateRelationsResult

class TfsUpdateFieldsResult(Enum):
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

class TfsUpdateRelationsResult(Enum):
    """
    Update workitem relations result.

    Enum values:
    - UPDATE_EXCEPTION: exception raised
    - UPDATE_FAIL: Failed to update relations
    - UPDATE_SUCCESS: Relations successfully updated
    """
    UPDATE_EXCEPTION = 1
    UPDATE_FAIL = 2
    
    UPDATE_SUCCESS = 0

class TfsWorkitemType(Enum):
    """
    Built-in workitem types. Import 'TfsWorkitemTypes' for type names
    """
    REQUIREMENT = 0
    TASK = 1
    CHANGE_REQUEST = 2
    BUG = 3

# Workitems type map
TfsWorkitemTypes = {
    TfsWorkitemType.REQUIREMENT : 'Requirement',
    TfsWorkitemType.CHANGE_REQUEST : 'Change request',
    TfsWorkitemType.TASK : 'Task',
    TfsWorkitemType.BUG : 'Bug'
}

class TfsWorkitem:
    """
    Workitem model class. Contains properties of workitem.
    """

    ### PROPERTY REGION ###

    @property
    def id(self) -> int:
        """
        Id of workitem
        """
        return self.__item.id
    
    @property
    def url(self) -> str:
        """
        URL of workitem
        """
        return self.__item.url

    @property
    def title(self) -> str:
        """
        Current title of workitem. Can be edited.
        Returns None if workitem doesn't contain title
        """

        return self.__item.title
    
    @title.setter
    def title(self, value: str) -> None:
        self.__item.title = value
    
    @property
    def revision(self) -> int:
        """
        Revision of workitem.
        """
        return self.__item.revision
    
    @property
    def assigned_to(self) -> str:
        """
        Return AssignedTo property of workitem. 
        If workitem contains AssignedTo property then returns 'displayName'.
        If workitem doesn't contain AssignedTo property then returns None.
        """
        return self.__item.assigned_to
    
    @property
    def fields_keys(self) -> List[str]:
        """
        Returns current list of fields names of workitem (properties names)
        """
        return self.__items.fields_keys

    @property
    def type_name(self) -> str:
        """
        Returns type name of workitem.
        """
        return self.__item.type_name
    
    @property
    def description(self) -> str:
        """
        Returns description property of workitem. Can be edited.
        If workitem does not contain 'System.Description' property by default then retuns None
        """
        
        return self.__item.description

    @description.setter
    def description(self, value: str) -> None:
        self.__item.description = value
    
    @property
    def fields(self) -> Dict[str, str]:
        """
        Returns Dictonary(str, str) of
        """

        return self.__items.fields

    def __getitem__(self, fld_name: str) -> str:
        """
        Returns value of field of workitem.
        :param: fld_name (str): field name
        """
        assert fld_name, 'Field name can\'t be None'

        return self.__item[fld_name]

    def __setitem__(self, fld_name: str, fld_value: str) -> None:
        """
        Sets workitem property value.

        :param: fld_name (str): property name. Can't be None.
        :param: fld_value (str): property value. Can't be None.
        """
        assert fld_name, 'Field name can\'t be None'
        assert fld_value, 'Field value can\'t be None'

        self.__item[fld_name] = fld_value
    
    @property
    def relations(self) -> List[TfsWorkitemRelation]:
        """
        Returns list of relations (TfsWorkitemRelation) of workitem
        """
        return [TfsWorkitemRelation.from_relation(rel) for rel in self.__item.relations]
    
    ### END PROPERTY REGION ###

    # Update internal workitem fields
    def update_fields(self) -> TfsUpdateFieldsResult:
        """
        Updates values of fields of workitem. It makes an api call.
        :return: TfsUpdateFieldsResult value. If success, current workitem fields are updated.
        """

        try:
            update_result: UpdateFieldsResult = self.__item.update_fields()

            if update_result == UpdateFieldsResult.UPDATE_SUCCESS:
                return TfsUpdateFieldsResult.UPDATE_SUCCESS
            elif update_result == UpdateFieldsResult.UPDATE_EMPTY:
                return TfsUpdateFieldsResult.UPDATE_EMPTY
            elif update_result == UpdateFieldsResult.UPDATE_EXCEPTION:
                return TfsUpdateFieldsResult.UPDATE_EXCEPTION
            else:
                return TfsUpdateFieldsResult.UPDATE_FAIL
        except:
            return TfsUpdateFieldsResult.UPDATE_EXCEPTION
    
    ### RELATION REGION ###
    
    def add_relation(self, destination_workitem, relation_type_name: str, \
        relation_attributes = None) -> TfsUpdateRelationsResult:
        """
        Adds relation to workitem.

        :param: destination_workitem (TfsWorkitem | int): destination workitem. Can't be None.
        :param: relation_type_name (str): relation type name. Can't be None.
        :return: TfsUpdateRelationsResult value. If success then relations of workitem are updated successfully.
        """

        id = None
        if destination_workitem is int:
            id = destination_workitem
        elif destination_workitem is TfsWorkitem:
            id = destination_workitem.id

        update_result: UpdateRelationsResult = self.__item.add_relation(id, relation_type_name, relation_attributes)

        if update_result == UpdateRelationsResult.UPDATE_SUCCESS:
            return TfsUpdateRelationsResult.UPDATE_SUCCESS
        elif update_result == UpdateRelationsResult.UPDATE_EXCEPTION:
            return TfsUpdateRelationsResult.UPDATE_EXCEPTION
        else:
            return TfsUpdateRelationsResult.UPDATE_FAIL

    ### END RELATION REGION ###

    @classmethod
    def from_workitem(cls, workitem: Workitem):
        wi = cls()

        wi.__item: Workitem = workitem

        return wi