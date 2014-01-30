#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import riak
import memcache
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.autoreload

from pandas import read_json

from utils import pandas_to_dict


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug):

        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')
        get_bucket = myBucket.get('dashboard').data

        dashboard = {}
        for d in get_bucket:
            if d['slug'] == slug:
                dashboard['slug'] = slug

                # GET ELEMENT
                _e = []
                for dash_element in d['element']:
                    element = myBucket.get('element').data
                    for e in element:
                        if dash_element == e['slug']:
                            _e.append(e)
                dashboard['element'] = _e

        self.render('index.html', dashboard=dashboard)


class ProcessHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, slug):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining')

        columns = json.loads(myBucket.get('{}-columns'.format(slug)).data)
        fields = columns
        try:
            if len(self.get_argument('fields')) >= 1:
                fields = self.get_argument('fields').split(',')
        except:
            pass

        fields_json = json.dumps(fields)
        if mc.get(str(slug)) and\
                mc.get('{}-columns'.format(slug)) == fields_json:
            self.write(mc.get(str(slug)))
            self.finish()

        mc.set('{}-columns'.format(slug), fields_json)

        df = read_json(myBucket.get(slug).data)

        read = df[fields]
        convert = pandas_to_dict(read)

        write = json.dumps({'columns': fields, 'json': convert})
        mc.set(str(slug), write)
        self.write(write)
        self.finish()