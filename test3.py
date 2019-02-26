from mininet.topo import Topo
from mininet.link import TCLink
import constant

class MyTopo( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        hosts = []
        s = self.addSwitch('s')
        for i in range(constant.HOST_COUNT):
            hosts.append(elf.addHost('h' + str(i)))
            self.addLink(h + str(i), s)


topos = { 'mytopo': ( lambda: MyTopo())}
