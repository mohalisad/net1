from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )

        # Add links
        self.addLink( h1, s1, delay='20ms' )
        self.addLink( h2, s1, delay='20ms' )
        self.addLink( s1, s2, delay='50ms' )
        self.addLink( h3, s2, delay='15ms' )
        self.addLink( h4, s2, delay='1s'   )


topos = { 'mytopo': ( lambda: MyTopo())}
