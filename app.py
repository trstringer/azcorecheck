"""Compare current used cores in region to requested cores"""
import os
import sys
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials

def azure_creds():
    """Return a dictionary of azure credentials"""

    return {
        'subscription_id': os.environ['ARM_SUBSCRIPTION_ID'],
        'tenant': os.environ['ARM_TENANT_ID'],
        'client_id': os.environ['ARM_CLIENT_ID'],
        'secret': os.environ['ARM_CLIENT_SECRET']
    }

def main():
    creds_temp = azure_creds()
    creds = ServicePrincipalCredentials(
        client_id=creds_temp['client_id'],
        secret=creds_temp['secret'],
        tenant=creds_temp['tenant']
    )
    client = ComputeManagementClient(
        credentials=creds,
        subscription_id=creds_temp['subscription_id']
    )

    try:
        total_regional_cores = [_ for _ in client.usage.list('eastus') if 'Total Regional Cores' in _.name.localized_value][0]
    except IndexError:
        print('unable to retrieve total regional cores')
        sys.exit(1)

    print(
        str(total_regional_cores.name.localized_value) + ' ' +
        str(total_regional_cores.current_value) + ' of ' +
        str(total_regional_cores.limit)
    )

if __name__ == '__main__':
    main()
