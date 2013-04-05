#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from optparse import OptionParser
import MySQLdb
from mako.template import Template
import yaml
import copy
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
import json

try:
  from collections import OrderedDict
except ImportError:
  from ordereddict import OrderedDict

mydoc_dir = os.path.dirname(os.path.abspath(__file__))
 
def pp(obj):
  if isinstance(obj, list) or isinstance(obj, dict):
    orig = json.dumps(obj, indent=4)
    print eval("u'''%s'''" % orig).encode('utf-8')
  else:
    print obj

def represent_dict(self, data):
    def key_function((key,value)):
        prio = {"comments":0,"columns":1}.get(key,99)
        return (prio, key)
    items = data.items()
    items.sort(key=key_function)
    return self.represent_mapping(u'tag:yaml.org,2002:map', items)

yaml.add_representer(dict, represent_dict)

def represent_odict(self, data):
    return self.represent_mapping(u'tag:yaml.org,2002:map', data.items())

yaml.add_representer(OrderedDict, represent_odict)

def construct_odict(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_constructor(u'tag:yaml.org,2002:map', construct_odict)

def opt_parse():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.set_defaults(doc_file="schema_doc.yaml")
    parser.add_option("-u", "--user", dest="user", help="", metavar="USER")
    parser.add_option("-p", "--password", dest="passwd", metavar="PASSWORD")
    parser.add_option("-H", "--host", dest="host", metavar="HOST")
    parser.add_option("-d", "--database", dest="db", metavar="DATABASE")
    parser.add_option("-y", "--yamldoc", dest="doc_file", metavar="DOCFILE")
    return parser.parse_args()

def erdump(**dbinf):
    graph = create_schema_graph(
        metadata=MetaData('mysql://%(user)s:%(passwd)s@%(host)s/%(db)s' % dbinf),
        show_datatypes=False,
        show_indexes=False,
        # rankdir='TB',
        rankdir='LR',
        concentrate=False
    )
    graph.write_png('erd.png')

def simplify(doc):
    simpl_doc = copy.deepcopy(doc)
    for t, t_val in simpl_doc['tables'].iteritems():
        for c, c_inf in t_val['columns'].iteritems():
            if c_inf != '':
                t_val['columns'][c] = c_inf['comment']
    return simpl_doc

def merge_yaml(new_doc, old_doc):
    if new_doc['db'] != old_doc['db']:
        raise Exception("db name mismatched with yaml, rename it! dbname in yaml: %s" % old_doc['db'])
    old_tables = old_doc['tables']
    new_tables = new_doc['tables']

    for new_t, new_t_content in new_tables.iteritems():
        if old_tables.has_key(new_t):
            new_t_content['comments'] = old_tables[new_t]['comments']
        else:
            continue
        for column_name in new_t_content['columns'].iterkeys():
            if old_tables[new_t]['columns'].has_key(column_name):
                new_t_content['columns'][column_name]['comment'] = old_tables[new_t]['columns'][column_name]

def yaml_merge_out(org_doc_file, doc_inf):
    try:
        f = open(org_doc_file, "r")
    except IOError, e:
        f = open(org_doc_file, "w")
        yaml.dump(simplify(doc_inf), f, encoding='utf8', allow_unicode=True, default_flow_style=False)
        f.close()
    else:
        old_doc = yaml.load(f)
        f.close()
        if old_doc:
            merge_yaml(doc_inf, old_doc)
        f = open(org_doc_file, "w")
        f.truncate()

        yaml.dump(simplify(doc_inf), f, encoding='utf8', allow_unicode=True, default_flow_style=False)
        f.close()

def main():
    try:
        opt, args = opt_parse()
    except Exception:
        usage()

    yaml_doc = OrderedDict({
        'db': opt.db,
        'tables': OrderedDict({})
    })

    doc_file = opt.__dict__.pop("doc_file")
    erdump(**(opt.__dict__))
    
    con = MySQLdb.connect(**(opt.__dict__))
    cur = con.cursor()    
    s = "show tables;"
    cur.execute(s)

    for t in cur.fetchall():
        cur.execute("desc %s;" % t[0])
        columns = cur.fetchall()

        columns_doc = OrderedDict([(c[0], {'type':c[1],'null':c[2],'key':c[3],'default':c[4],'extra':c[5],'comment': ""}) for c in columns])
        
        yaml_doc['tables'][t[0]] = OrderedDict({'columns': columns_doc, 'comments': [""]})

    yaml_merge_out(doc_file, yaml_doc)

    tmpl = Template(filename='%s/mydoc_tmpl.mako' % mydoc_dir, output_encoding='utf-8')
    print tmpl.render(attributes=yaml_doc)

if __name__ == "__main__":
    main()
