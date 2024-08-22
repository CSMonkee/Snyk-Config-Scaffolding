import json
import requests

SNYK_REST_API_BASE_URL="https://api.snyk.io/rest"


# Build the http headers, authorised using the group service account token passed as a command line argument
def build_headers(args):
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'token {args["group_svc_ac_token"]}'
    }
    return headers


# Iterate over your groups and return the id for the required group name
def get_group_id(args):
    url = f'{SNYK_REST_API_BASE_URL}/groups?version={args["api_ver"]}~beta'
    response = requests.request("GET", url, headers=build_headers(args))
    if response.status_code == 200:
        groups = json.loads(response.text)['data']
        for group in groups:
            if group["attributes"]["name"] == args["group_name"]:
                return group["id"]
    return None


# Check if the target organisation name already exists
def check_organization_exists(args, group_id):
    url = f'{SNYK_REST_API_BASE_URL}/groups/{group_id}/orgs?version={args["api_ver"]}'
    response = requests.request("GET", url, headers=build_headers(args))
    if response.status_code == 200:
        orgs = json.loads(response.text)['data']
        for org in orgs:
            if org['attributes']['name'] == args["org_name"]:
                return org['id']
    return None


# Create the service account within the target org and return the auth-key post creation only
def create_service_account(args, org_id, role_id):
    url = f'{SNYK_REST_API_BASE_URL}/orgs/{org_id}/service_accounts?version={args["api_ver"]}'
    payload = {
        "data": {
            "attributes": {
                "auth_type": "api_key",
                "name": "{0}".format(args["org_service_account_name"]),
                "role_id": "{0}".format(role_id)
            },
            "type": "service_account"
        }
    }

    # Make the POST request to create the service account
    response = requests.post(url, json=payload, headers=build_headers(args))

    if response.status_code == 201:
        service_account_data = response.json()
        print('Service account {0} created successfully!'.format(args["org_service_account_name"]))
        return service_account_data["data"]["attributes"]["api_key"]
    else:
        print(f"Failed to create service account {args['org_service_account_name']}: {response.status_code} - {response.text}")
        return None