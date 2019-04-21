import xml.etree.ElementTree as ET
import os
import glob


def read():
    cwd = os.getcwd()
    filePath = os.path.join(cwd, '*config.xml')
    filePath = glob.glob(filePath)
    filePath = filePath[0]


    tree = ET.parse(filePath)
    root = tree.getroot()

    host = None
    user = None
    password = None
    dbname = None
    port = None
    engine = None

    for child in root:
        if child.tag == 'host':
            host = child.text
        if child.tag == 'user':
            user = child.text
        if child.tag == 'password':
            password = child.text
        if child.tag == 'dbname':
            dbname = child.text
        if child.tag == 'port':
            port = child.text
        if child.tag == 'engine':
            engine = child.text

    return host,user, password, dbname, port, engine
