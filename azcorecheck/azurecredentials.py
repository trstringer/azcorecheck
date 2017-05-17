"""Credential class to store auth data"""
from collections import namedtuple

AzureCredential = namedtuple(
    'AzureCredential',
    ['client_id', 'secret', 'tenant', 'subscription_id']
)
