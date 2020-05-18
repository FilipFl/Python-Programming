from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel
from PySide2 import QtGui
from PySide2.QtGui import QPainter, QBrush, QPen, QPolygon
from PySide2.QtCore import QPoint, Qt, QRectF
import random
import math
import sys
import os

# the task given was to create a 2048 game on a hex board for 2 players, using Qt (Pyside2)

class Game:

    def __init__(self):
        self.player_playing = 1
        self.board = Board()
        self.board.create_block(self.player_playing)
        self.done = False

    def is_done(self):
        return self.done

    def finish_him(self):
        self.done = True

    def change_player(self):
        if self.player_playing ==1:
            self.player_playing = 2
        else:
            self.player_playing = 1

    def moveQT(self, click):
        if click == 1 and self.player_playing == 1:
            if self.board.move_blocks(self.player_playing, 0):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 2 and self.player_playing == 1:
            if self.board.move_blocks(self.player_playing, 1):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 3 and self.player_playing == 1:
            if self.board.move_blocks(self.player_playing, 2):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 4 and self.player_playing == 1:
            if self.board.move_blocks(self.player_playing, 3):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 5 and self.player_playing == 1:
            if self.board.move_blocks(self.player_playing, 4):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 6 and self.player_playing == 1:
            if self.board.move_blocks(self.player_playing, 5):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 7 and self.player_playing == 2:
            if self.board.move_blocks(self.player_playing, 0):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 8 and self.player_playing == 2:
            if self.board.move_blocks(self.player_playing, 1):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 9 and self.player_playing == 2:
            if self.board.move_blocks(self.player_playing, 2):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 10 and self.player_playing == 2:
            if self.board.move_blocks(self.player_playing, 3):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 11 and self.player_playing == 2:
            if self.board.move_blocks(self.player_playing, 4):
                self.change_player()
                self.board.create_block(self.player_playing)
        elif click == 12 and self.player_playing == 2:
            if self.board.move_blocks(self.player_playing, 5):
                self.change_player()
                self.board.create_block(self.player_playing)
        else:
            pass



    def main_game(self):
        os.system("cls" if os.name == 'nt' else 'clear')
        self.board.create_block(self.player_playing)
        self.move()
        self.change_player()

    def get_block(self,x,y):
        return self.board.get_field(x,y).get_block()

class Board:
    def __init__(self):
        self.map = []
        for i in range(0,9):
            row = []
            if i==0 or i==8:
                for j in range(0,5):
                    f = Field(i, j)
                    row.append(f)
            if i==1 or i==7:
                for j in range(0,6):
                    f = Field(i,j)
                    row.append(f)
            if i==2 or i==6:
                for j in range(0,7):
                    f = Field(i,j)
                    row.append(f)
            if i==3 or i==5:
                for j in range(0,8):
                    f = Field(i,j)
                    row.append(f)
            else:
                for j in range(0,9):
                    f= Field(i,j)
                    row.append(f)
            self.map.append(row)

    def get_field(self,x,y):
        return self.map[x][y]

    # metoda co runde tworząca klocek aktualnie grającego gracza
    def create_block(self, player):
        done = False
        while not done:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            status, ble = self.check_bound(x,y)
            if status:
                possible = self.get_field(x,y).get_block()
                if possible is None:
                    self.get_field(x, y).make_block(player)
                    done = True


    def move_blocks(self,player, dir):
        blocks = []
        iterations = -1
        for column in self.map:
            for field in column:
                block = field.get_block()
                if block != None:
                    if block.get_player() == player:
                        blocks.append(block)
        # przesuwanie każdego klocka po kolei, aż nic się nie będzie zmieniać na planszy
        nothing_changed = False
        while not nothing_changed:
            # określenie które klocki powinny poruszać się najpierw, w zależności jaki kierunek ruchu
            if dir == 0:
                blocks.sort(key=lambda x: x.get_y(), reverse=True)
            if dir == 3:
                blocks.sort(key=lambda x: x.get_y())
            if dir == 2:
                blocks.sort(key=lambda x: x.get_x())
            if dir == 5:
                blocks.sort(key=lambda x: x.get_x(), reverse=True)
            if dir == 1:
                blocks.sort(key=lambda x: x.get_x())
            if dir == 4:
                blocks.sort(key=lambda x: x.get_x(), reverse=True)
            nothing_changed = True
            for item in blocks:
                iterations += 1
                old = item.get_coords()
                possible, new_coords = item.get_adress_to_move(dir)
                if possible:
                    existing = self.get_field(new_coords[0], new_coords[1]).get_block()
                    if existing is not None:
                        if existing.get_player() == player and existing.get_value() == item.get_value():
                            existing.mul_value()
                            blocks.remove(item)
                            self.get_field(old[0], old[1]).del_block()
                            nothing_changed = False
                    else:
                        item.set_coords(new_coords)
                        self.get_field(new_coords[0],new_coords[1]).asign_block(item)
                        self.get_field(old[0], old[1]).del_block()
                        nothing_changed = False
        #sprawdzenie czy cokolwiek się zmieniło jeśli nie, ruch niepoprawny
        if iterations == 0:
            return False
        else:
            return True

    # sprawdzenie czy współrzędne znajdują się na mapie
    def check_bound(self, x, y):
        if x < 0 or y < 0 or x > 8:
            return False, [x, y]
        if x < 5:
            if y - x > 4:
                return False, [x, y]
        if (x == 5 and y > 7) or (x == 6 and y > 6) or (x == 7 and y > 5) or (x == 8 and y > 4):
            return False, [x, y]
        return True, [x, y]


class Field:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.blocked = None

    def make_block(self,player):
        self.blocked = Block(player,self.pos_x,self.pos_y)

    def del_block(self):
        self.blocked = None

    def asign_block(self,block):
        self.blocked = block


    def get_block(self):
        return self.blocked

    def value_to_string(self):
        #funkcja do printowania wartości
        s = ''
        if self.blocked is not None:
            value = self.blocked.get_value()
            if value < 10:
                s += " "+str(value)+"  "
            elif value < 100:
                s += " "+str(value)+" "
            elif value < 1000:
                s = " " +str(value)
            else:
                s += str(value)
            if self.blocked.get_player() == 1:
                s = '\x1b[6;30;42m' + s + '\x1b[0m'
            if self.blocked.get_player() == 2:
                s = '\x1b[0;30;41m' + s + '\x1b[0m'
        else:
            s = "    "
        return s


class Block:

    def __init__(self, player, x ,y):
        self.value = 2
        self.owned_by = player
        self.x_pos = x
        self.y_pos = y

    def mul_value(self):
        self.value = self.value * 2

    def get_value(self):
        return self.value

    def get_player(self):
        return self.owned_by

    def get_coords(self):
        return [self.x_pos,self.y_pos]

    def set_coords(self, lista):
        self.x_pos = lista[0]
        self.y_pos = lista[1]

    def get_x(self):
        return self.x_pos

    def get_y(self):
        return self.y_pos

    def value_to_string(self):
        # funkcja do printowania wartości
        s = ''
        s += str(self.value)
        return s


    def get_adress_to_move(self, dir):
        # 0 - w dół
        # 1 - lewo dół
        # 2 - lewo góra
        # 3 - góra
        # 4 - prawo góra
        # 5 - prawo dół
        directions = []
        if self.x_pos < 4:
            directions = [[0,+1],[-1,0],[-1,-1],[0,-1],[+1,0],[+1,+1]]
        elif self.x_pos > 4:
            directions = [[0,+1],[-1,+1],[-1,0],[0,-1],[+1,-1],[+1,0]]
        else:
            directions = [[0,+1],[-1,0],[-1,-1],[0,-1],[+1,-1],[+1,0]]
        get_dir = directions[dir]
        new_x = get_dir[0]+self.x_pos
        new_y = get_dir[1]+self.y_pos
        if new_x<0 or new_y<0 or new_x>8:
            return False, [new_x,new_y]
        if new_x < 5:
            if new_y-new_x > 4:
                return False, [new_x,new_y]
        if (new_x == 5 and new_y>7) or (new_x == 6 and new_y>6) or (new_x == 7 and new_y>5) or (new_x == 8 and new_y>4):
            return False,[new_x,new_y]
        return True, [new_x,new_y]

offsetX = 260
offsetY = 40
middle = [[[offsetX, offsetY], [4, 0]],
          [[offsetX-45, offsetY+26], [3, 0]],
          [[offsetX+45, offsetY+26], [5, 0]],
          [[offsetX-90, offsetY+52], [2, 0]],
          [[offsetX, offsetY+52], [4, 1]],
          [[offsetX+90, offsetY+52], [6, 0]],
          [[offsetX-135, offsetY+78], [1, 0]],
          [[offsetX-45, offsetY+78], [3, 1]],
          [[offsetX+45, offsetY+78], [5, 1]],
          [[offsetX+135, offsetY+78], [7, 0]],
          [[offsetX-180, offsetY+104], [0, 0]],
          [[offsetX-90, offsetY+104], [2, 1]],
          [[offsetX, offsetY+104], [4, 2]],
          [[offsetX+90, offsetY+104], [6, 1]],
          [[offsetX+180, offsetY+104], [8, 0]],
          [[offsetX-135, offsetY+130], [1, 1]],
          [[offsetX-45, offsetY+130], [3, 2]],
          [[offsetX+45, offsetY+130], [5, 2]],
          [[offsetX+135, offsetY+130], [7, 1]],
          [[offsetX-180, offsetY+156], [0, 1]],
          [[offsetX-90, offsetY+156], [2, 2]],
          [[offsetX, offsetY+156], [4, 3]],
          [[offsetX+90, offsetY+156], [6, 2]],
          [[offsetX+180,offsetY+156], [8, 1]],
          [[offsetX-135, offsetY+182], [1, 2]],
          [[offsetX-45, offsetY+182], [3, 3]],
          [[offsetX+45, offsetY+182], [5, 3]],
          [[offsetX+135, offsetY+182], [7, 2]],
          [[offsetX-180, offsetY+208], [0, 2]],
          [[offsetX-90, offsetY+208], [2, 3]],
          [[offsetX, offsetY+208], [4, 4]],
          [[offsetX+90, offsetY+208], [6, 3]],
          [[offsetX+180, offsetY+208], [8, 2]],
          [[offsetX-135, offsetY+234], [1, 3]],
          [[offsetX-45, offsetY+234], [3, 4]],
          [[offsetX+45, offsetY+234], [5, 4]],
          [[offsetX+135, offsetY+234], [7, 3]],
          [[offsetX-180, offsetY+260], [0, 3]],
          [[offsetX-90, offsetY+260], [2, 4]],
          [[offsetX, offsetY+260], [4, 5]],
          [[offsetX+90, offsetY+260], [6, 4]],
          [[offsetX+180, offsetY+260], [8, 3]],
          [[offsetX-135, offsetY+286], [1, 4]],
          [[offsetX-45, offsetY+286], [3, 5]],
          [[offsetX+45, offsetY+286], [5, 5]],
          [[offsetX+135, offsetY+286], [7, 4]],
          [[offsetX-180, offsetY+312], [0, 4]],
          [[offsetX-90, offsetY+312], [2, 5]],
          [[offsetX, offsetY+312], [4, 6]],
          [[offsetX+90, offsetY+312], [6, 5]],
          [[offsetX+180, offsetY+312], [8, 4]],
          [[offsetX-135, offsetY+338], [1, 5]],
          [[offsetX-45, offsetY+338], [3, 6]],
          [[offsetX+45, offsetY+338], [5, 6]],
          [[offsetX+135, offsetY+338], [7, 5]],
          [[offsetX-90, offsetY+364], [2, 6]],
          [[offsetX, offsetY+364], [4, 7]],
          [[offsetX+90, offsetY+364], [6, 6]],
          [[offsetX-45, offsetY+390], [3, 7]],
          [[offsetX+45, offsetY+390], [5, 7]],
          [[offsetX, offsetY+416], [4, 8]]
          ]


def hex_corner(center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return QPoint(center[0] + size * math.cos(angle_rad),
                 center[1] + size * math.sin(angle_rad))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.game = None
        self.setWindowTitle("2048 coronedition by Filip Flis")
        self.setGeometry(300, 300, 520, 600)
        self.setMinimumWidth(520)
        self.setMinimumHeight(600)
        self.setButton("Nowa Gra!",self.start, offsetX-140, offsetY+450)
        self.setButton("Wyjdz!", self.quiteApp, offsetX+60, offsetY+450)


    def setButton(self,msg,action,x,y):
        btn1 = QPushButton(msg, self)
        btn1.move(x,y)
        btn1.clicked.connect(action)

    def start(self):
        self.game = Game()
        self.update()

    def quiteApp(self):
        userInfo = QMessageBox.question(self, "RLY?", "Chcesz wyjść?", QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            myApp.quit()
        elif userInfo==QMessageBox.No:
            pass

    def keyPressEvent(self, event):
        pressed = event.key()
        if pressed == Qt.Key_Q:
            self.game.moveQT(3)
            self.update()
        elif pressed == Qt.Key_W:
            self.game.moveQT(4)
            self.update()
        elif pressed == Qt.Key_E:
            self.game.moveQT(5)
            self.update()
        elif pressed == Qt.Key_A:
            self.game.moveQT(2)
            self.update()
        elif pressed == Qt.Key_S:
            self.game.moveQT(1)
            self.update()
        elif pressed == Qt.Key_D:
            self.game.moveQT(6)
            self.update()
        elif pressed == Qt.Key_U:
            self.game.moveQT(9)
            self.update()
        elif pressed == Qt.Key_I:
            self.game.moveQT(10)
            self.update()
        elif pressed == Qt.Key_O:
            self.game.moveQT(11)
            self.update()
        elif pressed == Qt.Key_J:
            self.game.moveQT(8)
            self.update()
        elif pressed == Qt.Key_K:
            self.game.moveQT(7)
            self.update()
        elif pressed == Qt.Key_L:
            self.game.moveQT(12)
            self.update()
        else:
            pass

    def paintEvent(self,event):
        painter = QPainter(self)
        if self.game is not None:
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            size = 30
            for element in middle:
                painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
                block = self.game.get_block(element[1][0],element[1][1])
                txt = ""
                if block is not None:
                    if block.get_player()==1:
                        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
                        txt = block.value_to_string()
                    else:
                        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                        txt = block.value_to_string()
                else:
                    painter.setBrush(QBrush(Qt.black, Qt.NoBrush))
                points = [hex_corner(element[0],size,0),
                    hex_corner(element[0],size,1),
                    hex_corner(element[0],size,2),
                    hex_corner(element[0], size, 3),
                    hex_corner(element[0], size, 4),
                    hex_corner(element[0], size, 5)]
                poly = QPolygon(points)
                painter.drawPolygon(poly)
                if txt != "":
                    painter.setPen(QPen(Qt.black, 10, Qt.SolidLine))
                    painter.drawText(QRectF(element[0][0]-30, element[0][1]-10,60,20),Qt.AlignHCenter|Qt.AlignVCenter, txt)
        else:
            painter.setPen(QPen(Qt.black, 10, Qt.SolidLine))
            painter.drawText(QRectF(100, 200, 320, 200), Qt.AlignHCenter | Qt.AlignTop,
                             "Gracze poruszają się następującymi klawiszami: \n "
                             "                    Gracz czerwony | Gracz Żółty \n "
                             "LewoGóra:          Q    |    U                       \n"
                             "Góra:                 W    |    I                    \n"
                             "PrawoGóra:           E    |     O        \n"
                             "LewoDół:            A     |     J               \n"
                             "Dół:                    S      |     K                 \n"
                             "PrawoDół:                 D     |      L     ")


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    window = Window()
    window.show()
    myApp.exec_()
    sys.exit()