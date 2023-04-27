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
