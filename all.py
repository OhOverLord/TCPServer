SERVER_CONFIRMATION = ''
SERVER_MOVE = '102 MOVE\a\b'.encode('utf-8')
SERVER_TURN_LEFT = '103 TURN LEFT\a\b'.encode('utf-8')
SERVER_TURN_RIGHT = '104 TURN RIGHT\a\b'.encode('utf-8')
SERVER_PICK_UP = '105 GET MESSAGE\a\b'.encode('utf-8')
SERVER_LOGOUT = '106 LOGOUT\a\b'.encode('utf-8')
SERVER_KEY_REQUEST = '107 KEY REQUEST\a\b'.encode('utf-8')
SERVER_OK = '200 OK\a\b'.encode('utf-8')
SERVER_LOGIN_FAILED = '300 LOGIN FAILED\a\b'.encode('utf-8')
SERVER_SYNTAX_ERROR = '301 SYNTAX ERROR\a\b'.encode('utf-8')
SERVER_LOGIC_ERROR = '302 LOGIC ERROR\a\b'.encode('utf-8')
SERVER_KEY_OUT_OF_RANGE_ERROR = '303 KEY OUT OF RANGE\a\b'.encode('utf-8')

CLIENT_RECHARGING = 'RECHARGING\a\b'
CLIENT_FULL_POWER = 'FULL POWER\a\b'

SERVER_KEY = {
    '0': (23019, 32037),
    '1': (32037, 29295),
    '2': (18789, 13603),
    '3': (16443, 29533),
    '4': (18189, 21952)
}


UP = 0
RIGHT = 1
LEFT = 2
DOWN = 3


def print_color(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }
    if color not in colors:
        print(text)
    else:
        print(colors[color] + text + '\033[0m')import socket
from server import Server
from config import print_color


def main():
    server = Server()
    m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 4000)
    print_color(f'start server up on {server_address[0]} port {server_address[1]}', 'yellow')
    m_socket.bind(server_address)

    m_socket.listen(1)

    server.connection_to_server(m_socket)


if __name__ == "__main__":
    main()
from config import *


class Robot:
    def __init__(self) -> None:
        self.p_x = None
        self.p_y = None
        self.direction = -1
        self.barrier = False
        self.cnt = 0
        self.flag = False

    def turn_left(self):
        if self.direction == RIGHT:
            self.direction = UP
        elif self.direction == UP:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = RIGHT

    def turn_right(self):
        if self.direction == RIGHT:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = UP
        elif self.direction == UP:
            self.direction = RIGHT

    def is_barrier(self, flag):
        if not flag:
            print_color(f"I think I crashed....", "red")
            if self.cnt == 0:
                self.cnt += 1
                return SERVER_TURN_RIGHT
            elif self.cnt == 1:
                self.cnt += 1
                return SERVER_MOVE
            elif self.cnt == 2:
                self.cnt = 0
                self.barrier = False
                print_color(f"Phew, it's all right! I walked around the obstacle", "green")
                self.direction = -1
                self.p_x = None
                self.p_y = None
                return SERVER_TURN_LEFT
        else:
            print_color(f"I think I crashed....", "red")
            if self.cnt == 0:
                self.cnt += 1
                return SERVER_TURN_LEFT
            elif self.cnt == 1:
                self.cnt += 1
                return SERVER_MOVE
            elif self.cnt == 2:
                self.cnt += 1
                return SERVER_TURN_RIGHT
            elif self.cnt == 3:
                self.cnt += 1
                return SERVER_MOVE
            elif self.cnt == 4:
                self.cnt += 1
                return SERVER_MOVE
            elif self.cnt == 5:
                self.cnt = 0
                self.barrier = False
                print_color(f"Phew, it's all right! I walked around the obstacle", "green")
                self.direction = -1
                self.p_x = None
                self.p_y = None
                self.flag = False
                return SERVER_TURN_RIGHT

    def move(self, x, y):
        if x == 0 and y == 0:
            return SERVER_PICK_UP
        if self.p_x is None and self.p_y is None:
            self.p_x = x
            self.p_y = y
            return SERVER_MOVE

        if self.direction == -1:
            if x > self.p_x:
                self.direction = RIGHT
            elif x < self.p_x:
                self.direction = LEFT
            elif y > self.p_y:
                self.direction = UP
            elif y < self.p_y:
                self.direction = DOWN
            elif x == self.p_x and y == self.p_y:
                self.direction = LEFT

        if self.barrier:
            return self.is_barrier(self.flag)

        if self.direction == RIGHT:
            if x == self.p_x and y == self.p_y:
                if x == 0 or y == 0:
                    self.flag = True
                self.barrier = True
                return self.is_barrier(self.flag)
            elif x < 0:
                self.p_x = x
                self.p_y = y
                return SERVER_MOVE
            else:
                self.turn_right()
                return SERVER_TURN_RIGHT
        elif self.direction == LEFT:
            if x == self.p_x and y == self.p_y:
                if x == 0 or y == 0:
                    self.flag = True
                self.barrier = True
                return self.is_barrier(self.flag)
            elif x > 0:
                self.p_x = x
                self.p_y = y
                return SERVER_MOVE
            else:
                self.turn_right()
                return SERVER_TURN_RIGHT
        elif self.direction == UP:
            if x == self.p_x and y == self.p_y:
                if x == 0 or y == 0:
                    self.flag = True
                self.barrier = True
                return self.is_barrier(self.flag)
            elif y < 0:
                self.p_x = x
                self.p_y = y
                return SERVER_MOVE
            else:
                self.turn_right()
                return SERVER_TURN_RIGHT
        elif self.direction == DOWN:
            if x == self.p_x and y == self.p_y:
                if x == 0 or y == 0:
                    self.flag = True
                self.barrier = True
                return self.is_barrier(self.flag)
            elif y > 0:
                self.p_x = x
                self.p_y = y
                return SERVER_MOVE
            else:
                self.turn_right()
                return SERVER_TURN_RIGHT
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
            t1 = Thread(target=self.communicate, args=(conn, client_address))
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

    def communicate(self, conn, client_address):
        stage = 0
        id_key = 0
        server_hash = 0
        cnt = 0
        name = ''
        robot = Robot()
        tmp = ''
        recharge = False
        try:
            print_color(f'connection from {client_address}', "yellow")
            while True:
                tmp += str(conn.recv(1000).decode('utf-8'))
                if stage == 0 and (tmp.find('\a\b') > 18 or tmp.find('\a') > 18 or tmp.find('\b') > 18):
                    conn.sendall(SERVER_SYNTAX_ERROR)
                    break
                if stage == 4 and (tmp.find('\a\b') > 98 or tmp.find('\a') > 98 or tmp.find('\b') > 98):
                    conn.sendall(SERVER_SYNTAX_ERROR)
                    break
                if stage == 3 and '\a\b' not in tmp and len(tmp) > 12:
                    conn.sendall(SERVER_SYNTAX_ERROR)
                    break
                if '\a\b' not in tmp:
                    continue
                elif tmp.count('\a\b') >= 1 and tmp[len(tmp) - 2] == '\a' and tmp[len(tmp) - 1] == '\b':
                    data = [part for part in tmp.split('\a\b') if part]
                    tmp = ''
                    for part in data:
                        if part == "RECHARGING":
                            conn.settimeout(5)
                            recharge = True
                            continue

                        if part == "FULL POWER":
                            conn.settimeout(1)
                            recharge = False
                            continue

                        if recharge:
                            conn.sendall(SERVER_LOGIC_ERROR)
                            conn.close()
                            break
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
                            break
        except:
            print_color("TIMED OUT", "red")
        finally:
            conn.close()
