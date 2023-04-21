from enum import Enum
from ...models.workitems.tfs_workitem import UpdateFieldsResult, Workitem
from ...models.project.tfs_team_member import TeamMember
from ...models.client_error import ClientError

class MentionResult(Enum):
    '''
    ENUM: send mention result

    Values:
        MENTION_SUCCESS
        MENTION_ERROR
        MENTION_EXCEPTION
    '''

    MENTION_SUCCESS = 0
    MENTION_ERROR = 1
    MENTION_EXCEPTION = 2

class MentionClient:
    '''
    Mention client for mention users of TFS/Azure service
    '''

    _TFS_HISTORY_FIELD = 'System.History'
    
    @staticmethod
    def send_mention(workitem: Workitem, to_user: TeamMember, \
                    message: str, from_user: TeamMember = None) -> MentionResult:
        '''
        Sends mention to user. Writes mention to History of workitem
        WARNING: this function uses non-public API

        Args:
            workitem (Workitem): workitem where mention will send
            to_user (TeamMember): mentioned user
            message (str): mention text
            from_user (TeamMember): copy user who will be mentioned. Default: None

        Returns:
            Send mention result: MentionResult (incl. MENTION_EXCEPTION)

        Raises:
            ClientError: if workitem, to_user or message is None
        '''

        if not workitem:
            raise ClientError('workitem can\'t be None')
        
        if not to_user:
            raise ClientError('To User can\'t be None')
        
        if not message:
            raise ClientError('Mention message can\'t be None')

        mention = f'<a href=\"#\" data-vss-mention=\"version:2.0,{to_user.id}\">@{to_user.display_name}</a>: {message}'

        if (from_user) and (from_user.id != to_user.id):
            mention += f'<br>CC: <a href=\"#\" data-vss-mention=\"version:2.0,{from_user.Id}\">@{from_user.DisplayName}</a>'

        try:
            workitem[MentionClient._TFS_HISTORY_FIELD] = mention
            update_result = workitem.update_fields()

            return MentionResult.MENTION_SUCCESS \
                if update_result == UpdateFieldsResult.UPDATE_SUCCESS else MentionResult.MENTION_ERROR
        except:
            return MentionResult.MENTION_EXCEPTION
