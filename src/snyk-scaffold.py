import argparse
import utils.util_func
import utils.rest_api
import utils.v1_api


# Parse command line arguments that instruct program operation
def get_arguments():
    parser = argparse.ArgumentParser(
        description='This script enables Snyk customers to scaffold configuation for projects from within their \
        CD-CD pipelines')
    parser.add_argument('-g', '--group_name', required=True)
    parser.add_argument('-a', '--group_svc_ac_token', required=True)
    parser.add_argument('-r', '--group_role_name', required=True)
    parser.add_argument('-o', '--org_name', required=True)
    parser.add_argument('-s', '--org_service_account_name', required=True)
    parser.add_argument('-v', '--api_ver', required=True)
    parser.add_argument('-t', '--template_org_id', default=None)
    args = vars(parser.parse_args())
    return args


# Build the named org, service account assigned to the named group role and return the service account auth token upon
# creation only. You must store the key securely within your environment for use by pipelines to commit to the created
# organisation.
def scaffold_snyk_config(args):
    svc_ac_key = None
    group_id = utils.rest_api.get_group_id(args)
    if group_id is not None:
        org_id = utils.rest_api.check_organization_exists(args, group_id)
        role_id = utils.v1_api.get_group_role_id(args, group_id, args["group_role_name"])
        if org_id is None:
            org_id = utils.v1_api.create_organization(args, group_id)
            if org_id is not None:
                svc_ac_key = utils.rest_api.create_service_account(args, org_id, role_id)
        else:
            svc_ac_key = utils.rest_api.create_service_account(args, org_id, role_id)
    return svc_ac_key


# Main function
if __name__ == '__main__':
    args = get_arguments()
    key = scaffold_snyk_config(args)
    exit(key)
