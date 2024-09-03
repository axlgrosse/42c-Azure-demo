#!/usr/bin/env python3

import json
import argparse
import requests
import sys
import random
import subprocess #For AzureDevOps Integration

# This calls the scand-manager API to start a scan job
def start_job (scanToken: str, targetAPIHost: str, targetAPIToken: str, job_id: int):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    
    job_name = "scand-"+str(job_id)+"-v2"

    if not targetAPIToken:
        # If the target API authentication is provided in the scan configuration, no need to pass it here
        payload = {
            f"token": scanToken, 
            "name": job_name, 
            "expirationTime": 600, 
            "platformService": PLATFORM_SERVICE, 
            "scandImage": "42crunch/scand-agent:v2", 
            "env": {
                "SCAN42C_HOST": targetAPIHost
                }
            }
    else:
        # If the target API authentication token was provided, pass it to the scan job as env var SCAN42C_SECURITY_ACCESS_TOKEN (variable name will depend on the scan configuration)
        payload = {
            f"token": scanToken, 
            "name": job_name, 
            "expirationTime": 600, 
            "platformService": PLATFORM_SERVICE, 
            "scandImage": 
            "42crunch/scand-agent:v2", 
            "env": {
                "SCAN42C_HOST": targetAPIHost, 
                "SCAN42C_SECURITY_ACCESS_TOKEN": targetAPIToken
                }
            }

    response = requests.post(SCAND_MANAGER_URL, data=json.dumps(payload), headers=headers)

    return response.json()

def main():

    global SCAND_MANAGER_URL, PLATFORM_SERVICE

    parser = argparse.ArgumentParser(
        description='42Crunch Scan Jobs Manager'
    )
    parser.add_argument('-s', "--scan-token",
                        required=True,
                        help="42Crunch Scan Token")
    parser.add_argument('-t', "--target-api-host",
                        required=True,
                        help="Target API Host")
    parser.add_argument('-a', "--api-auth-token",
                        required=False,
                        help="Target API Authentication Token")
    parser.add_argument('-j', "--job-id",
                        required=True,
                        type=int,
                        help="Job ID")
    parsed_cli = parser.parse_args()

    SCAND_MANAGER_URL = "https://photo-demo.westeurope.cloudapp.azure.com/scand/api/job"
    PLATFORM_SERVICE = "services.42crunch.com:8001"

    scan_token = parsed_cli.scan_token
    target_api_host = parsed_cli.target_api_host
    api_auth_token = parsed_cli.api_auth_token
    job_id = parsed_cli.job_id

    scan_job = start_job (scan_token, target_api_host, api_auth_token, job_id)

    # Uncomment this for integration with Azure DevOps (DEPRECATED)
    # subprocess.Popen(["echo", "##vso[task.setvariable variable=SCANV2_JOB_ID;isoutput=true]{0}".format(scan_job.get("name"))])

    print (scan_job)

# -------------- Main Section ----------------------
if __name__ == '__main__':
    main()