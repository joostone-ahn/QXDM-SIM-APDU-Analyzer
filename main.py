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

debug_mode = 0

class Basic_GUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.open_btn = QPushButton("Open")
        self.open_btn.setFont(CourierNewFont)
        self.open_btn.setFixedWidth(100)
        self.open_btn.setCheckable(False)

        self.open_btn.clicked.connect(self.load_msg)

        self.opened_label = QLabel()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.open_btn)
        hbox1.addWidget(self.opened_label)
        # hbox1.addStretch()

        self.comb_box = QComboBox()
        self.comb_box.addItem("SIM1")
        self.comb_box.addItem("SIM2")
        self.comb_box.setFixedWidth(100)
        self.comb_box.setFont(CourierNewFont)

        self.exe_btn = QPushButton("Execute")
        self.exe_btn.setFixedWidth(100)
        self.exe_btn.setCheckable(False)
        self.exe_btn.setFont(CourierNewFont)
        self.exe_btn.setDisabled(True)

        self.exe_btn.clicked.connect(self.exe_msg)

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedWidth(100)
        self.save_btn.setCheckable(False)
        self.save_btn.setFont(CourierNewFont)
        self.save_btn.setDisabled(True)

        self.save_btn.clicked.connect(self.save_msg)

        self.saved_label = QLabel()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.comb_box)
        hbox2.addWidget(self.exe_btn)
        hbox2.addWidget(self.save_btn)
        hbox2.addWidget(self.saved_label)
        hbox2.addStretch()

        self.SUM_label = QLabel()
        self.SUM_label.setText("Summary")
        self.SUM_label.setFont(CourierNewFont)
        self.SUM_list = QListWidget()
        self.SUM_list.setAutoScroll(True)
        self.SUM_list.setFixedHeight(500)
        self.SUM_list.setFixedWidth(530)
        self.SUM_list.setFont(CourierNewFont)
        SUM_vbox = QVBoxLayout()
        SUM_vbox.addWidget(self.SUM_label)
        SUM_vbox.addWidget(self.SUM_list)

        self.SUM_list.itemClicked.connect(self.clicked_rst)
        self.SUM_list.itemSelectionChanged.connect(self.clicked_rst)

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
        # hbox3.addStretch()

        self.SUM_File_label = QLabel()
        self.SUM_File_label.setText("EF_FILE SUMMARY (TBD)")
        self.SUM_File_label.setFont(CourierNewFont)
        self.SUM_File_list = QListWidget()
        self.SUM_File_list.setAutoScroll(True)
        self.SUM_File_list.setFixedWidth(530)
        self.SUM_File_list.setFont(CourierNewFont)
        SUM_File_vbox = QVBoxLayout()
        SUM_File_vbox.addWidget(self.SUM_File_label)
        SUM_File_vbox.addWidget(self.SUM_File_list)

        self.Prot_label = QLabel()
        self.Prot_label.setText("Protocol-Level Analysis")
        self.Prot_label.setFont(CourierNewFont)
        self.Prot_list = QTextBrowser()
        self.Prot_list.setFont(CourierNewFont)
        Prot_vbox = QVBoxLayout()
        Prot_vbox.addWidget(self.Prot_label)
        Prot_vbox.addWidget(self.Prot_list)

        hbox4 = QHBoxLayout()
        hbox4.addLayout(SUM_File_vbox)
        hbox4.addLayout(Prot_vbox)
        # hbox4.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(QLabel())
        vbox.addLayout(hbox3)
        vbox.addWidget(QLabel())
        vbox.addLayout(hbox4)
        vbox.addWidget(QLabel())
        vbox.addWidget(QLabel("Copyright 2022. JUSEOK AHN<ajs3013@lguplus.co.kr> all rights reserved."))
        # vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('Dual SIM APDU Analyzer (beta)')
        self.showMaximized()

    @pyqtSlot()
    def load_msg(self):
        self.SUM_list.clear()
        self.App_list.clear()
        self.Prot_list.clear()
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

        if debug_mode :
            print('[File Name]', opened_file)
            print('msg_start :', len(self.msg_start), self.msg_start)
            print('msg_end   :', len(self.msg_end), self.msg_end)
            print('msg_SN    :', len(self.msg_SN), self.msg_SN)
            print('msg_port  :', len(self.msg_port), self.msg_port)
            print('msg_type  :', len(self.msg_type), self.msg_type)
            print('msg_data  :', len(self.msg_data), self.msg_data)
            print()

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

        if debug_mode :
            print('[ SIM PORT', port_num, ']')
            print('exe_start  :', len(self.exe_start), self.exe_start)
            print('exe_end    :', len(self.exe_end), self.exe_end)
            print('exe_type   :', len(self.exe_type), self.exe_type)
            print('exe_data   :', len(self.exe_data), self.exe_data)
            print('')

        prot_input = self.exe_start, self.exe_end, self.exe_type, self.exe_data
        self.prot_start, self.prot_end, self.prot_type, self.prot_data = msg_prot.process(prot_input)

        if debug_mode :
            print('[ PROTOCOL LEVEL FILTER ]')
            print('prot_start :', len(self.prot_start), self.prot_start)
            print('prot_end   :', len(self.prot_end), self.prot_end)
            print('prot_type  :', len(self.prot_type), self.prot_type)
            print('prot_data  :', len(self.prot_data), self.prot_data)
            print()

        sum_input = self.msg_all, self.prot_start, self.prot_type, self.prot_data
        self.sum_rst, self.sum_log_ch, self.sum_log_ch_id, self.sum_read, self.sum_error = msg_sum.rst(sum_input)
        for n in self.sum_rst:
            self.SUM_list.addItem(n)

        if debug_mode :
            print('[ SUMMARY FILTER ]')
            print('sum_rst       :', len(self.sum_rst), self.sum_rst)
            print('sum_log_ch    :', len(self.sum_log_ch), self.sum_log_ch)
            print('sum_log_ch_id :', len(self.sum_log_ch_id), self.sum_log_ch_id)
            print('sum_read      :', len(self.sum_read), self.sum_read)
            print('sum_error     :', len(self.sum_error), self.sum_error)
            print()

        self.save_btn.setEnabled(True)

    @pyqtSlot()
    def clicked_rst(self):
        self.App_list.clear()
        self.Prot_list.clear()

        item_num = self.SUM_list.currentRow()

        prot_rst_input = self.msg_all, self.prot_start, self.prot_type, self.prot_data
        prot_rst = msg_prot.rst(prot_rst_input, item_num)
        prot_rst_show = ''
        for n in prot_rst:
            prot_rst_show +=n +'\n'
        self.Prot_list.setPlainText(prot_rst_show)

        app_rst_input1 = self.msg_all, self.prot_start, self.prot_end
        app_rst_input2 = self.prot_type, self.sum_log_ch, self.sum_log_ch_id
        app_rst = msg_app.rst(app_rst_input1, app_rst_input2, self.sum_read, item_num)
        app_rst_show = ''
        for n in app_rst:
            app_rst_show +=n +'\n'
        self.App_list.setPlainText(app_rst_show)

    @pyqtSlot()
    def save_msg(self):
        save_contents =''

        for n in range(len(self.sum_rst)):
            save_contents += '='*150 + '\n'
            save_contents += self.sum_rst[n] + '\n'
            save_contents += '='*150 + '\n'
            prot_rst_input = self.msg_all, self.prot_start, self.prot_type, self.prot_data, n
            prot_rst = msg_prot.rst(prot_rst_input)
            for m in prot_rst[1:]:
                save_contents += m +'\n'
            save_contents += '\n'

        save_path = QFileDialog.getSaveFileName(self,'Save file','',"Text files(*.txt)")
        fp = open(save_path[0], "w")
        fp.write(save_contents)
        fp.close()

        self.saved_label.setText(save_path[0])
        self.save_btn.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Basic_GUI()
    sys.exit(app.exec_())