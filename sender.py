import file_manager as fm
import myping as mp

file = fm.file_read("a.txt")
mp.MyPing().send_file(file)
