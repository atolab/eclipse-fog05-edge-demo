import os
from fog05 import FIMAPI
from fog05_sdk.interfaces.FDU import FDU
import sys
import time
import json


DESC_FOLDER = './descriptors'

nuc = '4a560914-1c3e-4966-9fa8-7f0acc903253'
whitepi = 'e348ab58-5e36-4ec3-b55b-47ab00fe1ed2'
sensorpi = '64b067b6-abcc-41c5-b589-9c412bcd679b'
robotpi = '0e84bfdc-7568-49dd-983a-05ec36128a50'
descs = {
    'gw.json':whitepi,
    'ap.json':nuc,
    'zenoh.json':nuc,
    'control.json':nuc,
    'robot.json':robotpi,
    'gui.json':whitepi
}

net_desc = []

def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def read(fname):
    return open(fname).read()


def main(ip):
    a = FIMAPI(ip)

    fdus = {}
    nets = []

    print('Current Eclipse fog05 Infrastrucutre:')

    nodes = a.node.list()
    for nid in nodes:
        info = a.node.info(nid)
        print('ID: {} Hostname: {}'.format(nid, info['name']))


    input('Press enter to instantiate the demo')

    for d in net_desc:
        path_d = os.path.join(DESC_FOLDER,d)
        netd = json.loads(read(path_d))
        a.network.add_network(netd)
        nets.append(netd['uuid'])
        time.sleep(1)

    for d in descs:
        nid = descs[d]
        print('Instantiating {} to {}'.format(d, nid))
        path_d = os.path.join(DESC_FOLDER,d)
        data = json.loads(read(path_d))
        fdu_d = FDU(data)
        fduinfo = a.fdu.onboard(fdu_d)
        fdu_id = fduinfo.uuid
        print ('fdu_id : {}'.format(fdu_id))
        inst_info = a.fdu.define(fdu_id, nid)
        iid = inst_info.uuid
        time.sleep(1)
        a.fdu.configure(iid)
        time.sleep(1)
        a.fdu.start(iid)
        print ('iid : {}'.format(iid))
        print('Instantiated: {}'.format(fdu_d.name))
        fdus.update({fdu_id: iid})
        time.sleep(2)

    print('Instantiated:')
    print(json.dumps(fdus, indent=2))
    print('Bye!')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage {} <zenoh ip:port>")
        exit(-1)
    main(sys.argv[1])
