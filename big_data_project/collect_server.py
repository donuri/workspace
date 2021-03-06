import argparse
import configparser
from multiprocessing import Process, Queue, Pipe
import psutil
import time
import socket


def arg_reader():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', type=str, default='conf.txt')
    return parser.parse_args().conf


def conf_reader(conf_file):
    result = dict()
    conf = configparser.ConfigParser()
    conf.read(conf_file)
    section = conf.sections()
    for i in section:
        result[i] = conf[i]['interval']
    return result


def time_tick(pipe_name):
    count = 0
    while 1:
        try:
            time.sleep(1 - time.time() % 1)
            count += 1
            pipe_name.send(count)
            #            print(time.time())
            if count == 60:
                count = 0
        except:
            print('time_tick stop')
            break


def make_pipe(**data):
    for i in data.keys():
        globals()[f't{i[0]}'], globals()[f'{i[0]}t'] = Pipe()
        print(f'Make {i} pipe success')


def make_timer(**data):
    timers = []
    for i in data.keys():
        globals()[f'{i}_timer'] = Process(target=time_tick, args=(globals()[f't{i[0]}'],))
        timers.append(globals()[f'{i}_timer'])
        print(f'Make {i} timer success')
    return timers


def run_timer(timers):
    for timer in timers:
        timer.start()


def cpu_collector(conn, q, interval):
    while 1:
        try:
            if conn.recv() % interval == 0:
                # print(time.time())
                q.put(f'cpu {time.time()} {psutil.cpu_percent(None)}')
        except:
            print('cpu_collector stop')
            break


def mem_collector(conn, q, interval):
    while 1:
        try:
            if conn.recv() % interval == 0:
                # print(time.time())
                q.put(f'mem {time.time()} {psutil.virtual_memory().percent}')
        except:
            print('mem_collector stop')
            break


def disk_collector(conn, q, interval, disk_name):
    while 1:
        try:
            if conn.recv() % interval == 0:
                # print(time.time())
                q.put(f'disk {time.time()} {psutil.disk_usage(disk_name).percent}')
        except:
            print('disk_collector stop')
            break


def make_collector(q, **data):
    for i, j in data.items():
        j = int(j)
        if i == 'cpu':
            print('make cpu process sucess')
            cpu_pro = Process(target=cpu_collector, args=(globals()[f'{i[0]}t'], q, j))
            cpu_pro.start()

        elif i == 'mem':
            print('make mem process sucess')
            mem_pro = Process(target=mem_collector, args=(globals()[f'{i[0]}t'], q, j))
            mem_pro.start()

        elif i == 'disk':
            print('make disk process sucess')
            disk_pro = Process(target=disk_collector, args=(globals()[f'{i[0]}t'], q, j, 'c://'))
            disk_pro.start()


def socket_send_server(q, HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    while 1:
        try:
            data = str(q.get())
            msg = data
            data = msg.encode()
            length = len(data)
            client_socket.sendall(length.to_bytes(4, byteorder="little"))
            client_socket.sendall(data)

            data = client_socket.recv(4)
            length = int.from_bytes(data, "little")
            data = client_socket.recv(length)
            msg = data.decode()
            print('Received from : ', msg)
        except:
            print('client_server stop')
            break

    client_socket.close()


def main():
    data = conf_reader(arg_reader())
    make_pipe(**data)
    q = Queue()
    make_collector(q, **data)
    timers = make_timer(**data)
    run_timer(timers)
    socket_send_server(q, '127.0.0.1', 9999)


if __name__ == '__main__':
    main()
