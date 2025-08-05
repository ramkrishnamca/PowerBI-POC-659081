import os
import requests
from msal import ConfidentialClientApplication

# Environment variables
TENANT_ID = os.environ['TENANT_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
WORKSPACE_ID = os.environ['WORKSPACE_ID']

# MSAL Setup
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]

app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

token_response = app.acquire_token_for_client(scopes=SCOPE)
access_token = token_response.get('access_token')

if not access_token:
    raise Exception("Token acquisition failed")

# Headers for Power BI API
headers = {
    'Authorization': f'Bearer {access_token}'
}

# PBIX file and dataset name
pbix_path = 'reports/Test.pbix'
dataset_name = 'Test'

# Upload PBIX
try:
    with open(pbix_path, 'rb') as pbix_file:
        print("Uploading PBIX...")
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/imports?datasetDisplayName={dataset_name}&nameConflict=Overwrite"
        response = requests.post(
            url,
            headers=headers,
            files={'file': pbix_file}
        )

        print("Upload Status:", response.status_code)
        try:
            print("Response:", response.json())
        except ValueError:
            print("Non-JSON Response:", response.text)

except FileNotFoundError:
    print(f"Error: PBIX file not found at path '{pbix_path}'")
except Exception as e:
    print("Unexpected error:", str(e))
