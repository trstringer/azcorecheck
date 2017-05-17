"""Compare current used cores in region to requested cores"""
import argparse
import os
import sys
from azurecredentials import AzureCredential
from corecheck import has_enough_cores

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
