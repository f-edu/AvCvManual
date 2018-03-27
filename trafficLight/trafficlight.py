#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort
# import PyQt5
from ui_mainwindow import Ui_MainWindow


class SerialSender(object):
    def __init__(self,
                 serial_port_combo_box,
                 device_id_spin_box,
                 power_spin_box,
                 status_bar):
        self._serial_port_combo_box = serial_port_combo_box
        self._device_id_spin_box = device_id_spin_box
        self._power_spin_box = power_spin_box
        self._status_bar = status_bar

    def red(self):
        self.set_command(100, 0, 0, 0, 0, 0xf0)

    def yellow(self):
        self.set_command(0, 100, 0, 0, 0, 0xf0)

    def green(self):
        self.set_command(0, 0, 100, 0, 0, 0xc0)

    def green_left_normal(self):
        self.set_command(0, 0, 0, 100, 0, 0xa0)

    def green_right_normal(self):
        self.set_command(0, 0, 0, 0, 100, 0x90)

    def green_left_inverted(self):
        self.set_command(0, 0, 0, 0, 100, 0xa0)

    def green_right_inverted(self):
        self.set_command(0, 0, 0, 100, 0, 0x90)

    def set_command(self, led_1, led_2, led_3, led_4, led_5, code):
        serial_port = QtSerialPort.QSerialPort()


        port_name = str(self._serial_port_combo_box.currentText())
        baud_rate = 115200
        
        serial_port.setPortName(port_name)
        serial_port.setBaudRate(baud_rate)

        if serial_port.open(QtCore.QIODevice.ReadWrite) != True:
            message = "Ошибка: не удалось открыть порт {}!".format(port_name)
            self._status_bar.showMessage(message)
            self._status_bar.update()
            return

        self._status_bar.showMessage("Посылаем команду светофору...")
        self._status_bar.update()

        command = "Ping\r\n"

        serial_port.write(bytes(command))
        serial_port.flush()
        sys.stderr.write(command)

        #TODO: process answer

        device_id = int(self._device_id_spin_box.value())
        power = int(self._power_spin_box.value())

        template = "Set {:d}, {:d} {:d} {:d} {:d} {:d}, {:d} 0x{:02X}\r\n"
        command = template.format(device_id,
                                  led_1,
                                  led_2,
                                  led_3,
                                  led_4, 
                                  led_5,
                                  power,
                                  code)

        serial_port.write(bytes(command))
        serial_port.flush()
        sys.stderr.write(command)

        #TODO: process answer

        self._status_bar.showMessage("Успех!")
        self._status_bar.update()

        serial_port.close()


def main(argv):
    application = QtWidgets.QApplication(argv)

    main_window = QtWidgets.QMainWindow()

    main_window.ui = Ui_MainWindow()
    main_window.ui.setupUi(main_window)

    status_bar = main_window.ui.statusbar

    combo_box = main_window.ui.serialPortComboBox

    ports = QtSerialPort.QSerialPortInfo.availablePorts()
    for port in ports:
        combo_box.addItem(port.portName())

    sender = SerialSender(main_window.ui.serialPortComboBox,
                          main_window.ui.deviceIdSpinBox,
                          main_window.ui.powerSpinBox,
                          status_bar)

    normal_red_button = main_window.ui.normalRedPushButton
    normal_yellow_button = main_window.ui.normalYellowPushButton
    normal_green_button = main_window.ui.normalGreenPushButton
    normal_green_left_button = main_window.ui.normalGreenLeftPushButton
    normal_green_right_button = main_window.ui.normalGreenRightPushButton

    inverted_red_button = main_window.ui.invertedRedPushButton
    inverted_yellow_button = main_window.ui.invertedYellowPushButton
    inverted_green_button = main_window.ui.invertedGreenPushButton
    inverted_green_left_button = main_window.ui.invertedGreenLeftPushButton
    inverted_green_right_button = main_window.ui.invertedGreenRightPushButton

    normal_red_button.clicked.connect(sender.red)
    normal_yellow_button.clicked.connect(sender.yellow)
    normal_green_button.clicked.connect(sender.green)
    normal_green_left_button.clicked.connect(sender.green_left_normal)
    normal_green_right_button.clicked.connect(sender.green_right_normal)

    inverted_red_button.clicked.connect(sender.red)
    inverted_yellow_button.clicked.connect(sender.yellow)
    inverted_green_button.clicked.connect(sender.green)
    inverted_green_left_button.clicked.connect(sender.green_left_inverted)
    inverted_green_right_button.clicked.connect(sender.green_right_inverted)

    main_window.show()

    application.exec_()


if __name__ == "__main__":
    main(sys.argv)
