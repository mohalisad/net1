import file_manager as fm
import myping as mp

file = fm.file_read("a.txt")
myping = mp.MyPing()
myping.send_file(file)

raw_input()

myping.receive_file("a.txt")
