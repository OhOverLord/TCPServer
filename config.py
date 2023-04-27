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
        print(colors[color] + text + '\033[0m')