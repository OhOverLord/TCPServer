import socket
from threading import Thread
from config import *
from robot import Robot
import re


def extract_data(data):
    data = data.encode('utf-8')
    if data == '':
        return data


class Server:
    def __init__(self) -> None:
        self.list_of_threads = []

    @staticmethod
    def extract_data(data):
        return [part for part in data.split('\a\b') if part]
    @staticmethod
    def extract_coordinates(data):
        tmp = data.split(' ')
        x = int(tmp[1])
        y = int(tmp[2])
        return x, y

    def connection_to_server(self, m_socket):
        while True:
            print_color('waiting for a connection', 'green')
            conn, client_address = m_socket.accept()
            conn.settimeout(1)
            t1 = Thread(target=self.communicate, args=(m_socket, conn, client_address))
            t1.start()
            self.list_of_threads.append(t1)

    @staticmethod
    def enc_message(data):
        _str = str(data)
        _str += '\a\b'
        return _str.encode('utf-8')

    def server_confirmation(self, name, server_key):
        _sum = 0
        for c in name:
            _sum += ord(c)

        _sum *= 1000
        _hash = _sum % 65536
        _sum += server_key
        return self.enc_message((_hash + server_key) % 65536), _hash

    def compare_hashes(self, _num, _hash, client_key):
        _num = int(_num)
        _num += 65536 - client_key
        _num %= 65536
        if _num == _hash:
            return True
        return False

    def communicate(self, m_socket, conn, client_address):
        stage = 0
        id_key = 0
        server_hash = 0
        cnt = 0
        name = ''
        robot = Robot()
        tmp = ''
        try:
            print_color(f'connection from {client_address}', "yellow")
            while True:
                tmp += str(conn.recv(1000).decode('utf-8'))
                if '\a\b' not in tmp:
                    continue
                elif tmp.count('\a\b') >= 1 and tmp[len(tmp) - 2] == '\a' and tmp[len(tmp) - 1] == '\b':
                    data = [part for part in tmp.split('\a\b') if part]
                    tmp = ''
                    for part in data:
                        print(f'Received {part}')
                        if stage == 0:
                            name = part
                            if len(name) > 18:
                                conn.sendall(SERVER_SYNTAX_ERROR)
                                break
                            conn.sendall(SERVER_KEY_REQUEST)
                            stage += 1
                        elif stage == 1:
                            id_key = part
                            if not id_key.isdigit():
                                conn.sendall(SERVER_SYNTAX_ERROR)
                                break
                            if int(id_key) < 0 or int(id_key) > 4:
                                conn.sendall(SERVER_KEY_OUT_OF_RANGE_ERROR)
                                break
                            server_key = SERVER_KEY[part][0]
                            confirmation_server_key, server_hash = self.server_confirmation(name, server_key)
                            conn.sendall(confirmation_server_key)
                            stage += 1
                        elif stage == 2:
                            if not part.isdigit() or len(part) >= 6:
                                conn.sendall(SERVER_SYNTAX_ERROR)
                                break
                            if self.compare_hashes(part, server_hash, SERVER_KEY[id_key][1]):
                                conn.sendall(SERVER_OK)
                            else:
                                conn.sendall(SERVER_LOGIN_FAILED)
                                break
                            print_color(f"Hello mr {name}!", "purple")
                            conn.sendall(SERVER_MOVE)
                            stage += 1
                        elif stage == 3:
                            print(part)
                            if part[len(part) - 1] == ' ':
                                conn.sendall(SERVER_SYNTAX_ERROR)
                                break
                            if '.' in part:
                                conn.sendall(SERVER_SYNTAX_ERROR)
                                break
                            if part != '' and 'OK' in part:
                                cnt += 1
                                x, y = self.extract_coordinates(part)
                                res = robot.move(x, y)
                                if res == SERVER_PICK_UP:
                                    conn.sendall(SERVER_PICK_UP)
                                    stage += 1
                                else:
                                    conn.sendall(res)
                            else:
                                break
                        elif stage == 4:
                            print_color(f"Tajný vzkaz: {part}", "red")
                            conn.sendall(SERVER_LOGOUT)
                            conn.close()
        except Exception as e:
            print(e)
        finally:
            conn.close()
