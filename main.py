'''
Programa para leitura de dados remotamente

v1.0.0 - 14/12/2020

por:
Matheus Fay Soares
@matheusfay
'''

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QGroupBox, QLineEdit, QComboBox, \
    QMessageBox, QLabel
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QPixmap
import sys
import os

from datetime import datetime
from pythonping import ping
import socket

import pysftp
import paramiko


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi(os.getcwd() + "\\ui\Re8000_Bateria.ui", self)

        # Diretorios
        global imagens
        imagens = os.getcwd() + "\images\\"
        global docs
        docs = os.getcwd() + "\docs\\"
        global output_files
        output_files = os.getcwd() + "\output_files\\"


        self.setWindowIcon(QtGui.QIcon(imagens + 'icon.ico'))
        #self.setWindowTitle('Leitura Bateria - Embrasul RE8000')
        self.inicia_ui()

        # Variáveis Globais
        global ssh


        # Atribui funções ao clique do botão
        self.ping.clicked.connect(self.teste_ping)  # Ping
        self.start.clicked.connect(self.conectar)  # Start
        self.stop.clicked.connect(self.desconectar)  # Stop
        self.help.clicked.connect(self.abre_instrucao)  # Ajuda

        self.show()


    def inicia_ui(self):
        '''
        Função para inicializar os componentes da ui
        @matheusfay
        '''

        # Conexão
        self.janela = self.findChild(QLabel, "janela")
        pixmap2 = QPixmap(imagens + 'background.jpg')
        self.janela.setPixmap(pixmap2)


        self.ip = self.findChild(QLineEdit, "ip")
        self.porta = self.findChild(QLineEdit, "porta")
        self.status = self.findChild(QLabel, "status")

        self.start = self.findChild(QPushButton, "start")
        image_start = imagens + "button_start.png"
        self.start.setIcon(QtGui.QIcon(image_start))
        self.start.setIconSize(QtCore.QSize(81, 41))
        self.start.setStyleSheet("border: 0px; background: transparent;")

        self.stop = self.findChild(QPushButton, "stop")
        image_stop = imagens + "button_stop.png"
        self.stop.setIcon(QtGui.QIcon(image_stop))
        self.stop.setIconSize(QtCore.QSize(81, 41))
        self.stop.setStyleSheet("border: 0px; background: transparent;")

        self.ping = self.findChild(QPushButton, "ping")
        image_ping = imagens + "button_ping.png"
        self.ping.setIcon(QtGui.QIcon(image_ping))
        self.ping.setIconSize(QtCore.QSize(81, 41))
        self.ping.setStyleSheet("border: 0px; background: transparent;")

        self.help = self.findChild(QPushButton, "help")
        image_help = imagens + "help.png"
        self.help.setIcon(QtGui.QIcon(image_help))
        self.help.setIconSize(QtCore.QSize(31, 31))
        self.help.setStyleSheet("border: 0px; background: transparent;")

        self.serial = self.findChild(QLineEdit, "serial")
        self.firmware = self.findChild(QLineEdit, "firmware")
        self.sistema = self.findChild(QLineEdit, "sistema")

        #self.logo = self.findChild(QLabel, "logo")
        #pixmap = QPixmap(imagens + 'logo.png')
        #self.logo.setPixmap(pixmap)

        #Informações da Bateria
        self.carga_absoluta = self.findChild(QLineEdit, "carga_absoluta")
        self.carga_relativa= self.findChild(QLineEdit, "carga_relativa")
        self.tensao = self.findChild(QLineEdit, "tensao")
        self.corrente = self.findChild(QLineEdit, "corrente")
        self.tempo_descarga = self.findChild(QLineEdit, "tempo_descarga")
        self.tempo_carga = self.findChild(QLineEdit, "tempo_carga")

        #Alertas
        #Safety Status
        self.OTD = self.findChild(QLineEdit, "OTD")
        self.OTC = self.findChild(QLineEdit, "OTC")
        self.OCD = self.findChild(QLineEdit, "OCD")
        self.OCC = self.findChild(QLineEdit, "OCC")
        self.CUV = self.findChild(QLineEdit, "CUV")
        self.COV = self.findChild(QLineEdit, "COV")
        self.PF = self.findChild(QLineEdit, "PF")
        self.WDF = self.findChild(QLineEdit, "WDF")
        self.AOCD = self.findChild(QLineEdit, "AOCD")
        self.SCC = self.findChild(QLineEdit, "SCC")
        self.SCD = self.findChild(QLineEdit, "SCD")

        #PF Status
        self.VSHUT = self.findChild(QLineEdit, "VSHUT")
        self.SOPT = self.findChild(QLineEdit, "SOPT")
        self.SOCD = self.findChild(QLineEdit, "SOCD")
        self.SOCC = self.findChild(QLineEdit, "SOCC")
        self.AFE_P = self.findChild(QLineEdit, "AFE_P")
        self.AFE_C = self.findChild(QLineEdit, "AFE_C")
        self.DFF = self.findChild(QLineEdit, "DFF")
        self.DFETF = self.findChild(QLineEdit, "DFETF")
        self.CFETF = self.findChild(QLineEdit, "CFETF")
        self.CIM = self.findChild(QLineEdit, "CIM")
        self.SOTD = self.findChild(QLineEdit, "SOTD")
        self.SOTC = self.findChild(QLineEdit, "SOTC")
        self.SOV = self.findChild(QLineEdit, "SOV")
        self.PFIN = self.findChild(QLineEdit, "PFIN")

        #FET Status
        self.ZVCHG = self.findChild(QLineEdit, "ZVCHG")
        self.CHG = self.findChild(QLineEdit, "CHG")
        self.DSG = self.findChild(QLineEdit, "DSG")

    def teste_ping(self):
        '''
        Função para realizar o ping no IP do equipamento
        @matheusfay
        '''
        IP_TESTE = self.ip.text()

        ping_file = open(output_files + "ping_output.txt", "w")
        ping(IP_TESTE, verbose=True, out=ping_file)
        ping_file.close()

        try:
            ping_file = open(output_files + "ping_output.txt", "r")
            test_data_list = ping_file.readlines()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon(imagens + 'icon.ico'))
            msg.setText(f"Disparando IP [{IP_TESTE}]:")
            msg.setInformativeText(f"{test_data_list[0].rstrip()}")
            msg.setWindowTitle("Ping")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

            ping_file.close()
        except:
            return

    def conectar(self):
        '''
        Função para atualizar os valores via sftp
        @matheusfay

        Source:
        https://stackoverflow.com/questions/12295551/how-to-list-all-the-folders-and-files-in-the-directory-after-
        connecting-through
        '''
        sftpURL = str(self.ip.text())
        sftpUser = 'root'
        sftpPass = ''

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(sftpURL, username=sftpUser, password=sftpPass, timeout=5)
            self.status.setStyleSheet("color: rgb(35,142,35); border: 0px;")
            self.status.setText("Conectado")


            ftp = ssh.open_sftp()
            ftp.chdir('/media/mmcblk0p2/etc')
            files_etc = ftp.listdir()
            ftp.get('version.info', output_files + 'informacoes.txt')
            info_file = open(output_files + 'informacoes.txt', 'r')
            info_list = info_file.readlines()
            self.firmware.setText(info_list[0])
            self.sistema.setText(info_list[2])
            self.serial.setText(info_list[3])

            equipamento_conectado = 1

        except Exception as e:
            equipamento_conectado = 0
            self.status.setStyleSheet("border: 0px; color: rgb(255, 0, 0);")
            self.status.setText("Desconectado")

        ftp.chdir('/media/mmcblk0p2')
        files = ftp.listdir()
        ftp.get('info_bateria.txt', output_files + 'informacoes_bateria.txt')

        try:
            output_file = open(output_files + "informacoes_bateria.txt", "r")
            output_list = output_file.readlines()

            ssh.close()
        except:
            ssh.close()

        #Informações da Bateria
        absolute_charge = output_list[0]
        self.carga_absoluta.setText(f'{absolute_charge} %')

        relative_charge = output_list[1]
        self.carga_relativa.setText(f'{relative_charge} %')

        rt_empty = float(output_list[2])/60
        self.tempo_descarga.setText(f'{rt_empty} h')

        avg_full = float(output_list[3])/60
        self.tempo_carga.setText(f'{avg_full} h')

        voltage = float(output_list[4])/1000
        self.tensao.setText(f'{voltage} V')

        current = float(output_list[5])/1000
        self.corrente.setText(f'{current} A')

        #Alertas
        safety = format(int(output_list[6], 16), '0>16b')
        print(safety)
        self.set_safety(safety)

        pf = format(int(output_list[7], 16), '0>16b')
        print(pf)
        self.set_pf(pf)

        fet = format(int(output_list[8], 8), '0>8b')
        print(fet)
        self.set_fet(fet)

    def desconectar(self):
        '''
        Função para desconectar a comunicação
        @matheusfay
        '''
        equipamento_conectado = 0
        self.status.setStyleSheet("border: 0px; color: rgb(255, 0, 0);")
        self.status.setText("Desconectado")
        self.ip.setReadOnly(False)

        '''
        self.OTD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.OTC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.OCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.OCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.CUV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.COV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.PF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.WDF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.AOCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.VSHUT.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SOPT.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SOCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SOCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.AFE_P.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.AFE_C.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.DFF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.DFETF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.CFETF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.CIM.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SOTD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SOTC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.SOV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.PFIN.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.ZVCHG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.CHG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        self.DSG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background - color: rgb(168, 168, 168);")
        '''

    def abre_instrucao(self):
        '''
        Função para abrir o pdf de instruções de uso
        @matheusfay

        Source: https://stackoverflow.com/questions/19453338/opening-pdf-file
        '''
        filename = docs + "datasheet_bateria.pdf"
        os.startfile(filename)

    def set_safety(self, safety):
        if int(safety[0]) == 1:
            self.OTD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.OTD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[1]) == 1:
            self.OTC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.OTC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[2]) == 1:
            self.OCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.OCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[3]) == 1:
            self.OCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.OCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[8]) == 1:
            self.CUV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.CUV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[9]) == 1:
            self.COV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.COV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[10]) == 1:
            self.PF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.PF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[12]) == 1:
            self.WDF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.WDF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[13]) == 1:
            self.AOCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.AOCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[14]) == 1:
            self.SCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(safety[15]) == 1:
            self.SCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

    def set_pf(self, pf):
        if int(pf[1]) == 1:
            self.VSHUT.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.VSHUT.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[3]) == 1:
            self.SOPT.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SOPT.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[4]) == 1:
            self.SOCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SOCD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[5]) == 1:
            self.SOCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SOCC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[6]) == 1:
            self.AFE_P.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.AFE_P.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[7]) == 1:
            self.AFE_C.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.AFE_C.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[8]) == 1:
            self.DFF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.DFF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[9]) == 1:
            self.DFETF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.DFETF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[10]) == 1:
            self.CFETF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.CFETF.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[11]) == 1:
            self.CIM.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.CIM.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[12]) == 1:
            self.SOTD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SOTD.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[13]) == 1:
            self.SOTC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SOTC.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[14]) == 1:
            self.SOV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.SOV.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(pf[15]) == 1:
            self.PFIN.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.PFIN.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

    def set_fet(self, fet):
        if int(fet[4]) == 1:
            self.ZVCHG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.ZVCHG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(fet[5]) == 1:
            self.CHG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.CHG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

        if int(fet[6]) == 1:
            self.DSG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(255,0,0);")
        else:
            self.DSG.setStyleSheet("border: 1px solid black; color: rgb(0, 0, 0); background-color: rgb(35,142,35);")

app = QApplication(sys.argv)
window = UI()
app.exec_()