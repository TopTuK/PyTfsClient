from pytfsclient.tfs_client_factory import TfsClientFactory
from pytfsclient.tfs_workitem_client import TfsWorkitemClient
from pytfsclient.tfs_workitem_model import TfsWorkitem

print('Hello to Release Scope Checker')

# https://hqrndtfs.avp.ru/tfs/web/qr.aspx?pguid=e29440ef-c152-4668-bb06-8d2619f61c08&qid=1b9e52c7-ad9d-4027-b9b9-4a89ea8edfd9
query_id = '1b9e52c7-ad9d-4027-b9b9-4a89ea8edfd9'

base_client = TfsClientFactory.create('https://dit-tfs/tfs', 'DefaultCollection/KAVKIS')
base_client.authentificate_with_password('KL\\Sidorov_S', 'nbgf-gfCC43')

client = TfsClientFactory.get_workitem_client(base_client)

def check_legal_status(wi: TfsWorkitem) -> None:
    legal_status = wi['KL.LegalStatus']
    if legal_status not in ['Not required', 'Manually Approved', 'IPMS: Approved', 'IPMS: Approved with comments']:
        print('{} {} {}'.format(wi.id, wi.title, legal_status))

def check_patent_status(wi: TfsWorkitem) -> None:
    patent_status = wi['KL.PatentsCheckStatus']

    if patent_status not in ['Not required', 'IPMS: Not Required', 'Manually Approved']:
        print('{} {} {}'.format(wi.id, wi.title, patent_status))

try:
    query_result = client.run_saved_query(query_id=query_id)
    
    if (not query_result) or (query_result.is_empty):
        print('Query is empty')
        exit()

    for wi in query_result.workitems:
        if '[BRQ][Win] Localization' in wi.title:
            continue

        if '[BRQ][Win] Customization' in wi.title:
            continue
        
        decomposition_done = bool(wi['KL.DecompositionDone'])
        if decomposition_done:
            #check_legal_status(wi)

            check_patent_status(wi)
            #patent_status = wi['']
            #print('{} {}'.format(wi.id, wi.title))

except:
    print('EXCEPTION')

print('Meow!')