import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui
import msg_item
import port
import msg_sum
import msg_app
import msg_prot

BoldFont = QtGui.QFont()
BoldFont.setBold(True)

CourierNewFont = QtGui.QFont()
CourierNewFont.setFamily("Courier New")

debug_mode = 1

class Basic_GUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.open_btn = QPushButton("File Open")
        self.open_btn.setFont(CourierNewFont)
        self.open_btn.setFixedWidth(150)
        self.open_btn.setCheckable(False)

        self.open_btn.clicked.connect(self.load_msg)

        self.opened_label = QLabel()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.open_btn)
        hbox1.addWidget(self.opened_label)
        hbox1.addStretch()

        self.comb_box = QComboBox()
        self.comb_box.addItem("SIM Port1")
        self.comb_box.addItem("SIM Port2")
        self.comb_box.setFixedWidth(150)
        self.comb_box.setFont(CourierNewFont)

        self.exe_btn = QPushButton("Execute")
        self.exe_btn.setFixedWidth(150)
        self.exe_btn.setCheckable(False)
        self.exe_btn.setFont(CourierNewFont)
        self.exe_btn.setDisabled(True)

        self.exe_btn.clicked.connect(self.exe_msg)


        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.comb_box)
        hbox2.addWidget(self.exe_btn)
        hbox2.addStretch()

        self.SUM_label = QLabel()
        self.SUM_label.setText("Summary")
        self.SUM_label.setFont(CourierNewFont)
        self.SUM_list = QListWidget()
        self.SUM_list.setAutoScroll(True)
        self.SUM_list.setFixedWidth(500)
        self.SUM_list.setFixedHeight(500)
        self.SUM_list.setFont(CourierNewFont)

        self.SUM_list.itemClicked.connect(self.clicked_rst)
        self.SUM_list.itemSelectionChanged.connect(self.clicked_rst)

        SUM_vbox = QVBoxLayout()
        SUM_vbox.addWidget(self.SUM_label)
        SUM_vbox.addWidget(self.SUM_list)

        self.App_label = QLabel()
        self.App_label.setText("Application-Level Analysis")
        self.App_label.setFont(CourierNewFont)
        self.App_list = QTextBrowser()
        self.App_list.setFixedHeight(500)
        self.App_list.setFont(CourierNewFont)
        App_vbox = QVBoxLayout()
        App_vbox.addWidget(self.App_label)
        App_vbox.addWidget(self.App_list)

        hbox3 = QHBoxLayout()
        hbox3.addLayout(SUM_vbox)
        hbox3.addLayout(App_vbox)

        self.Prot_label = QLabel()
        self.Prot_label.setText("Protocol-Level Analysis")
        self.Prot_label.setFont(CourierNewFont)
        self.Prot_list = QTextBrowser()
        self.Prot_list.setFixedHeight(250)
        self.Prot_list.setFont(CourierNewFont)
        Prot_vbox = QVBoxLayout()
        Prot_vbox.addWidget(self.Prot_label)
        Prot_vbox.addWidget(self.Prot_list)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(QLabel())
        vbox.addLayout(hbox3)
        vbox.addWidget(QLabel())
        vbox.addLayout(Prot_vbox)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('Dual SIM APDU Analyzer (beta)')
        self.showMaximized()

    @pyqtSlot()
    def load_msg(self):
        fname = QFileDialog.getOpenFileName(self,'Load file','',"Text files(*.txt)")
        opened_file = fname[0]
        if fname[0]:
            f = open(fname[0],'rt',encoding='UTF8') #https://m.blog.naver.com/yejoon3117/221058408177
            with f:
                try:
                    self.msg_all = f.readlines()
                except:
                    print("read fail")
                for n in range(len(self.msg_all)):
                    self.msg_all[n] = self.msg_all[n].replace('\n', '')
        self.opened_label.setText(opened_file)
        self.exe_btn.setEnabled(True)

        self.msg_start, self.msg_end, self.msg_SN, self.msg_port, self.msg_type, self.msg_data = msg_item.process(self.msg_all)

        if debug_mode == 1:
            print('[File Name]', opened_file)
            print('msg_start :', len(self.msg_start), self.msg_start)
            print('msg_end   :', len(self.msg_end), self.msg_end)
            print('msg_SN    :', len(self.msg_SN), self.msg_SN)
            print('msg_port  :', len(self.msg_port), self.msg_port)
            print('msg_type  :', len(self.msg_type), self.msg_type)
            print('msg_data  :', len(self.msg_data), self.msg_data)
            print()

        self.SUM_list.clear()
        self.App_list.clear()
        self.Prot_list.clear()

    @pyqtSlot()
    def exe_msg(self):
        self.SUM_list.clear()
        self.App_list.clear()
        self.Prot_list.clear()
        port_num = self.comb_box.currentIndex()+1

        port_index =[]
        for n in range(len(self.msg_port)):
            if self.msg_port[n] == port_num:
                port_index.append(n)

        port_input = self.msg_all, self.msg_start, self.msg_end, self.msg_SN, self.msg_type, self.msg_data
        self.exe_start, self.exe_end, self.exe_type, self.exe_data = port.process(port_input, port_index)

        if debug_mode == 1:
            print('[ SIM PORT', port_num, ']')
            print('exe_start  :', len(self.exe_start), self.exe_start)
            print('exe_end    :', len(self.exe_end), self.exe_end)
            print('exe_type   :', len(self.exe_type), self.exe_type)
            print('exe_data   :', len(self.exe_data), self.exe_data)
            print('')

        prot_input = self.exe_start, self.exe_end, self.exe_type, self.exe_data
        self.prot_start, self.prot_end, self.prot_type, self.prot_data = msg_prot.process(prot_input)

        if debug_mode == 1:
            print('[ PROTOCOL LEVEL FILTER ]')
            print('prot_start :', len(self.prot_start), self.prot_start)
            print('prot_end   :', len(self.prot_end), self.prot_end)
            print('prot_type  :', len(self.prot_type), self.prot_type)
            print('prot_data  :', len(self.prot_data), self.prot_data)
            print()

        sum_input = self.msg_all, self.prot_start, self.prot_end, self.prot_type, self.prot_data
        self.sum_rst = msg_sum.rst(sum_input)
        for n in self.sum_rst:
            self.SUM_list.addItem(n)

        if debug_mode == 1:
            print('[ SUMMARY FILTER ]')
            print('sum_rst    :', len(self.sum_rst), self.sum_rst)
            print()


    @pyqtSlot()
    def clicked_rst(self):
        self.App_list.clear()
        self.Prot_list.clear()

        item_num = self.SUM_list.currentRow()

        prot_rst_input = self.msg_all, self.prot_start, self.prot_type, self.prot_data, item_num
        prot_rst = msg_prot.rst(prot_rst_input)
        prot_rst_show = ''
        for n in prot_rst:
            prot_rst_show +=n +'\n'
        self.Prot_list.setPlainText(prot_rst_show)

        app_rst_input = self.msg_all, self.prot_start, self.prot_end, item_num
        app_rst = msg_app.rst(app_rst_input)
        app_rst_show = ''
        for n in app_rst:
            app_rst_show +=n +'\n'
        self.App_list.setPlainText(app_rst_show)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Basic_GUI()
    sys.exit(app.exec_())