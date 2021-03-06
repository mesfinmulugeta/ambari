#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import random
from resource_management.libraries.functions import conf_select

DEFAULT_COLLECTOR_SUFFIX = '.sink.timeline.collector'
DEFAULT_METRICS2_PROPERTIES_FILE_NAME = 'hadoop-metrics2.properties'

def select_metric_collector_for_sink(sink_name):
    # TODO check '*' sink_name

    all_collectors_string = get_metric_collectors_from_properties_file(sink_name)
    all_collectors_list = all_collectors_string.split(',')
    return select_metric_collector_hosts_from_hostnames(all_collectors_list)

def select_metric_collector_hosts_from_hostnames(hosts):
    return get_random_host(hosts)

def get_random_host(hosts):
    return random.choice(hosts)

def get_metric_collectors_from_properties_file(sink_name):
    hadoop_conf_dir = conf_select.get_hadoop_conf_dir()
    props = load_properties_from_file(os.path.join(hadoop_conf_dir, DEFAULT_METRICS2_PROPERTIES_FILE_NAME))
    return props.get(sink_name + DEFAULT_COLLECTOR_SUFFIX)

def load_properties_from_file(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip('" \t')
                props[key] = value
    return props
