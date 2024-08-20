import json
import requests

SNYK_REST_API_BASE_URL="https://api.snyk.io/rest"

# http header construction
def build_headers(args):
    headers = {
      'Content-Type': 'application/vnd.api+json',
      'Authorization': '{0}'.format(args["group_svc_ac_token"])
    }
    return headers


def get_group_id(args):
    url = f'{SNYK_REST_API_BASE_URL}/groups?version={args["api_ver"]}~beta'
    response = requests.request("GET", url, headers=build_headers(args))
    if response.status_code == 200:
        groups = json.loads(response.text)['data']
        for group in groups:
            if group["attributes"]["name"] == args["group_name"]:
                return group["id"]
    return None


def group_orgs(args, groupId, pagination):
    if pagination is None:
        url = 'https://api.snyk.io/rest/groups/{0}/orgs?version={1}~beta'.format(groupId, args["api_ver"])
    else:
        url = 'https://api.snyk.io/rest/groups/{0}/orgs?version={1}&starting_after={2}'.format(groupId, args["api_ver"],
                                                                                               pagination)
    response = requests.request("GET", url, headers=build_headers(args))
    return response.text


def check_organization_exists(args, group_id):
    url = f'{SNYK_REST_API_BASE_URL}/groups/{group_id}/orgs?version={args["api_ver"]}'
    response = requests.request("GET", url, headers=build_headers(args))
    if response.status_code == 200:
        orgs = json.loads(response.text)['data']
        #orgs = response.json().get('orgs', [])
        for org in orgs:
            if org['attributes']['name'] == args["org_name"]:
                return org['id']
    return None


def get_snyk_service_account_token(args, org_id):

    # Endpoint to list service accounts in the group
    url = f'{SNYK_REST_API_BASE_URL}//orgs/{org_id}/service_accounts?version={args["api_ver"]}'
    response = requests.request("GET", url, headers=build_headers(args))
    #response = requests.get(f'{SNYK_REST_API_BASE_URL}/orgs/{org_id}/service_accounts', headers=build_headers(args))

    if response.status_code == 200:
        service_accounts = json.loads(response.text)['data']

        # Find the service account by name
        for account in service_accounts:
            if account['attributes']['name'] == "CICD":
                # Assuming the token is stored within the account details
                return account.get('token', None)

        # If the account is not found, return None
        return None
    else:
        # Handle errors
        print(f"Failed to retrieve service accounts: {response.status_code}, {response.text}")
        return None



def create_organization(org_name, group_id=None):
    url = f'{SNYK_REST_API_BASE_URL}/orgs'

    payload = {
        'name': org_name,
    }

    if group_id:
        payload['groupId'] = group_id

    response = requests.post(url, headers=build_headers(), json=payload)

    if response.status_code == 200:
        org_data = response.json()
        print(f"Organization '{org_name}' created successfully!")
        return org_data["id"]
    else:
        print(f"Failed to create organization: {response.status_code} - {response.text}")
        return None



def create_service_account(args):
    url = f'{SNYK_REST_API_BASE_URL}/org/{args["org_id"]}/service_accounts'

    payload = {
        'name': "CICD",
        'scopes': ['org.read', 'org.write', 'project.read', 'project.write'],  # Example scopes
    }

    response = requests.post(url, headers=build_headers(args), json=payload)

    if response.status_code == 200:
        service_account_data = response.json()
        print(f"Service account 'CICD' created successfully!")
        return service_account_data
    else:
        print(f"Failed to create service account: {response.status_code} - {response.text}")
        return None
