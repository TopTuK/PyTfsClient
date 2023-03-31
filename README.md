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
client_connection = ClientFactory.create_pat('username', 'userpassword', 'https://tfs-server/tfs/', 'DefaultCollection/MyProject')
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

    4.1 Managing workitems
    ```python
    wi = workitem_client.get_single_workitem(100500)
    print('Item: Id={}, Title={}, State={}'.format(wi.id, wi.title, wi['System.State']))
    wi['Custom.Field'] = 'Value'
    wi.update_fields()
    print('Item custom field: {}'.format(wi['Custom.Field']))

    workitems = client.get_workitems([1, 2, 3])
    for wi in workitems:
        print('Item: id={}, Title={}'.format(wi.id, wi.title))
    ```
