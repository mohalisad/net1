SPLIT_SIZE = 100
MAX_FILENAME_SIZE = 16
class file_read:
    def __init__(self,path):
        self.file_name = path + chr(0)*(MAX_FILENAME_SIZE - len(path))
        with open(path, 'r') as content_file:
            self.content = content_file.read()
        self.chunks = []
        i = 0
        while i < len(self.content):
            self.chunks.append(self.content[i:min(i+SPLIT_SIZE,len(self.content))])
            i += SPLIT_SIZE
    def chunks_count(self):
        return len(self.chunks)
    def get_part(self,index):
        header = chr(0)+chr(index)+chr(self.chunks_count())+self.file_name
        chunk_length = len(self.chunks[index])
        body = chr(chunk_length)+self.chunks[index] + chr(0)*(SPLIT_SIZE-chunk_length)
        return header+body
class file_write:
    def __init__(self,file_name):
        self.file_name = file_name
        self.packets_received = 0
    def get_packet(self,packet):
        file_name = fix_str(packet[3:3+MAX_FILENAME_SIZE])
        if self.file_name == file_name:
            if self.packets_received == 0:
                self.packets_count = ord(packet[2])
                self.packets = [''] * self.packets_count
            index = ord(packet[1])
            chunk_length = ord(packet[3+MAX_FILENAME_SIZE])
            begin = 4+MAX_FILENAME_SIZE
            self.packets[index] = packet[begin:begin+chunk_length]
            self.packets_received += 1
            self.check_complete()
    def check_complete(self):
        if self.packets_received >= self.packets_count:
            if not '' in self.packets:
                self.save()
    def save(self):
        print "".join(self.packets)

def get_packet_size():
    return 4+MAX_FILENAME_SIZE+SPLIT_SIZE
def fix_str(input):
    ret = ""
    for i in input:
        if i == chr(0):
            return ret
        ret += i
