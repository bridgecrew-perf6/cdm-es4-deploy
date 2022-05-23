## EC2 CDM ES4

This repo will generate the Terraform configuration needed to provision EC2 CDM ES4 resources.

***

### To Deploy CDM run the two following commands.

1. From scripts directory.  This generates the UUID file and seeds the database
```
   python3 crms-cdm-allocation.py '{"uuid_idx" : 100, "instructor_ids" : 5, "run" : "provision_all"}'
```

2. From base project directory.  This generates the Terraform and runs the apply command.
```
./provision.sh 
3 args are required
arg 1: provision environment (dev|stage|prod)
arg 2: terraform function (apply|plan|show|destroy)
arg 3: region (gov-west|gov-east)

real	0m0.002s
user	0m0.000s
sys	0m0.001s

Example:
./provision prod apply gov-west

```

To destroy the provisioned CDM, run the following.
`./provision prod destroy gov-west`

***

### The Project files.

Wrapper bash script to execute the provision-cdm bash script.

- [provision.sh](provision.sh)

Main bash script that calls helper scripts for building the Terraform and Nginx configs.  This script also provisions the Terraform.

- [provision-cdm.sh](./scripts/provision-cdm.sh)

Python Script for generating the EC2 CDM Terraform configuration, this is called by the provision-cdm script

- [genEC2CDM.py](./scripts/genEC2CDM.py)

Terraform template file that represents the header of the Terraform configuration.

- [ec2-tf-cdm-template-header.txt](./template/ec2-tf-cdm-template-header.txt)

Terraform template file that represents the body of the Terraform configuration.

- [ec2-tf-cdm-template.txt](./template/ec2-tf-cdm-template.txt)

CRMS CDM Allocation Python script - This is a temporary add-hoc script.

- [crms-cdm-allocation.py](./scripts/crms-cdm-allocation.py) - Python script.
- gen_uid() - This function generates the [new-uid.txt](./scripts/new-uid.txt) text file.
- delete_cdm_resources() - This function deletes the records from the CDM allocation tables.
- provision_cdm_resources() - This function provisions the CDM allocation tables. 

Bash Script for generating the following text files ,this is called the provision-cdm script.

- [buildUidIpMap.sh](./scripts/buildUidIpMap.sh) - Bash script.
- [ips-http-output.txt](./scripts/output/ips-http-output.txt) - Text file that lists the CDM URLS.
- [ips-nginx.txt](./scripts/output/ips-nginx.txt) - Text file for the Nginx configuration.




