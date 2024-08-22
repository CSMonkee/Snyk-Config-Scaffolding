import json
from urllib.request import urlopen
import requests

SNYK_V1_API_BASE_URL="https://api.snyk.io/v1"

def build_headers(args):
    headers = {
      'Content-Type': 'application/json',
      'Authorization': '{0}'.format(args["group_svc_ac_token"])
    }
    return headers


def create_organization(args, groupId):
    url = f'{SNYK_V1_API_BASE_URL}/org'
    payload = {'name': '{0}'.format(args["org_name"]), 'groupId': '{0}'.format(groupId)}
    payload = json.dumps(payload)
    response = requests.post(url, headers=build_headers(args), data=payload)

    if response.status_code == 201:
        org = response.json()
        print('Organisation {0} created successfully!'.format(args["org_name"]))
        return org["id"]
    else:
        print(f"Failed to create organisation: {response.status_code} - {response.text}")
        return None



def get_group_role(args, groupId, rolename):
    url = f'{SNYK_V1_API_BASE_URL}/group/{groupId}/roles'
    response = requests.get(url, headers=build_headers(args))

    for role in json.loads(response.text):
        if role["name"] == rolename:
            return role["publicId"]
    print(f"Unable to find role {rolename} : {response.status_code} - {response.text}")
    return None
