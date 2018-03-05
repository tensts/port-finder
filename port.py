#!/usr/bin/python

import os
import sys
import json
import sqlite3
from jsonschema import validate
import time
import argparse

DB_PATH=os.path.join(os.getcwd(),'data/ports.sqlite3')
DEBUG=0
JSON_SCHEMA={"description":"string",
        "port":"number",
        "status":"string",
        "proto":"string"}

def _parse_record(record):
    try:
        validate(record,JSON_SCHEMA)
    except ValidationError as e: 
        raise e
        return False

    if record['tcp'] is True and record['udp'] is True:
        record['proto'] = 'tcp|udp'
    elif record['udp'] is False:
        record['proto'] = 'tcp'
    else:
        record['proto'] = 'udp'

    return (record['port'], record['proto'],
            record['status'][:16], record['description'])


def importdb(filepath):
    print '[+] starting import'
    start = time.time()
    
    try:
        conn = sqlite3.connect(DB_PATH)
    except:
        print '[!] could not connect to sqlite3'
        return 1
    
    cur = conn.cursor()

    print '[+] dropping existing database...'
    cur.execute('DROP TABLE IF EXISTS "ports"')
    conn.commit()
    
    print '[+] creating new table'
    cur.execute("CREATE TABLE ports(port int, proto varchar(7),status varchar(16), description text)")
    conn.commit()
    
    tmp=[]
    print '[+] reading json file'
    #json rather will fit to memory
    #so we dont have to stream it.
    data = json.load(open(filepath,'r'))
    print '[+] importing...'
    for idx,port_number in enumerate(data['ports']):
        record = data['ports'][port_number]

        if DEBUG == 1:
            print "[:] importing nr: %d" % idx
            print record
        
        if isinstance(record,list) == False:
            try:
                tmp.append(_parse_record(record))
            except ValidationError:
                print "[!] error loading record %d" % idx
                continue
        else:
            for n in record:
                try:
                    tmp.append(_parse_record(n))
                except ValidationError:
                    print "[!] error loading record %d" % idx
                    continue

        
        if idx % 1024 == 0:
            cur.executemany('''REPLACE INTO ports(port,proto,status,description)
                       VALUES(?,?,?,?)''',tmp)
            conn.commit()
            tmp = []
    
    conn.commit()

    cur.execute("CREATE INDEX port_ports on ports(port)")
    conn.commit()
    conn.close()
    conn = None
    print '[+] import ended in %d sec' % (time.time() - start)
    return True

def find(port_number):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for record in cur.execute("SELECT * FROM PORTS WHERE PORT=?",(port_number,)):
        print '''[+] PORT: %d,\nPROTO: %s,\nSTATUS: %s,\nDESCRIPTION:\n%s''' % record

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', metavar="port_number", type=int, nargs='?',default='-1')
    parser.add_argument('-v', action="store_true", default=False, help="verbose")
    parser.add_argument('-d', metavar="sqlite3_file", required=False, help="override default sqlite3_file")
    parser.add_argument('-i', metavar='json_file', required=False, help="import json_file to database" )
    args = parser.parse_args()
    
    if args.v is not False:
        DEBUG=1

    if args.d is not None:
        DB_PATH = args.d
        if DEBUG == 1:
            print "[:] changed database path to %s" % DB_PATH
    
    if args.i is not None and os.path.exists(args.i):
        if DEBUG == 1:
            print "[:] importing from %s to %s" %(args.i,DB_PATH)
            #sys.exit("[+] DEBUG END")
        status = importdb(args.i)
        sys.exit(status)
    
    if isinstance(args.port,int) and args.port != -1:
        find(args.port)
    else:
        parser.print_help(sys.stderr)
