from typing import List, Union
from ..project.tfs_team_member import TfsTeamMember
from .tfs_workitem_relation import WorkitemRelation

class FieldChange:
    '''
    Field change model
    '''

    @property
    def name(self) -> str:
        return self.__name

    @property
    def old_value(self) -> Union[str, TfsTeamMember, dict]:
        return self.__old_value

    @property
    def new_value(self) -> Union[str, TfsTeamMember, dict]:
        return self.__new_value

    @classmethod
    def _from_json(cls, name, json_value):
        fld_change = cls()

        fld_change.__name = name

        if 'newValue' in json_value:
            if isinstance(json_value['newValue'], dict):
                if 'displayName' in json_value['newValue']:
                    fld_change.__new_value = TfsTeamMember.from_json(json_value['newValue'])
                else:
                   fld_change.__new_value = str(json_value['newValue']) # convert to str
            else:
                fld_change.__new_value = str(json_value['newValue']) # convert to str
        else:
            fld_change.__new_value = None
        
        if 'oldValue' in json_value:
            if isinstance(json_value['oldValue'], dict):
                if 'displayName' in json_value['oldValue']:
                    fld_change.__old_value = TfsTeamMember.from_json(json_value['oldValue'])
                else:
                   fld_change.__old_value = str(json_value['oldValue']) # convert to str
            else:
                fld_change.__old_value = str(json_value['oldValue']) # convert to str
        else:
            fld_change.__old_value = None

        return fld_change

class WorkitemRelationChanges:
    '''
    '''

    @property
    def added(self) -> List[WorkitemRelation]:
        return self.__added

    @property
    def removed(self) -> List[WorkitemRelation]:
        return self.__removed

    @property
    def updated(self) -> List[WorkitemRelation]:
        return self.__updated

    @classmethod
    def _from_json(cls, json_item):
        rel_changes = cls()

        rel_changes.__added = None
        rel_changes.__removed = None
        rel_changes.__updated = None

        if 'added' in json_item:
            rel_changes.__added = [WorkitemRelation.from_json(rel_change) for rel_change in json_item['added']]

        if 'removed' in json_item:
            rel_changes.__removed = [WorkitemRelation.from_json(rel_change) for rel_change in json_item['removed']]

        if 'updated' in json_item:
            rel_changes.__removed = [WorkitemRelation.from_json(rel_change) for rel_change in json_item['updated']]

        return rel_changes
    
class WorkitemChange:
    '''
    Workitem update change model
    '''

    @property
    def id(self) -> int:
        return self.__id

    @property
    def workitem_id(self) -> int:
        return self.__workitem_id
    
    @property
    def revision(self) -> int:
        return self.__rev
    
    @property
    def revised_by(self) -> TfsTeamMember:
        return self.__revised_by
    
    @property
    def revised_date(self):
        return self.__revised_date
    
    @property
    def url(self):
        return self.__url

    @property
    def field_changes(self) -> List[FieldChange]:
        return self.__field_changes
    
    @property
    def relation_changes(self) -> WorkitemRelationChanges:
        return self.__relation_changes
    
    @classmethod
    def from_json(cls, json_item):
        change = cls()

        change.__id = json_item['id']
        change.__workitem_id = json_item['workItemId']
        change.__rev = json_item['rev']

        change.__revised_by = TfsTeamMember.from_json(json_item['revisedBy'])
        change.__revised_date = json_item['revisedDate']

        change.__url = json_item['url']

        if 'fields' in json_item:
            change.__field_changes = [FieldChange._from_json(key, value) for key, value in json_item['fields'].items()]
        else:
            change.__field_changes = None

        if ('relations' in json_item) and (isinstance(json_item['relations'], dict)):
            change.__relation_changes = WorkitemRelationChanges._from_json(json_item['relations'])
        else:
            change.__relation_changes = None

        return change