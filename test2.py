from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    delay      = '20ms'
    bandwidth  = 1
    switch_que = 1
    count      = 2
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        s1 = self.addSwitch( 's1' )

        # Add links
        self.addLink(h1,s1,delay=self.delay,max_queue_size=self.switch_que,bw=self.bandwidth)
        self.addLink(h2,s1,delay=self.delay,max_queue_size=self.switch_que,bw=self.bandwidth)

topos = { 'mytopo': ( lambda: MyTopo())}
