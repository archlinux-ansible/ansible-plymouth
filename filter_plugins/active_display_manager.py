from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  filter: active_display_manager
  author: Alex Wicks <alex@awicks.io>
  short_description: Return currently active display manager
  description:
    - This filter will find the currently active display manager.
    - The value from ansible_facts.services, from the service_facts module should be provided as input.
"""
from ansible import errors
from ansible.module_utils.common._collections_compat import MutableMapping

class FilterModule(object):
    def filters(self):
        return {
            "active_display_manager": self.active_display_manager,
        }
    def contains_key_and_enabled(self, _element: tuple):
        display_managers = [
            "gdm", "gdm-plymouth",
            "sddm", "sddm-plymouth",
            "lightdm", "lightdm-plymouth",
            "lxdm", "lxdm-plymouth",
        ]
        name, data = _element
        if name.split(".")[0] not in display_managers:
            return (None, None)
        return (
            name.split(".")[0],
            data["status"] == "enabled",
        )
    """
    Takes ansible_facts.services as input
    Outputs currently active display manager
    """
    def active_display_manager(self, services):
        if not isinstance(services, MutableMapping):
            raise errors.AnsibleFilterError("Expected dictionary")
        return list(set([
            k.split("-")[0] for k, v in dict(map(
                self.contains_key_and_enabled,
                services.items(),
            )).items() if v is True
        ]))[0]
