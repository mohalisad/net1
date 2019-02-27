from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from myping import HOST_COUNT


class MyTopo( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        s = self.addSwitch('s1')
        for i in range(HOST_COUNT):
            host = self.addHost('h' + str(i+1))
            self.addLink(host, s)

net = Mininet(MyTopo(),link=TCLink)
net.start()
for host in net.hosts:
    host.cmd( 'python /home/mininet/develoer/net1/servant.py &')
    pass
CLI(net)
