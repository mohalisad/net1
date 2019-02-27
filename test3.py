from mininet.topo import Topo
from mininet.link import TCLink

HOST_COUNT = 4

class MyTopo( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        hosts = []
        s = self.addSwitch('s1')
        for i in range(HOST_COUNT):
            hosts.append(self.addHost('h' + str(i+1)))
            self.addLink(hosts[-1], s)


topos = { 'mytopo': ( lambda: MyTopo())}
