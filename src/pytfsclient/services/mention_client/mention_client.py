from enum import Enum
from ...models.workitems.tfs_workitem import UpdateFieldsResult, Workitem
from ...models.project.tfs_team_member import TfsTeamMember

class MentionResult(Enum):
    MENTION_SUCCESS = 0
    MENTION_ERROR = 1
    MENTION_EXCEPTION = 2

class MentionClient:
    """
    TFS Mention client for mention users
    """

    _TFS_HISTORY_FIELD = 'System.History'
    
    @staticmethod
    def send_mention(self, workitem: Workitem, to_user: TfsTeamMember, \
                    message: str, from_user: TfsTeamMember = None) -> MentionResult:
        """
        Sends mention to user. Writes mention to History of workitem
        WARNING: this function uses non-public API
        """

        assert workitem, 'workitem can\'t be None'
        assert to_user, 'To User can\'t be None'
        assert message, 'Mention message can\'t be None'

        mention = f'<a href=\"#\" data-vss-mention=\"version:2.0,{to_user.id}\">@{to_user.display_name}</a>: {message}'

        if (from_user) and (from_user.id != to_user.id):
            mention += f'<br>CC: <a href=\"#\" data-vss-mention=\"version:2.0,{from_user.Id}\">@{from_user.DisplayName}</a>'

        try:
            workitem[self._TFS_HISTORY_FIELD] = mention
            update_result = workitem.update_fields()

            return MentionResult.MENTION_SUCCESS \
                if update_result == UpdateFieldsResult.UPDATE_SUCCESS else MentionResult.MENTION_ERROR
        except:
            return MentionResult.MENTION_EXCEPTION
