"""
Example topology of Quagga routers
"""

import inspect
import os
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        # List of Quagga host configs
        quaggaHosts = []
        

        # Add switch for IXP fabric
        #ixpfabric = self.addSwitch('fabric-sw1')

	H1 = QuaggaHost(name='h1', ip='172.0.1.1/24', loIP='10.0.1.1/24')
	R1 = QuaggaHost(name='r1', ip='172.0.1.2/24', loIP='10.0.1.2/24')
	H2 = QuaggaHost(name='h2', ip='172.0.6.2/24', loIP='10.0.6.2/24')
	R4 = QuaggaHost(name='r4', ip='172.0.4.2/24', loIP='10.0.4.2/24')
	R2 = QuaggaHost(name='r2', ip='172.0.2.2/24', loIP='10.0.2.2/24')
	R3 = QuaggaHost(name='r3', ip='172.0.3.2/24', loIP='10.0.3.2/24')

	quaggaHosts.append(H1)
	quaggaHosts.append(R1)
	quaggaHosts.append(H2)
	quaggaHosts.append(R4)
	quaggaHosts.append(R2)
	quaggaHosts.append(R3)
	
	quaggaNodes = []

        # Setup each Quagga router, add a link between it and the IXP fabric
        for host in quaggaHosts:

            # Create an instance of a host, called a quaggaContainer
            quaggaContainer = self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)
		
	    quaggaNodes.append(quaggaContainer);

            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            # Attach the quaggaContainer to the IXP Fabric Switch
            #self.addLink(quaggaContainer, ixpfabric)

	
	self.addLink(quaggaNodes[0], quaggaNodes[1], intfName1='h1-eth0', params1={'ip':'172.0.1.1/24'}, intfName2='r1-eth0', params2={'ip':'172.0.1.2/24'})

	self.addLink(quaggaNodes[1],quaggaNodes[4], intfName1='r1-eth1', params1={'ip':'172.0.2.1/24'}, intfName2='r2-eth0', params2={'ip':'172.0.2.2/24'})
	self.addLink(quaggaNodes[1],quaggaNodes[5], intfName1='r1-eth2', params1={'ip':'172.0.3.1/24'}, intfName2='r3-eth0', params2={'ip':'172.0.3.2/24'})

	self.addLink(quaggaNodes[4],quaggaNodes[3], intfName1='r2-eth1', params1={'ip':'172.0.4.1/24'}, intfName2='r4-eth0', params2={'ip':'172.0.4.2/24'})

	self.addLink(quaggaNodes[5],quaggaNodes[3], intfName1='r3-eth1', params1={'ip':'172.0.5.1/24'}, intfName2='r4-eth1', params2={'ip':'172.0.5.2/24'})
	
	self.addLink(quaggaNodes[2],quaggaNodes[3], intfName1='h2-eth0', params1={'ip':'172.0.6.2/24'}, intfName2='r4-eth2', params2={'ip':'172.0.6.1/24'})
	
	
