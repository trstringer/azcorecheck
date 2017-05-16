"""Compare current used cores in region to requested cores"""
import argparse
import os
import sys
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.common.exceptions import CloudError

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

    parser = argparse.ArgumentParser()
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

def main():
    """Main script execution"""

    cli_args = parse_args()

    try:
        creds_raw = azure_creds()
        creds = ServicePrincipalCredentials(
            client_id=creds_raw['client_id'],
            secret=creds_raw['secret'],
            tenant=creds_raw['tenant']
        )
        client = ComputeManagementClient(
            credentials=creds,
            subscription_id=creds_raw['subscription_id']
        )
    except KeyError:
        print('Error while reading environment variable')
        sys.exit(0 if cli_args.permissive else 1)
    except CloudError:
        print('Unable to connect to the Azure subscription')
        sys.exit(0 if cli_args.permissive else 1)

    try:
        total_regional_cores = [
            _ for _ in client.usage.list('eastus')
            if 'Total Regional Cores' in _.name.localized_value
        ][0]
    except IndexError:
        print('unable to retrieve total regional cores')
        sys.exit(0 if cli_args.permissive else 1)

    print(
        str(total_regional_cores.name.localized_value) + ' ' +
        str(total_regional_cores.current_value) + ' of ' +
        str(total_regional_cores.limit)
    )

    print('Desiring ' + str(cli_args.desired) + ' cores')
    # pylint: disable=line-too-long
    enough_cores = cli_args.desired + total_regional_cores.current_value <= total_regional_cores.limit
    print('Provisioning will succeed :: ' + str(enough_cores))

    sys.exit(0 if enough_cores else 1)

if __name__ == '__main__':
    main()
