#!/bin/sh
ip netns add h1
ip netns add h2
ip netns add h3
/usr/share/openvswitch/scripts/ovs-ctl start
ovs-vsctl add-br s1
ovs-vsctl add-br s2
ip link add l1-1 type veth peer name l1-2
ip link add l2-1 type veth peer name l2-2
ip link add l3-1 type veth peer name l3-2
ip link add l4-1 type veth peer name l4-2

ip link set l1-2 up
ip link set l2-2 up

ip link set l1-1 netns h1
ovs-vsctl add-port s1 l1-2

ip link set l2-1 netns h2
ovs-vsctl add-port s1 l2-2

ip netns exec h1 ip addr add 10.0.0.1/24 dev l1-2
ip netns exec h2 ip addr add 10.0.0.2/24 dev l2-2
