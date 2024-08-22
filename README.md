### THIS SOFTWARE IS WORK IN PROGRESS. DO NOT CONSIDER IT COMPLETE UNTIL THIS NOTICE IS REMOVED!

# Snyk-Config-Scaffolding
The utility can be called within CICD pipelines. It enables Snyk customers to scaffold the following configuration 
within the Snyk platform:

- target organisation
- service account with a named group role scope within the created target organisation

These artefacts will only be created if they do not exist. Upon creation of the service account, an auth key for that
account will be returned by way of exit code. This auth key cannot be returned thereafter and so users are reminded to 
store it securely within their environment for subsequent use by their pipeline. Creation of the target organisation and 
associated service account should abstract all repository scans for a given application within your estate. This ensures 
an (Application 1:1 Snyk Organisation) mapping in accordance with recommended best practice.

Customers are advised to build a facade service in front of snyk-scaffold, where the facade will be called directly from 
CICD pipelines. This ensures the Snyk group auth key that is required in order to scaffold Snyk configuration for the 
pipeline will be kept within a restricted environmental context. 


## How to call Snyk-Config-Scaffolding
````
python3 Snyk-Config-Scaffolding/src/snyk-scaffold.py
    --group_name="<snyk-group-name>"
    --org_name="<target-snyk-org-name>" 
    --group_svc_ac_token="<snyk-group-service-account-token-value>" 
    --org_service_account_name="<name>" 
    --group_role_name="<name>"
    --api_ver="<snyk-rest-api-version>"

python3 Snyk-Config-Scaffolding/src/snyk-scaffold.py
    --group_name="kevin.matthews Group"
    --org_name="Kevin-Test2"
    --group_svc_ac_token="<snyk-group-service-account-token-value>"
    --org_service_account_name="CICD"
    --group_role_name="CICD"
    --api_ver="2024-08-15"
````

### Note:
At the time of writing, I am required to use a mix of GA and beta REST APIs. As the beta APIs become GA, so I will 
update this software.

I have yet to add pagination at this time.