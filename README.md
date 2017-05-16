# Azure Region Core Checker

This cli tests whether or not there are enough cores available in a region (this is for an automated requirement).

## Setup

CentOS requires the following dependencies installed...

```
$ sudo yum install -y git epel-release gcc libffi-devel python-devel openssl-devel
$ sudo yum install -y python-pip
```

Install the azcorecheck tool...

```
$ git clone https://github.com/tstringer/azure-regional-core-checker.git
$ cd azure-regional-core-checker
$ chmod 755 ./install
$ sudo ./install
```

## Environment variables

This cli expects the following environment variables to be defined...

- `ARM_SUBSCRIPTION_ID` - Azure subscription ID
- `ARM_TENANT_ID` - The tenant/directory ID for the service principal
- `ARM_CLIENT_ID` - Client/application ID of the service principal
- `ARM_CLIENT_SECRET` - Secret for the service principal

> :bulb: A service principal can be created with the use of [this guide (Azure documentation)](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal)

## Usage

```
usage: azcorecheck [-h] -l LOCATION -d DESIRED_CORE_COUNT [-p]

optional arguments:
  -h, --help            show this help message and exit
  -l LOCATION, --location LOCATION
                        azure region to check
  -d DESIRED_CORE_COUNT, --desired DESIRED_CORE_COUNT
                        desired core count to check if available
  -p, --permissive      if there is a runtime error exit with a zero code
```
