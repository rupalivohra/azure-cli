import argparse
import getpass

from azure.mgmt.compute.models import VirtualHardDisk

from azure.cli.commands import (COMMON_PARAMETERS as GLOBAL_COMMON_PARAMETERS, extend_parameter,
                                patch_aliases)
from azure.cli.command_modules.vm._validators import MinMaxValue
from azure.cli.command_modules.vm._actions import (VMImageFieldAction,
                                                   VMSSHFieldAction,
                                                   VMDNSNameAction,
                                                   load_images_from_aliases_doc,
                                                   get_subscription_locations)
from azure.cli._locale import L

# BASIC PARAMETER CONFIGURATION

PARAMETER_ALIASES = patch_aliases(GLOBAL_COMMON_PARAMETERS, {
    'diskname': {
        'name': '--name -n',
        'help': L('Disk name'),
    },
    'disksize': {
        'name': '--disksize',
        'help': L('Size of disk (Gb)'),
        'type': MinMaxValue(1, 1023),
        'default': 1023
    },
    'image_location': {
        'name': '--image-location',
        'help': L('Image location')
    },
    'lun': {
        'name': '--lun',
        'help': L('0-based logical unit number (LUN). Max value depends on the Virtual ' + \
                  'Machine size'),
        'type': int,
    },
    'vhd': {
        'name': '--vhd',
        'type': VirtualHardDisk
    },
    'vm_name': {
        'name': '--vm-name',
        'dest': 'vm_name',
        'help': 'Name of Virtual Machine to update',
    }
})

def get_location_completion_list(prefix, **kwargs):#pylint: disable=unused-argument
    result = get_subscription_locations()
    return [l.name for l in result]

def get_urn_aliases_completion_list(prefix, **kwargs):#pylint: disable=unused-argument
    images = load_images_from_aliases_doc()
    return [i['urn alias'] for i in images]

VM_CREATE_PARAMETER_ALIASES = {
    'location': {
        'completer': get_location_completion_list
    },
    'name': {
        'name': '--name -n'
    },
    'os_disk_uri': {
        'name': '--os-disk-uri',
        'help': argparse.SUPPRESS
    },
    'os_offer': {
        'name': '--os_offer',
        'help': argparse.SUPPRESS
    },
    'os_publisher': {
        'name': '--os-publisher',
        'help': argparse.SUPPRESS
    },
    'os_sku': {
        'name': '--os-sku',
        'help': argparse.SUPPRESS
    },
    'os_type': {
        'name': '--os-type',
        'help': argparse.SUPPRESS
    },
    'os_version': {
        'name': '--os-version',
        'help': argparse.SUPPRESS
    },
    'admin_username': {
        'name': '--admin-username',
        'default': getpass.getuser(),
        'help': 'Admin login.  Defaults to current username.'
    },
    'ssh_key_value': {
        'name': '--ssh-key-value',
        'action': VMSSHFieldAction
    },
    'dns_name_for_public_ip': {
        'name': '--dns-name-for-public-ip',
        'action': VMDNSNameAction
    },
    'dns_name_type': {
        'name': '--dns-name-type',
        'help': argparse.SUPPRESS
    },
    'authentication_type': {
        'name': '--authentication-type',
        'choices': ['ssh', 'password'],
        'default': 'password'
    },
    'availability_set_type': {
        'name': '--availability-set-type',
        'choices': ['none', 'existing'],
        'default': 'none'
    },
    'private_ip_address_allocation': {
        'name': '--private-ip-address-allocation',
        'choices': ['Dynamic', 'Static'],
        'default': 'Dynamic'
    },
    'public_ip_address_allocation': {
        'name': '--public-ip-address-allocation',
        'choices': ['Dynamic', 'Static'],
        'default': 'Dynamic'
    },
    'public_ip_address_type': {
        'name': '--public-ip-address-type',
        'choices': ['none', 'new', 'existing'],
        'default': 'new'
    },
    'storage_account_type': {
        'name': '--storage-account-type',
        'choices': ['new', 'existing'],
        'default': 'new'
    },
    'virtual_network_type': {
        'name': '--virtual-network-type',
        'choices': ['new', 'existing'],
        'default': 'new'
    }
}

# EXTRA PARAMETER SETS

VM_CREATE_EXTRA_PARAMETERS = {
    'image': {
        'name': '--image',
        'action': VMImageFieldAction,
        'completer': get_urn_aliases_completion_list
        },
}

VM_PATCH_EXTRA_PARAMETERS = {
    'resource_group_name':
        extend_parameter(PARAMETER_ALIASES['resource_group_name'], required=True,
                         dest='resource_group_name'),
    'vm_name':
        extend_parameter(PARAMETER_ALIASES['vm_name'], required=True)
}