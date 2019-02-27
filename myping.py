import os
import select
import signal
import struct
import sys
import time
import socket,sys
import random
from impacket import ImpactPacket

default_timer = time.time

ICMP_ECHO = 8
ICMP_MAX_RECV = 2048
MAX_CLIENTS = 4

def random_ip():
    return "10.0.0." + random.randint(2,MAX_CLIENTS);

class MyPing(object):
    def __init__(self, bind=None):
        self.bind = bind
        self.init_socket()
    def init_socket(self):
        try:
            current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            current_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            if self.bind:
                print('self.bind: ', self.bind)
                current_socket.bind((self.bind, 0))
        except socket.error, (errno, msg):
            if errno == 1:
                etype, evalue, etb = sys.exc_info()
                evalue = etype("%s - Note that ICMP messages can only be sent from processes running as root." % evalue)
                raise etype, evalue, etb
            raise
        self.current_socket = current_socket
    def header2dict(self, names, struct_format, data):
        unpacked_data = struct.unpack(struct_format, data)
        return dict(zip(names, unpacked_data))

    def send_file(self,data):
        for i in range(data.chunks_count()):
            self.send_one_ping(random_ip(),random_ip(),self.current_socket,data.get_part(i))
        receive_time, packet_size, ip, ip_header, icmp_header = self.receive_one_ping(self.current_socket)
        self.current_socket.close()

    def circle(self):
        while True:
            receive_time, packet_size, ip, ip_header, icmp_header = self.receive_one_ping(self.current_socket)
        self.send_one_ping(random_ip(),random_ip(),self.current_socket,icmp_header["data"])
        print "hi"
        self.current_socket.close()

    # send an ICMP ECHO_REQUEST packet
    def send_one_ping(self,src,dst,current_socket,icmp_payload):
        ip = ImpactPacket.IP()
        ip.set_ip_src(src)
        ip.set_ip_dst(dst)

        #Create a new ICMP ECHO_REQUEST packet
        icmp = ImpactPacket.ICMP()
        icmp.set_icmp_type(icmp.ICMP_ECHO)

        #inlude a small payload inside the ICMP packet
        #and have the ip packet contain the ICMP packet
        icmp.contains(ImpactPacket.Data(icmp_payload))
        ip.contains(icmp)


        #give the ICMP packet some ID
        icmp.set_icmp_id(0x03)

        #set the ICMP packet checksum
        icmp.set_icmp_cksum(0)
        icmp.auto_checksum = 1

        send_time = default_timer()

        try:
            current_socket.sendto(ip.get_packet(), (dst, 1)) # Port number is irrelevant for ICMP
        except socket.error as e:
            current_socket.close()
            return

    def receive_one_ping(self, current_socket):
        packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)
        icmp_header = self.header2dict(
            names=[
                "type", "code", "checksum",
                "packet_id", "seq_number"
            ],
            struct_format="!BBHHH",
            data=packet_data[20:20+fm.get_packet_size()]
        )
        receive_time = default_timer()
        ip_header = self.header2dict(
            names=[
                "version", "type", "length",
                "id", "flags", "ttl", "protocol",
                "checksum", "src_ip", "dest_ip"
            ],
            struct_format="!BBHHHBBHII",
            data=packet_data[:20]
        )
        packet_size = len(packet_data) - (20+fm.get_packet_size())
        ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
        return receive_time, packet_size, ip, ip_header, icmp_header
