from typing import List, Union
from ..project.tfs_team_member import TeamMember
from .tfs_workitem_relation import WorkitemRelation
from ..client_error import ClientError

class FieldChange:
    '''
    Class contains information of field change of workitem.
    '''

    @property
    def name(self) -> str:
        '''
        Returns:
            Field name
        '''

        return self.__name

    @property
    def old_value(self) -> Union[str, TeamMember, dict]:
        '''
        Returns:
            Old value of field: str, TeamMember or dict
        '''
        return self.__old_value

    @property
    def new_value(self) -> Union[str, TeamMember, dict]:
        '''
        Returns:
            New value of field: str, TeamMember or dict
        '''
        return self.__new_value

    @classmethod
    def _from_json(cls, name, json_value):
        if not name:
            raise ClientError('name is None')

        fld_change = cls()

        try:
            fld_change.__name = name

            if 'newValue' in json_value:
                if isinstance(json_value['newValue'], dict):
                    if 'displayName' in json_value['newValue']:
                        fld_change.__new_value = TeamMember.from_json(json_value['newValue'])
                    else:
                        fld_change.__new_value = str(json_value['newValue']) # convert to str
                else:
                    fld_change.__new_value = str(json_value['newValue']) # convert to str
            else:
                fld_change.__new_value = None
            
            if 'oldValue' in json_value:
                if isinstance(json_value['oldValue'], dict):
                    if 'displayName' in json_value['oldValue']:
                        fld_change.__old_value = TeamMember.from_json(json_value['oldValue'])
                    else:
                        fld_change.__old_value = str(json_value['oldValue']) # convert to str
                else:
                    fld_change.__old_value = str(json_value['oldValue']) # convert to str
            else:
                fld_change.__old_value = None
        
        except Exception as ex:
            raise ClientError(ex)

        return fld_change

class WorkitemRelationChanges:
    '''
    Class contains information about workitem relation change.
    '''

    @property
    def added(self) -> List[WorkitemRelation]:
        '''
        Returns:
            List of added relations: List[WorkitemRelations]
        '''

        return self.__added

    @property
    def removed(self) -> List[WorkitemRelation]:
        '''
        Returns:
            List of removed relations: List[WorkitemRelations]
        '''

        return self.__removed

    @property
    def updated(self) -> List[WorkitemRelation]:
        '''
        Returns:
            List of updated relations: List[WorkitemRelations]
        '''

        return self.__updated

    @classmethod
    def _from_json(cls, json_item):
        rel_changes = cls()

        rel_changes.__added = None
        rel_changes.__removed = None
        rel_changes.__updated = None

        try:
            if 'added' in json_item:
                rel_changes.__added = [WorkitemRelation.from_json(rel_change) for rel_change in json_item['added']]

            if 'removed' in json_item:
                rel_changes.__removed = [WorkitemRelation.from_json(rel_change) for rel_change in json_item['removed']]

            if 'updated' in json_item:
                rel_changes.__removed = [WorkitemRelation.from_json(rel_change) for rel_change in json_item['updated']]
        
        except Exception as ex:
            raise ClientError(ex)

        return rel_changes
    
class WorkitemChange:
    '''
    Class contains information about workite change. Use WorkitemClient::get_workitem_changes().
    '''

    @property
    def id(self) -> int:
        '''
        Returns:
            Id of workitem change
        '''

        return self.__id

    @property
    def workitem_id(self) -> int:
        '''
        Returns:
            Id of workitem
        '''

        return self.__workitem_id
    
    @property
    def revision(self) -> int:
        '''
        Returns:
            Revision number
        '''

        return self.__rev
    
    @property
    def revised_by(self) -> TeamMember:
        '''
        Returns:
            Team member who revised workitem: TeamMember
        '''

        return self.__revised_by
    
    @property
    def revised_date(self):
        '''
        Returns:
            Date of revision
        '''

        return self.__revised_date
    
    @property
    def url(self) -> str:
        '''
        Returns:
            URL of workitem change
        '''

        return self.__url

    @property
    def field_changes(self) -> List[FieldChange]:
        '''
        Returns:
            List of changes of fields: List[FieldChange].
            Can be None
        '''

        return self.__field_changes
    
    @property
    def relation_changes(self) -> WorkitemRelationChanges:
        '''
        Returns:
            Information of relations changes: WorkitemRelationChanges
            Can be None.
        '''

        return self.__relation_changes
    
    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates WorkitemChange class instance from given json object.

        Args:
            json_response (object): json response from TFS Server.

        Returns:
            WorkitemChange class instance

        Raises:
            ClientError if json_item is invalid
        '''

        change = cls()

        try:
            change.__id = json_item['id']
            change.__workitem_id = json_item['workItemId']
            change.__rev = json_item['rev']

            change.__revised_by = TeamMember.from_json(json_item['revisedBy'])
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
        
        except Exception as ex:
            raise ClientError(ex)

        return change