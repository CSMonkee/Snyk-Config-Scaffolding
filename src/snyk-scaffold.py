import argparse
import utils.util_func
import utils.rest_api
import utils.v1_api

def get_arguments():
    parser = argparse.ArgumentParser(description='This script enables Snyk customers to scaffold configuation for projects from within their CD-CD pipelines')
    parser.add_argument('-g', '--group_name', required=True)
    parser.add_argument('-o', '--org_name', required=True)
    parser.add_argument('-a', '--group_svc_ac_token', required=True)
    parser.add_argument('-r', '--group_role_name', required=True)
    parser.add_argument('-s', '--service_account_name', required=True)
    parser.add_argument('-v', '--api_ver', required=True)

    args = vars(parser.parse_args())
    return args


def scaffold_snyk_config(args):
    groupId = utils.rest_api.get_group_id(args)
    if groupId != None:
        org_id = utils.rest_api.check_organization_exists(args, groupId)
        role_id = utils.v1_api.get_group_role(args, groupId, args["group_role_name"])
        if org_id == None:
            org_id = utils.v1_api.create_organization(args, groupId, role_id)
            if org_id != None:
                svc_ac = utils.rest_api.create_service_account(args, org_id)
        else:
            svc_ac_key = utils.rest_api.create_service_account(args, org_id, role_id)
            return svc_ac_key



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    args = get_arguments()
    scaffold_snyk_config(args)

