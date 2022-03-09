# PyTfsClient library (TFS API Python client)

Microsoft Team Foundation Server Python Library is a Microsoft TFS API Python client that can work with Microsoft TFS workitems.

## Installing
Feel free to use command "pip install pytfsclient"

## Basic usage
0. Install pytfsclient package
1. Import package
```python
import pytfsclient
from pytfsclient.tfs_client_factory import TfsClientFactory
```
2. Create and configure Base TFS Client
```python
base_client = TfsClientFactory.create('https://tfs-server/tfs/', 'DefaultCollection/MyProject')
### IF authentificate with PAT
base_client.authentificate_with_pat('<personal access token>')
### OR with user name and password
base_client.authentificate_with_password('username', 'userpassword')
```
3. Get facade your need

    3.1 If you want to manage workitems
    ```python
    client = TfsClientFactory.get_workitem_client(base_client)
    ```
    
    3.2 If you want to manage projects, teams, team members
    ```python
    client = TfsClientFactory.get_project_client(base_client)
    ```
    
4. Manage TFS items

    4.1 Managing workitems
    ```python
    wi = client.get_single_workitem(10500)
    print('Item: Id={}, Title={}, State={}'.format(wi.id, wi.title, wi['System.State']))
    wi['Custom.Field'] = 'Value'
    wi.update()
    print('Item custom field: {}'.format(wi['Custom.Field']))

    workitems = client.get_workitems([1, 2, 3])
    for wi in workitems:
        print('Item: id={}, Title={}'.format(wi.id, wi.title))
    ```

## Docs
TODO: 
