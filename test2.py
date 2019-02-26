from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    delay      = '20ms'
    bandwidth  = 1
    switch_que = 1
    count      = 2
    def __init__( self ):
        switches = []
        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        for i in range(count):
            switches.append(self.addSwitch( 's' + str(i) ))

        # Add links
        self.addLink(h1,switches[0],delay=self.delay,max_queue_size=self.switch_que,bw=self.bandwidth)
        self.addLink(h2,switches[-1]=self.delay,max_queue_size=self.switch_que,bw=self.bandwidth)
        for i in range(1,count-1):
            self.addLink(switches[i],switches[i+1],delay=self.delay,max_queue_size=self.switch_que,bw=self.bandwidth)
topos = { 'mytopo': ( lambda: MyTopo())}
