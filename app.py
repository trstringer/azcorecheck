"""Compare current used cores in region to requested cores"""
import argparse
from collections import namedtuple
import os
import sys
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.common.exceptions import CloudError

AzureCredential = namedtuple(
    'AzureCredential',
    ['client_id', 'secret', 'tenant', 'subscription_id']
)

def azure_creds():
    """Return a dictionary of azure credentials"""

    return {
        'subscription_id': os.environ['ARM_SUBSCRIPTION_ID'],
        'tenant': os.environ['ARM_TENANT_ID'],
        'client_id': os.environ['ARM_CLIENT_ID'],
        'secret': os.environ['ARM_CLIENT_SECRET']
    }

def parse_args():
    """Parse the cli arguments"""

    parser = argparse.ArgumentParser(prog='azcorecheck')
    parser.add_argument(
        '-l', '--location',
        required=True,
        help='azure region to check'
    )
    parser.add_argument(
        '-d', '--desired',
        type=int,
        required=True,
        metavar='DESIRED_CORE_COUNT',
        help='desired core count to check if available'
    )
    parser.add_argument(
        '-p', '--permissive',
        action='store_true',
        help='if there is a runtime error exit with a zero code'
    )
    return parser.parse_args()

def has_enough_cores(azure_credentials, location, desired_core_count=1, verbose=False):
    """Test if a region has enough cores"""

    client = ComputeManagementClient(
        credentials=ServicePrincipalCredentials(
            client_id=azure_credentials.client_id,
            secret=azure_credentials.secret,
            tenant=azure_credentials.tenant
        ),
        subscription_id=azure_credentials.subscription_id
    )

    total_regional_cores = [
        _ for _ in client.usage.list(location)
        if 'Total Regional Cores' in _.name.localized_value
    ][0]

    if verbose:
        print(
            str(total_regional_cores.name.localized_value) + ' ' +
            str(total_regional_cores.current_value) + ' of ' +
            str(total_regional_cores.limit)
        )
        print('Requesting ' + str(desired_core_count) + ' core(s)')

    return desired_core_count <= total_regional_cores.limit - total_regional_cores.current_value

def main():
    """Main script execution"""

    cli_args = parse_args()

    try:
        creds = AzureCredential(
            client_id=os.environ['ARM_CLIENT_ID'],
            secret=os.environ['ARM_CLIENT_SECRET'],
            tenant=os.environ['ARM_TENANT_ID'],
            subscription_id=os.environ['ARM_SUBSCRIPTION_ID']
        )
        enough_cores = has_enough_cores(creds, cli_args.location, cli_args.desired, verbose=True)
        print('Desired core count is available' if enough_cores else 'Desired core count is unavailable')
    except KeyError as key_err:
        print('KeyError ' + key_err.message)
        sys.exit(0 if cli_args.permissive else 1)
    except IndexError as idx_err:
        print('IndexError ' + idx_err.message)
        sys.exit(0 if cli_args.permissive else 1)
    except CloudError:
        print('Unable to connect to the Azure subscription')
        sys.exit(0 if cli_args.permissive else 1)

    sys.exit(0 if enough_cores else 1)

if __name__ == '__main__':
    main()
