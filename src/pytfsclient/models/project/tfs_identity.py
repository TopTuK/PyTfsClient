from ..client_error import ClientError

class Identity:
    '''
    Identity model class contains infromation about TFS/Azure group of project
    '''

    @property
    def is_user(self) -> bool:
        '''
        Returns:
            True if identity is user
        '''
        return self.identity_type == 'user'

    @property
    def is_group(self) -> bool:
        '''
        Returns:
            True if identity is group
        '''
        return self.identity_type == 'group'
    
    @property
    def is_team(self) -> bool:
        '''
        Returns:
            True if identity is team
        '''
        return self.identity_type == 'team'

    @property
    def identity_type(self) -> str:
        '''
        Returns:
            Identity type
        '''
        return self.__identity_type
    
    @property
    def friendly_name(self) -> str:
        '''
        Returns:
            Friendly display name of Identity
        '''
        return self.__friendly_name
    
    @property
    def display_name(self) -> str:
        '''
        Returns:
            Display name of Identity
        '''
        return self.__display_name
    
    @property
    def foundation_id(self) -> str:
        '''
        Returns:
            Team Foundation Id of Identity
        '''
        return self.__foundation_id
    
    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates instance of Identity class from given json object

        Args:
            json_item (object): JSON object with attributes.

        Returns:
            Instance of Identity class
        '''

        group = cls()

        try:
            group.__foundation_id = json_item['TeamFoundationId']

            group.__identity_type = json_item['IdentityType'] if 'IdentityType' in json_item else 'Unknown'
            group.__display_name = json_item['DisplayName'] if 'DisplayName' in json_item else ''
            group.__friendly_name = json_item['FriendlyDisplayName'] if 'FriendlyDisplayName' in json_item else ''

            return group
        except Exception as ex:
            raise ClientError(ex)