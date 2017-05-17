"""Logic to do core check in Azure"""
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials

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
