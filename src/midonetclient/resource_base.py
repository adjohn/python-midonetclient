# Copyright 2011 Midokura Japan KK

import exceptions
import urllib

class ResourceBase(object):

    media_type = None

    def __init__(self, web, uri, dto):
        self.web_resource = web
        self.uri = uri
        self.dto = dto

    def create(self, headers={}):
        if self.media_type:
            headers['Content-Type'] = self.media_type
        resp, data = self.web_resource.post(self.uri, self.dto, headers)

        if self.media_type:
            headers['Accept'] = self.media_type
        res, self.dto = self.web_resource.get(resp['location'], headers=headers)
        return self

    def get(self, headers={}, **kwargs):

        uri = self.dto['uri']
        res, self.dto =  self.web_resource.get(uri, headers=headers)
        return self

    def get_children(self, uri, query, headers, clazz, extra_args=None):
        resources = []
        res, dtos =  self.web_resource.get(uri, query=query, headers=headers)
        if dtos is None: # work around for hosts API returning empty when
                         # there's no hosts
            return resources
        for dto in dtos:
            if extra_args is None:
                resources.append(clazz(self.web_resource, uri, dto))
            else:
                resources.append(clazz(self.web_resource, uri, dto, *extra_args))
        return resources

    def get_uri(self):
        return self.dto['uri']

    def update(self, headers={}):
        if self.media_type:
            headers['Content-Type'] = self.media_type
        resp, body = self.web_resource.put(self.dto['uri'], self.dto, headers=headers)
        if self.media_type:
            headers['Accept'] = self.media_type
        resp, self.dto = self.web_resource.get(self.dto['uri'], headers=headers)
        return self

    def delete(self, headers={}):
        resp, junk =  self.web_resource.delete(self.dto['uri'], headers=headers)
        return None

    def __repr__(self):
        return self.__class__.__name__ + str(self.dto)

