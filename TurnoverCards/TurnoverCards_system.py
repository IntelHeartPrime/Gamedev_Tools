from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont

import sys

class MyWindow(QMainWindow):
    # config my own window
    def __init__(self):

        ''' data '''
        self.fire1_num = 0.0
        self.proability_num = 0.0
        self.fire2_num = 0.0
        self.consumedDiamonds_num = 0.0
        self.turnDiamonds_num = 0.0
        self.refreshDiamonds_num = 0.0
        ''' data '''

        super(MyWindow, self).__init__()
        self.resize(720, 1280)
        # 居中
        self.center()

        self.setWindowTitle("Cards Activity")
        self.setWindowIcon(QIcon("cards.png"))
        self.initUI()


    def initUI(self):

        # Side Bar
        self.statusBar().showMessage('Simulation of Cards Activity')

        # Lable - Fire1 Value
        self.fire1_lab = QtWidgets.QLabel(self)
        self.fire1_lab.resize(300, 40)
        self.fire1_lab.setText("🔥FIRE1 = "+str((self.fire1_num)))
        self.fire1_lab.move(47, 30)
        self.fire1_lab.setFont(QFont("SansSerif", 20))

        # Lable - Probability Value
        self.proability_lab = QtWidgets.QLabel(self)
        self.proability_lab.resize(300, 40)
        self.proability_lab.setText("PROBABILITY = "+str((self.proability_num)))
        self.proability_lab.move(47, 110)
        self.proability_lab.setFont(QFont("SansSerif", 20))

        # Lable - Fire2 Value
        self.fire2_lab = QtWidgets.QLabel(self)
        self.fire2_lab.resize(300, 40)
        self.fire2_lab.setText("🔥FIRE2 = "+str((self.fire2_num)))
        self.fire2_lab.move(47, 70)
        self.fire2_lab.setFont(QFont("SansSerif", 20))

        # Lable - Comsumed Diamonds Lable
        self.consumedDiamonds_lab = QtWidgets.QLabel(self)
        self.consumedDiamonds_lab.resize(300, 50)
        self.consumedDiamonds_lab.setText("CONSUMED DIAMONDS⇣")
        self.consumedDiamonds_lab.move(426, 34)
        self.consumedDiamonds_lab.setFont(QFont("SansSerif", 20))

        # Lable - Comsumed Diamonds Number
        self.consumedDiamondsNum_lab = QtWidgets.QLabel(self)
        self.consumedDiamondsNum_lab.resize(300, 50)
        self.consumedDiamondsNum_lab.setText("💎 "+ str((self.consumedDiamonds_num)))
        self.consumedDiamondsNum_lab.move(426, 80)
        self.consumedDiamondsNum_lab.setFont(QFont("SansSerif", 20))

        # Lable - turn diamonds
        self.turnDiamonds_lab = QtWidgets.QLabel(self)
        self.turnDiamonds_lab.resize(300, 50)
        self.turnDiamonds_lab.setText("TURN DIAMONDS: 💎 "+str((self.turnDiamonds_num)))
        self.turnDiamonds_lab.move(230, 720)
        self.turnDiamonds_lab.setFont(QFont("SansSerif", 20))

        # btn - Refresh
        self.refresh_btn = QtWidgets.QPushButton(self)
        self.refresh_btn.move(213,780)
        self.refresh_btn.resize(295,80)
        self.refresh_btn.setText("REFRESH 💎 " + str(self.refreshDiamonds_num))
        self.refresh_btn.clicked.connect(self.refreshBtnEvent)
        self.refresh_btn.setFont(QFont("SansSerif", 20))

        # btn - Reset
        self.reset_btn = QtWidgets.QPushButton(self)
        self.reset_btn.move(26,780)
        self.reset_btn.resize(91,72)
        self.reset_btn.setText("RESET")
        self.reset_btn.clicked.connect(self.resetBtnEvent)
        self.reset_btn.setFont(QFont("SansSerif", 20))

        ''' Cards Btns '''

        # 定义 Cards List
        self.cardsBtnsPos = []
        start_pos_x = 120
        start_pos_y = 180
        every_card_width = 150
        every_card_height = 160
        dis_x = 10
        dis_y = 10

        for x in range(3):
            for y in range(3):
                pos_x = start_pos_x + x*(every_card_width+dis_x)
                pos_y = start_pos_y + y*(every_card_height+dis_y)
                pos = [pos_x, pos_y]
                self.cardsBtnsPos.append(pos)

        # Card_btn1
        CardBtn1 = QtWidgets.QPushButton(self)
        CardBtn1.resize(every_card_width, every_card_height)
        CardBtn1.move(self.cardsBtnsPos[0][0], self.cardsBtnsPos[0][1])
        CardBtn1.setIcon(QIcon("cards.png"))
        CardBtn1.setText("1")
        CardBtn1.clicked.connect(self.cardEvent1)


        # Card_btn2
        CardBtn2 = QtWidgets.QPushButton(self)
        CardBtn2.resize(every_card_width, every_card_height)
        CardBtn2.move(self.cardsBtnsPos[1][0], self.cardsBtnsPos[1][1])
        CardBtn2.setIcon(QIcon("cards.png"))
        CardBtn2.setText("2")
        CardBtn2.clicked.connect(self.cardEvent2)

        # Card_btn3
        CardBtn3 = QtWidgets.QPushButton(self)
        CardBtn3.resize(every_card_width, every_card_height)
        CardBtn3.move(self.cardsBtnsPos[2][0], self.cardsBtnsPos[2][1])
        CardBtn3.setIcon(QIcon("cards.png"))
        CardBtn3.setText("3")
        CardBtn3.clicked.connect(self.cardEvent3)

        # Card_btn4
        CardBtn4 = QtWidgets.QPushButton(self)
        CardBtn4.resize(every_card_width, every_card_height)
        CardBtn4.move(self.cardsBtnsPos[3][0], self.cardsBtnsPos[3][1])
        CardBtn4.setIcon(QIcon("cards.png"))
        CardBtn4.setText("4")
        CardBtn4.clicked.connect(self.cardEvent4)

        # Card_btn5
        CardBtn5 = QtWidgets.QPushButton(self)
        CardBtn5.resize(every_card_width, every_card_height)
        CardBtn5.move(self.cardsBtnsPos[4][0], self.cardsBtnsPos[4][1])
        CardBtn5.setIcon(QIcon("cards.png"))
        CardBtn5.setText("5")
        CardBtn5.clicked.connect(self.cardEvent5)

        # Card_btn6
        CardBtn6 = QtWidgets.QPushButton(self)
        CardBtn6.resize(every_card_width, every_card_height)
        CardBtn6.move(self.cardsBtnsPos[5][0], self.cardsBtnsPos[5][1])
        CardBtn6.setIcon(QIcon("cards.png"))
        CardBtn6.setText("6")
        CardBtn6.clicked.connect(self.cardEvent6)

        # Card_btn7
        CardBtn7 = QtWidgets.QPushButton(self)
        CardBtn7.resize(every_card_width, every_card_height)
        CardBtn7.move(self.cardsBtnsPos[6][0], self.cardsBtnsPos[6][1])
        CardBtn7.setIcon(QIcon("cards.png"))
        CardBtn7.setText("7")
        CardBtn7.clicked.connect(self.cardEvent7)

        # Card_btn8
        CardBtn8 = QtWidgets.QPushButton(self)
        CardBtn8.resize(every_card_width, every_card_height)
        CardBtn8.move(self.cardsBtnsPos[7][0], self.cardsBtnsPos[7][1])
        CardBtn8.setIcon(QIcon("cards.png"))
        CardBtn8.setText("8")
        CardBtn8.clicked.connect(self.cardEvent8)

        # Card_btn9
        CardBtn9 = QtWidgets.QPushButton(self)
        CardBtn9.resize(every_card_width, every_card_height)
        CardBtn9.move(self.cardsBtnsPos[8][0], self.cardsBtnsPos[8][1])
        CardBtn9.setIcon(QIcon("cards.png"))
        CardBtn9.setText("9")
        CardBtn9.clicked.connect(self.cardEvent9)

        ''' Cards Btns '''

    def refreshBtnEvent(self):
        print("")

    def resetBtnEvent(self):
        print("")

    def cardEvent1(self):
        print("1")

    def cardEvent2(self):
        print("2")

    def cardEvent3(self):
        print("3")

    def cardEvent4(self):
        print("4")

    def cardEvent5(self):
        print("5")

    def cardEvent6(self):
        print("6")

    def cardEvent7(self):
        print("7")

    def cardEvent8(self):
        print("8")

    def cardEvent9(self):
        print("9")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())







def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec())


window()



