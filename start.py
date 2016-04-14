#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo

net = None


def startNetwork():
    "instantiates a topo, then starts the network and prints debug information"

    info('** Creating Quagga network topology\n')
    topo = QuaggaTopo()

    info('** Starting the network\n')
    global net
    net = MiniNExT(topo, controller=OVSController)
    net.start()

    info('** Dumping host connections\n')
    dumpNodeConnections(net.hosts)

    info('** Testing network connectivity\n')
    net.ping(net.hosts) 

#Insert Queries
    net['r1'].cmd('sysctl -w net.ipv4.ip_forward=1')
    net['r2'].cmd('sysctl -w net.ipv4.ip_forward=1')
    net['r3'].cmd('sysctl -w net.ipv4.ip_forward=1')
    net['r4'].cmd('sysctl -w net.ipv4.ip_forward=1')
 
    net['h1'].cmd('ip route add 41.41.2.0/24 via 41.41.1.2')
    net['h1'].cmd('ip route add 41.41.3.0/24 via 41.41.1.2')
    net['h1'].cmd('ip route add 41.41.4.0/24 via 41.41.1.2')
    net['h1'].cmd('ip route add 41.41.5.0/24 via 41.41.1.2')
    net['h1'].cmd('ip route add 41.41.6.0/24 via 41.41.1.2')

    net['r1'].cmd('ip route add 41.41.4.0/24 via 41.41.2.2')
    net['r1'].cmd('ip route add 41.41.5.0/24 via 41.41.3.2')
    net['r1'].cmd('ip route add 41.41.6.0/24 via 41.41.2.2')

    net['r2'].cmd('ip route add 41.41.1.0/24 via 41.41.2.1')
    net['r2'].cmd('ip route add 41.41.3.0/24 via 41.41.2.1')
    net['r2'].cmd('ip route add 41.41.5.0/24 via 41.41.4.2')
    net['r2'].cmd('ip route add 41.41.6.0/24 via 41.41.4.2')

    net['r3'].cmd('ip route add 41.41.1.0/24 via 41.41.3.1')
    net['r3'].cmd('ip route add 41.41.2.0/24 via 41.41.3.1')
    net['r3'].cmd('ip route add 41.41.4.0/24 via 41.41.5.2')
    net['r3'].cmd('ip route add 41.41.6.0/24 via 41.41.5.2')	

    net['r4'].cmd('ip route add 41.41.2.0/24 via 41.41.4.1')
    net['r4'].cmd('ip route add 41.41.3.0/24 via 41.41.5.1')
    net['r4'].cmd('ip route add 41.41.1.0/24 via 41.41.4.1')

    net['h2'].cmd('ip route add 41.41.2.0/24 via 41.41.6.1')
    net['h2'].cmd('ip route add 41.41.3.0/24 via 41.41.6.1')
    net['h2'].cmd('ip route add 41.41.4.0/24 via 41.41.6.1')
    net['h2'].cmd('ip route add 41.41.5.0/24 via 41.41.6.1')
    net['h2'].cmd('ip route add 41.41.1.0/24 via 41.41.6.1')

#r1 sysctl -w net.ipv4.ip_forward=1

    info('** Dumping host processes\n')
    for host in net.hosts:
        host.cmdPrint("ps aux")

    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
