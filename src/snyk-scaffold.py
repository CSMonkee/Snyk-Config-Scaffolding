import argparse
import utils.util_func
import utils.rest_api

def get_arguments():
    parser = argparse.ArgumentParser(description='This script enables Snyk customers to scaffold configuation for projects from within their CD-CD pipelines')
    parser.add_argument('-g', '--group_name', required=True)
    parser.add_argument('-o', '--org_name', required=True)
    parser.add_argument('-s', '--group_svc_ac_token', required=True)
    parser.add_argument('-v', '--api_ver', required=True)

    args = vars(parser.parse_args())
    return args


def scaffold_snyk_config(args):

    groupId = utils.rest_api.get_group_id(args)
    if groupId != None:
        orgId = utils.rest_api.check_organization_exists(args, groupId)
        if orgId == None:
            orgId = utils.rest_api.create_organization(args["org_name"], groupId)
        if orgId != None:
            org_svc_ac_token = utils.rest_api.get_snyk_service_account_token(args, orgId)
            if org_svc_ac_token == None:
                svc_ac = utils.rest_api.create_service_account(args)
                x=0



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    args = get_arguments()
    scaffold_snyk_config(args)

