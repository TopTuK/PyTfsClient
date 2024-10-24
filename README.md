# TESTS
[![Run tests](https://github.com/TopTuK/PyTfsClient/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/TopTuK/PyTfsClient/actions/workflows/tests.yaml)

# PyTfsClient library (TFS API Python client)

Microsoft Team Foundation Server Python Library is a Microsoft TFS API Python client that can work with Microsoft TFS.

## Installing
Feel free to use command "pip install pytfsclient"

## Basic usage
0. Install pytfsclient package
1. Import package
```python
import pytfsclient
from pytfsclient.client_factory import ClientFactory
```
2. Create and configure Base TFS Client
```python
### IF authentificate with PAT
client_connection = ClientFactory.create_pat('<personal access token>', 'https://tfs-server/tfs/', 'DefaultCollection/MyProject')
### OR with user name and password
client_connection = ClientFactory.create_ntlm('username', 'userpassword', 'https://tfs-server/tfs/', 'DefaultCollection/MyProject')
```
3. Get facade your need

    3.1 If you want to manage workitems
    ```python
    workitem_client = ClientFactory.get_workitem_client(client_connection)
    ```
    
    3.2 If you want to manage projects, teams, team members
    ```python
    project_client = ClientFactory.get_project_client(client_connection)
    ```
    
4. Manage TFS items

    4.1 Get workitems properties
    ```python
    wi = workitem_client.get_single_workitem(100500)
    print('Item: Id={}, Title={}, State={}'.format(wi.id, wi.title, wi['System.State']))
    wi['Custom.Field'] = 'Value'
    wi.update_fields()
    print('Item custom field: {}'.format(wi['Custom.Field']))

    workitems = workitem_client.get_workitems([1, 2, 3])
    for wi in workitems:
        print('Item: id={}, Title={}'.format(wi.id, wi.title))
    ```

    4.2 Create workitem in current project
    ```python
    wi_type_name = 'Requirement'
    wi_title = f'New requirement'
    wi_description = f'This BRQ was created by PyTfsClient'

    wi_fields = {
        'System.Title': wi_title,
        'System.Description': wi_description,
    }

    # Create workitem
    wi = workitem_client.create_workitem(wi_type_name, wi_fields)
    ```

    4.3 Create workitem in another project
    ```python
    wi_project = f'AnotherProject'

    wi_type_name = 'User Story'
    wi_title = f'New user story'
    wi_description = f'This User Story was created by PyTfsClient'

    wi_fields = {
        'System.Title': wi_title,
        'System.Description': wi_description,
    }

    # Create workitem
    wi = workitem_client.create_workitem(type_name=wi_type_name, item_fields=wi_fields, project=wi_project)
    ```

# Coding style
https://google.github.io/styleguide/pyguide.html

# Additional API
- It can send mentions to another user (see MentionClient::send_mention)
- It can get project identities (groups, teams, etc.) without Graph API.