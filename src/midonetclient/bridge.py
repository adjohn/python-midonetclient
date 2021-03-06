# Copyright 2012 Midokura Japan KK

from resource_base import ResourceBase
from bridge_port import BridgePort
from router_port import RouterPort
from dhcp_subnet import DhcpSubnet

import port_type
import vendor_media_type


class Bridge(ResourceBase):

    media_type = vendor_media_type.APPLICATION_BRIDGE_JSON

    def __init__(self, http, uri, dto):
        super(Bridge, self).__init__(http, uri, dto)

    def get_name(self):
        return self.dto['name']

    def get_id(self):
        return self.dto['id']

    def get_tenant_id(self):
        return self.dto['tenantId']

    def get_inbound_filter_id(self):
        return self.dto['inboundFilterId']

    def get_outbound_filter_id(self):
        return self.dto['outboundFilterId']

    def name(self, name):
        self.dto['name'] = name
        return self

    def tenant_id(self, tenant_id):
        self.dto['tenantId'] = tenant_id
        return self

    def inbound_filter_id(self, id_) :
        self.dto['inboundFilterId'] = id_
        return self

    def outbound_filter_id(self, id_) :
        self.dto['outboundFilterId'] = id_
        return self

    def get_ports(self, query={}):
        headers = {'Content-Type':
                       vendor_media_type.APPLICATION_PORT_COLLECTION_JSON}
        return self.get_children(self.dto['ports'], query, headers, BridgePort)

    def get_peer_ports(self, query={}):
        headers = {'Content-Type':
                       vendor_media_type.APPLICATION_PORT_COLLECTION_JSON}
        res, peer_ports =  self.web_resource.get(self.dto['peerPorts'],
                                                 headers, query)

        res = []
        for pp in peer_ports:
            if pp['type'] == port_type.INTERIOR_ROUTER:
                res.append(RouterPort(self.web_resource, self.dto['ports'], pp))
            elif pp['type'] == port_type.INTERIOR_BRIDGE:
                res.append(BridgePort(self.web_resource, self.dto['ports'], pp))
        return res

    def get_dhcp_subnets(self):
        query = {}
        headers = {
            'Content-Type':
                vendor_media_type.APPLICATION_DHCP_SUBNET_COLLECTION_JSON
            }
        return self.get_children(self.dto['dhcpSubnets'], query, headers,
                                 DhcpSubnet)

    def get_dhcp_subnet(self, subnet_str):
        """
        given the subnet_str (x.x.x.x_y, address_length), returns DhcpSubnet
        resource that has subnet prefix and length found in the subnet_str.
        """
        prefix, length = subnet_str.split('_')
        for ds in self.get_dhcp_subnets():
            if ds.get_subnet_prefix() == prefix and \
                    ds.get_subnet_length() == int(length):
                return ds
        raise LookupError('subnet=%r not found' % subnet_str)

    def add_interior_port(self):
        return BridgePort(self.web_resource, self.dto['ports'],
                          {'type': port_type.INTERIOR_BRIDGE})

    def add_exterior_port(self):
        return BridgePort(self.web_resource, self.dto['ports'],
                          {'type': port_type.EXTERIOR_BRIDGE})

    def add_dhcp_subnet(self):
        return DhcpSubnet(self.web_resource, self.dto['dhcpSubnets'], {})
