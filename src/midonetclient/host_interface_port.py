# Copyright 2012 Midokura Japan KK

from resource_base import ResourceBase
import vendor_media_type

class HostInterfacePort(ResourceBase):

    media_type = vendor_media_type.APPLICATION_HOST_INTERFACE_PORT_JSON

    def __init__(self, http, uri, dto):
        super(HostInterfacePort, self).__init__(http, uri, dto)

    def get_host_id(self):
        return self.dto['hostId']

    def get_interface_name(self):
        return self.dto['interfaceName']

    def get_port_id(self):
        return self.dto['portId']

    def port_id(self, port_id):
        self.dto['portId'] = port_id
        return self

    def interface_name(self, name):
        self.dto['interfaceName'] = name
        return self

