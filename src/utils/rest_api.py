import json
import requests

SNYK_REST_API_BASE_URL="https://api.snyk.io/rest"

# http header construction
def build_headers(args):
    headers = {
      'Content-Type': 'application/vnd.api+json',
      'Authorization': 'token {0}'.format(args["group_svc_ac_token"])
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


def create_service_account(args, org_id):
    url = f'{SNYK_REST_API_BASE_URL}/org/{org_id}/service_accounts?version={args["api_ver"]}'
    payload = {
        "data": {
            "attributes": {
                "auth_type": "api_key",
                "name": "{0}".format(args["service_account_name"]),
                "role_id": "{0}".format("02f9c335-fed6-4af2-9f08-d1b56995f1c7")
            },
            "type": "service_account"
        }
    }
    #payload = json.dumps(payload)
    response = requests.post(url, json=payload, headers=build_headers(args))

    if response.status_code == 201:
        service_account_data = response.json()
        print('Organisation {0} created successfully!'.format(args["service_account_name"]))
        return service_account_data
    else:
        print(f"Failed to create service account: {response.status_code} - {response.text}")
        return None