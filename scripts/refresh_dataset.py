
import os
import requests
from msal import ConfidentialClientApplication

TENANT_ID = os.environ['TENANT_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
WORKSPACE_ID = os.environ['WORKSPACE_ID']
DATASET_ID = os.environ['DATASET_ID']

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]

app = ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = app.acquire_token_for_client(scopes=SCOPE)

access_token = token_response.get('access_token')
if not access_token:
    raise Exception("Token acquisition failed")

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

refresh_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/refreshes"
response = requests.post(refresh_url, headers=headers)

print("Refresh Trigger Status:", response.status_code)
print("Response:", response.json())
