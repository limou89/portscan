import socket
from datetime import datetime
from optparse import OptionParser
from threading import Thread
import os

# 多线程复杂命令扫描器
def open_1(ip, port):
    s = socket.socket()
    try:
        s.connect((ip, port))
        return True
    except:
        return False

def scan(ip, port, filename):
    if open_1(ip, port):
        print("%s host %s port open" % (ip, port))
        try:
            with open(filename, 'a') as f:
                f.write("%s host %s port open\n" % (ip, port))
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        print("%s host %s port close" % (ip, port))

def main():
    usage = "usage: xxx.py -i ip地址 -p 端口"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--ip", type="string", dest="ipaddress", help="your target ip here")
    parser.add_option("-p", "--port", type="string", dest="port", help="your target port here")
    (options, args) = parser.parse_args()

    ip = options.ipaddress
    port = options.port

    if not ip or not port:
        print("Error: IP address and port must be provided.")
        return

    defaultport = [135, 149, 445, 1433, 3306, 3389, 5944]

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime("%Y年%m月%d日%H时%M分%S秒")
    result_dir = './result/'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    filename = os.path.join(result_dir, f"result_{timestamp}.txt")

    if ',' in port:  # xxx.py -i 127.0.0.1 -p 80,21,89
        port_list = [int(x) for x in port.split(',')]
        for p in port_list:
            s = Thread(target=scan, args=(ip, p, filename,))
            s.start()

    elif '-' in port:  # xxx.py -i 127.0.0.1 -p 10805-10810
        start_port, end_port = map(int, port.split('-'))
        for p in range(start_port, end_port + 1):
            s = Thread(target=scan, args=(ip, p, filename,))
            s.start()

    elif port == 'all':  # xxx.py -i 127.0.0.1 -p all
        for p in range(1, 65536):
            s = Thread(target=scan, args=(ip, p, filename,))
            s.start()

    elif port == 'default':  # xxx.py -i 127.0.0.1 -p default
        for p in defaultport:
            s = Thread(target=scan, args=(ip, p, filename,))
            s.start()

if __name__ == '__main__':
    main()