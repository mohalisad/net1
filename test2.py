from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

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
        self.addLink( h1, s1, delay='20ms',max_queue_size=1000)
        self.addLink( h2, s1, delay='20ms',max_queue_size=1000)
        self.addLink( s1, s2, delay='50ms',max_queue_size=1000)
        self.addLink( h3, s2, delay='15ms',max_queue_size=1000)
        self.addLink( h4, s2, delay='1s'  ,max_queue_size=1000)


topos = { 'mytopo': ( lambda: MyTopo())}
