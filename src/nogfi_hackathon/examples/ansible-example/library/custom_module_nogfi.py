#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
import ipaddress
__metaclass__ = type

DOCUMENTATION = r'''
---
module: custom_module_nog.fi

short_description: This is a test custom module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This custom module takes prefix and integer as input and returns the IP address from the index stated by ip_offset

options:
    prefix:
        description: IPv4/6 prefix
        required: true
        type: str
    ip_offset:
        description: this integer indicates the index of returned IP address
        required: trye
        type: int

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  custom_module_nogfi::
    prefix: 1.1.1.0/24
    ip_offset: 5
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: IP4/6 prefix
    type: str
    returned: always
    sample: '1.1.1.0/24'
message:
    description: IP address returned
    type: str
    returned: always
    sample: '1.1.1.5'
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        prefix=dict(type='str', required=True),
        ip_offset=dict(type='int', required=True)
        # new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        ip = "",
        prefix = "",
        changed = True
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    result["prefix"] = module.params['prefix']
    result["ip"] = str(ipaddress.ip_network(module.params['prefix'])[5])


    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()