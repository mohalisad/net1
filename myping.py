import os
import select
import signal
import struct
import sys
import time
import socket,sys
import random
from impacket import ImpactPacket
import file_manager as fm

default_timer = time.time

ICMP_MAX_RECV = 2048
HOST_COUNT = 10

def random_ip():
    return "10.0.0." + str(random.randint(2,HOST_COUNT))

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
            self.send_one_ping(random_ip(),"10.0.0.1",self.current_socket,data.get_part(i))
    def receive_file(self,filename):
        for i in range(2,HOST_COUNT+1):
            self.send_one_ping("10.0.0." + str(i),"10.0.0.1",self.current_socket,fm.make_rpacket(filename))
            writer = fm.file_write(filename)
        while True:
            receive_time, packet_size, ip, ip_header, icmp_header,data = self.receive_one_ping(self.current_socket)
            if writer.get_packet(data):
                break
    def circle(self):
        names = []
        receiver_ip = ""
        while True:
            receive_time, packet_size, ip, ip_header, icmp_header,data = self.receive_one_ping(self.current_socket)
            if data[0] == chr(1):
                names.append(fm.get_rpacket_name(data))
                receiver_ip = ip
            elif data[0] == chr(0):
                receiver = random_ip()
                if fm.get_packet_name(data) in names:
                    sender = receiver_ip
                    data = chr(2) + data[1:]
                else:
                    while True:
                        sender = random_ip()
                        if sender != receiver:
                            break
                #time.sleep(.2)
                self.send_one_ping(sender,receiver,self.current_socket,data)
        self.current_socket.close()

    def send_one_ping(self,src,dst,current_socket,icmp_payload):
        ip = ImpactPacket.IP()
        ip.set_ip_src(src)
        ip.set_ip_dst(dst)
        icmp = ImpactPacket.ICMP()
        icmp.set_icmp_type(icmp.ICMP_ECHO)
        icmp.contains(ImpactPacket.Data(icmp_payload))
        ip.contains(icmp)
        icmp.set_icmp_id(0x03)
        icmp.set_icmp_cksum(0)
        icmp.auto_checksum = 1

        send_time = default_timer()
        current_socket.sendto(ip.get_packet(), (dst, 1))

    def receive_one_ping(self, current_socket):
        while True:
            packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)
            if ord(str(packet_data[20])) == 0:
                break
        icmp_header = self.header2dict(
            names=[
                "type", "code", "checksum",
                "packet_id", "seq_number"
            ],
            struct_format="!BBHHH",
            data=packet_data[20:28]
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
        packet_size = len(packet_data) - 28
        ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
        if ord(str(packet_data[28])) == 1:
            data = packet_data[28:28 + fm.get_rpacket_size()]
            data = ''.join([str(elem) for elem in data])
        data = packet_data[28:28 + fm.get_packet_size()]
        data = ''.join([str(elem) for elem in data])
        return receive_time, packet_size, ip, ip_header, icmp_header,data
