import typing
from PyQt5.QtWidgets import QLabel,QLineEdit,QPlainTextEdit,QSpinBox,QLayout,QApplication,QVBoxLayout,QMainWindow,QPushButton, QWidget
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from PyQt5.QtCore import Qt

# Register QTextCursor as a metatype


import sys
import pymongo
import json
import random
import socket
import threading

class TCP_client():
    def __init__(self):
        # with open("config.txt","r") as file:
        #     settings = file.readline().split("#")
        # self.target_ip = settings[0]
        # self.target_port = int(settings[1])
        
        self.target_port = 9998
        
        
    def client_runner(self,target_ip):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, self.target_port))
        
        return client
        


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        
        uic.loadUi("mainUI.ui",self)
        self.Client = TCP_client()
        self.show()
        self.username_input : QLineEdit = self.findChild(QLineEdit,"username")
        
        self.textDisply : QPlainTextEdit = self.findChild(QPlainTextEdit,"DisplayText")
        self.inputText : QLineEdit = self.findChild(QLineEdit,"input")
        self.target_ip_input : QLineEdit = self.findChild(QLineEdit,"server_ip")
        self.Send_btn : QPushButton = self.findChild(QPushButton,"send")
        self.connect_btn : QPushButton = self.findChild(QPushButton,"connect")
        self.errText : QLabel = self.findChild(QLabel,"err_text")
        self.textDisply.setEnabled(False)
        self.inputText.setEnabled(False)
        self.Send_btn.setEnabled(False)
        
    def onTextEnter(self):
        if self.username_input.text() and self.target_ip_input.text():
            self.connect_btn.setEnabled(True)
        else:
            self.connect_btn.setEnabled(False)
        
        
        
    def connect_sever(self):
       
            try:
                self.errText.setText(" ")
                target_ip = self.target_ip_input.text()
                self.client = self.Client.client_runner(target_ip)
                if self.client != None:
                    self.textDisply.setEnabled(True)
                    self.inputText.setEnabled(True)
                    self.Send_btn.setEnabled(True)
                    
                    self.client.send(bytes("[+] "+self.username_input.text()+" " +"Connected!!","utf-8"))
                    self.temp_data = "[+] "+self.username_input.text()+" " +"Connected!!","utf-8"
                    threading.Thread(target=self.receving,args=(self.client,)).start()
                    
                else:
                    self.errText.setText("Error Connecting Target Server,Try Again")
                    self.textDisply.setEnabled(False)
                    self.inputText.setEnabled(False)
                    self.Send_btn.setEnabled(False)
            except Exception as err:
                self.errText.setText(str(err))
            
        

    def msg_send(self):
        
        self.to_sent =  "[" + self.username_input.text() + "]  " + self.inputText.text() 
        self.client.send(bytes(self.to_sent,"utf-8"))
        self.temp_data = self.to_sent
       
        
        self.inputText.clear()  
    
    
    def receving(self,client):
        try:
            while True:
                #client = self.Client.client_runner()
                recv = client.recv(4096).decode("utf-8")
                recv = str(recv)
                print(recv)
                    
                if recv != None:
                    #print(recv)
                    if self.temp_data == recv:
                        print("Own")
                        self.textDisply.insertPlainText(str(recv)+"\n")
                        cursor = self.textDisply.textCursor()
                        cursor.movePosition(QTextCursor.End)

                        # Move the cursor to the start of the block (line) that contains the inserted text
                        cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)

                         # Create a block format and set its alignment to right
                        block_format = QTextBlockFormat()
                        block_format.setAlignment(Qt.AlignRight)

                        # Set the block format to the current block (line) that contains the inserted text
                        cursor.setBlockFormat(block_format)
                    

                                                
                                        
                                            
                                            
                    else:
                        self.textDisply.insertPlainText(str(recv)+"\n")
                        
        except Exception as err:
                print(str(err))
      

                
            
             
            
##Real Working



app= QApplication(sys.argv)
window = UI()
window.setWindowTitle("X Chat")

window.Send_btn.clicked.connect(lambda : window.msg_send())
window.connect_btn.clicked.connect(lambda : window.connect_sever())
window.username_input.textChanged.connect(lambda : window.onTextEnter())
window.target_ip_input.textChanged.connect(lambda: window.onTextEnter())

sys.exit(app.exec())