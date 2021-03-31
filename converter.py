# Владелец интеллектуальной собственности и разработчик данного программного обеспечения: Лошкарев Вадим Игоревич

#Указатель версии ПО (для заставки и раздела Информация)
version = "Версия программы: 2.1"

import csv
from datetime import datetime, date, time, timedelta
#import random
import os
import errno
import res_rc
import sys

import start_logo_conv  #модуль заставки
import csv_to_xml  #модуль главного окна PyQt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDate, QDateTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QToolTip, QPushButton, QApplication, QMessageBox, QAction
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QPalette

class Logo(QtWidgets.QWidget, start_logo_conv.Ui_Form):
    def __init__(self, parent=None):
        super(Logo, self).__init__(parent)

        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #Указатель версии ПО (для заставки и раздела Информация)
        self.label_2.setText(version)

        self.show()
        self.value = 0
        while self.value <= 400000:
            self.value += 1
            QtWidgets.QApplication.processEvents()
        self.close()

class main_window(QMainWindow, csv_to_xml.Ui_MainWindow):

    data = []
    dict = {}

    def __init__(self, parent = None):
        super(main_window, self).__init__()
        self.setupUi(self)

        self.lineEdit.setPlaceholderText('Выберите CSV-файл')
        self.lineEdit_2.setPlaceholderText((f"Путь сохранения по-умолчанию: {os.getcwd()}"))
        self.folder = os.getcwd()
        self.folder_xml = os.getcwd()
        self.pushButton_3.setEnabled(False)

        self.progressBar.setVisible(False)
        self.pushButton.clicked.connect(self.choose_file)            #Выбор файла

        self.pushButton_2.clicked.connect(self.choose_folder)
        self.pushButton_3.clicked.connect(self.do_convert)
        self.action.triggered.connect(self.info_page)
        self.action_3.triggered.connect(self.close)

    def info_page(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setText("Программное обеспечение: Конвертер файлов из формата CSV в формат XML")
        msg.setInformativeText(f"Разработчик: ФГУП \"ВНИИМС\"\nРаспространяется на безвозмездной основе\n{version}\n\nТехническая поддержка: fgis2@gost.ru")
        okButton = msg.addButton('Закрыть', QMessageBox.AcceptRole)
        msg.exec()

    def csv_reader(self, file_obj):
        """
        Read a csv file
        """
        reader = csv.reader(file_obj)
        for row in reader:
            row_1 = (' '.join(row))
            self.data.append(row_1.split(';'))
        return self.data

    def create_dict(self, csv_list):
        for n in range(len(csv_list[0])):
            self.dict[csv_list[0][n]] = csv_list[1][n]
        return self.dict

    def do_convert(self):
        self.pushButton.setVisible(False)
        csv_path = self.file
        file_name = os.path.splitext(self.filename_csv)[0]

        try:
            with open(csv_path, "r", encoding='utf-8') as f_obj:
                csv_list = self.csv_reader(f_obj)
                TOTAL_RESULTS = len(csv_list)-1

        except UnicodeDecodeError:
            with open(csv_path, "r") as f_obj:
                csv_list = self.csv_reader(f_obj)
                TOTAL_RESULTS = len(csv_list)-1


        #Количество записей о поверках СИ в одной заявке (не более 5000 записей)
        RESULTS_IN_APP = int(self.spinBox.text())

        parts = TOTAL_RESULTS // RESULTS_IN_APP # Вычисление количества заявок (Общее количество заявок делится без остатка на желаемое количество в одной заявке)
        if TOTAL_RESULTS % RESULTS_IN_APP != 0: # Если остаток от деления заявок на части не равен 0, то количество заявок увеличивается на 1.
            parts += 1

        set_progress = 0
        progress_value = 100 / (TOTAL_RESULTS / RESULTS_IN_APP)
        self.progressBar.setVisible(True)

        for j in range(parts):
            error = ''
            if TOTAL_RESULTS <= RESULTS_IN_APP:
                try:
                    self.converter(csv_list, file_name, TOTAL_RESULTS, j + 1)
                except (KeyError, PermissionError):
                    self.statusBar().showMessage('Ошибка, неверный формат данных в CSV')
                    error = 'True'
                except ValueError as exp:
                    self.statusBar().showMessage(str(exp))
                    error = 'True'
            elif TOTAL_RESULTS > RESULTS_IN_APP:
                try:
                    self.converter(csv_list, file_name, RESULTS_IN_APP, j + 1)
                    TOTAL_RESULTS -= RESULTS_IN_APP
                except (KeyError, PermissionError):
                    self.statusBar().showMessage('Ошибка, неверный формат данных в CSV')
                    error = 'True'
                except ValueError as exp:
                    self.statusBar().showMessage(str(exp))
                    error = 'True'

            set_progress += progress_value
            if set_progress > 100:
                set_progress = 100
            self.progressBar.setValue(round(set_progress))

        if error != 'True':
            self.statusBar().showMessage('Конвертирование файла завершено')
            self.spinBox.setValue(1)

        self.pushButton.setVisible(True)
        self.progressBar.setVisible(False)

        self.lineEdit.setText('')
        self.lineEdit.setPlaceholderText('Выберите CSV-файл')
        self.file = ''
        self.pushButton_3.setEnabled(False)
        self.data = []
        self.dict = {}


    def choose_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Выбрать CSV-файл", '*.csv')[0]
        if self.file != '':
            self.pushButton_3.setEnabled(True)
            self.statusBar().clearMessage()
        self.filename_csv = os.path.basename(self.file)
        self.lineEdit.setText(self.filename_csv)

        return self.filename_csv, self.file

    def choose_folder(self):
        self.folder_xml = QFileDialog.getExistingDirectory(self, "Каталог сохранения заявок")
        self.lineEdit_2.setText(self.folder_xml)
        return self.folder_xml

    def converter(self, csv_data, xml_name, result, part):

        self.data_for_xml = self.create_dict(csv_data)
        #Для контроля использую Условный шифр знака поверки, тип поверки и калибровку, если таких ключа нет в словаре, формат файла не совпадает
        signCipher_element = self.data_for_xml["signCipher"].upper()
        typePov = self.data_for_xml["type"]

        if self.folder_xml != self.folder:
            self.folder = self.folder_xml

        try:
            self.path_for_files = self.folder + '/' + xml_name
            os.makedirs(self.path_for_files)
        except OSError:
            self.path_for_files = self.folder + '/' + xml_name

        #Префикс названия файла
        prefix = f'{xml_name}_'

        date_stamp = datetime.now().strftime("%Y%m%d%H%M")

        #Название файла
        self.name_of_file = f'{date_stamp}_{prefix}записей_{str(result)}_part_{part}.xml'

        FileFullPath = os.path.join(self.path_for_files, self.name_of_file)  #Путь сохранения файла

        with open (FileFullPath, 'w', encoding='utf-8') as sample:

            header_1 = f'<?xml version="1.0" encoding="utf-8" ?>\n'
            header_2 = f'<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-06-19">\n'
            header = header_1 + header_2
            sample.write(header)

        with open (FileFullPath, 'a', encoding='utf-8') as sample_body:

            for i in range(result):

                self.data_for_xml = self.create_dict(csv_data)

                #Условный шифр знака поверки
                if self.data_for_xml["signCipher"].upper() != '':
                    signCipher_element = self.data_for_xml["signCipher"].upper()
                else:
                    raise ValueError("Не заполнено поле условный шифр")

                #Модификация СИ и Тип СИ
                if self.data_for_xml['mitypeNumber'] != '':
                    mitypeNumber = self.data_for_xml['mitypeNumber']
                else:
                    raise ValueError("Не заполнено поле Тип СИ")

                if self.data_for_xml['modification'] != '':
                    modification = self.data_for_xml['modification']
                else:
                    raise ValueError("Не заполнено поле Модификация")

                manufactureNum = self.data_for_xml['manufactureNum']         #Заводской номер СИ
                inventoryNum = self.data_for_xml['inventoryNum']             #Инвентарный номер СИ (Букв-цифр обозн)
                manufactureYear_csv = self.data_for_xml['manufactureYear']   #Дата производства СИ

                result_start = f'<gost:result>\n'
                miInfo_start = f'<gost:miInfo>\n'
                singleMI_start = f'<gost:singleMI>\n'
                mitypeNumber = f'<gost:mitypeNumber>{mitypeNumber}</gost:mitypeNumber>\n'

                if manufactureNum != '' and inventoryNum == '':
                    manufactureNum = f'<gost:manufactureNum>{manufactureNum}</gost:manufactureNum>\n'
                elif manufactureNum == '' and inventoryNum != '':
                    manufactureNum = f'<gost:inventoryNum>{inventoryNum}</gost:inventoryNum>\n'
                elif manufactureNum != '' and inventoryNum != '':
                    raise ValueError("Заполнены два поля Зав. № и БЦО одновременно")
                elif manufactureNum == '' and inventoryNum == '':
                    raise ValueError("Не заполнено ни одно поле Зав. № или БЦО")

                manufactureYear = f'<gost:manufactureYear>{manufactureYear_csv}</gost:manufactureYear>\n'
                modification = f'<gost:modification>{modification}</gost:modification>\n'
                singleMI_close = f'</gost:singleMI>\n'
                miInfo_close = f'</gost:miInfo>\n'

                if manufactureYear_csv != '':
                    miInfo = miInfo_start + singleMI_start + mitypeNumber + manufactureNum + manufactureYear + modification + singleMI_close + miInfo_close
                else:
                    miInfo = miInfo_start + singleMI_start + mitypeNumber + manufactureNum + modification + singleMI_close + miInfo_close

                if self.data_for_xml['applicable'] != '':
                    verification_marker = self.data_for_xml['applicable']  # (пригодно, непригодно)
                else:
                    raise ValueError("Не заполнено поле Пригодность")

                try:
                    if self.data_for_xml['vrfDate'] != '':
                        vrfDate = datetime.strptime(self.data_for_xml['vrfDate'], '%d.%m.%Y').date()       #Отформатированная дата поверки
                    else:
                        raise ValueError("Не заполнено поле Дата поверки")

                    if self.data_for_xml['validDate'] != '':
                        validDate = datetime.strptime(self.data_for_xml['validDate'], '%d.%m.%Y').date() #Отформатированная дата действия поверки
                    else:
                        self.statusBar().showMessage('Не заполнено поле Действительна до (validDate)')
                        validDate = self.data_for_xml['validDate']
                except ValueError:
                    if self.data_for_xml['vrfDate'] != '':
                        vrfDate = datetime.strptime(self.data_for_xml['vrfDate'], '%Y-%m-%d').date()       #Отформатированная дата поверки
                    else:
                        raise ValueError("Не заполнено поле Дата поверки")

                    if self.data_for_xml['validDate'] != '':
                        validDate = datetime.strptime(self.data_for_xml['validDate'], '%Y-%m-%d').date() #Отформатированная дата действия поверки
                    else:
                        self.statusBar().showMessage('Не заполнено поле Действительна до (validDate)')
                        validDate = self.data_for_xml['validDate']

                if verification_marker.lower() == 'пригодно':
                    signCipher = f'<gost:signCipher>{signCipher_element}</gost:signCipher>\n'
                    if self.data_for_xml["miOwner"] != '':
                        miOwner = f"<gost:miOwner>{self.data_for_xml['miOwner']}</gost:miOwner>\n"
                        #print('miOwner', miOwner)
                    else:
                        raise ValueError("Не заполнено поле Владелец СИ")
                    vrfDate = f'<gost:vrfDate>{vrfDate}</gost:vrfDate>\n'
                    validDate = f'<gost:validDate>{validDate}</gost:validDate>\n'
                    if self.data_for_xml["type"] != '':
                        typePov = f'<gost:type>{self.data_for_xml["type"]}</gost:type>\n'
                    else:
                        raise ValueError("Не заполнено поле Тип поверки")
                    if self.data_for_xml['calibration'] != '':
                        if self.data_for_xml['calibration'].lower() == 'да':
                            calibrate = 'true'
                            calibration = f'<gost:calibration>{calibrate}</gost:calibration>\n'
                        elif self.data_for_xml['calibration'].lower() == 'нет':
                            calibrate = 'false'
                            calibration = f'<gost:calibration>{calibrate}</gost:calibration>\n'
                    else:
                        raise ValueError("Не заполнено поле Результаты калибровки")

                    valid = signCipher + miOwner + vrfDate + validDate + typePov + calibration

                    #Знак поверки в паспорте
                    if self.data_for_xml['signPass'].lower() == 'да':
                        signPass = 'true'
                    else:
                        signPass = 'false'

                    #Знак поверки на СИ
                    if self.data_for_xml['signMi'].lower() == 'да':
                        signMi = 'true'
                    else:
                        signMi = 'false'

                    applicable_start = f'<gost:applicable>\n'
                    stickerNum = ''
                    if self.data_for_xml['stickerNum'] != '':
                        stickerNum = f'<gost:stickerNum>{self.data_for_xml["stickerNum"]}</gost:stickerNum>\n'
                    signPass = f'<gost:signPass>{signPass}</gost:signPass>\n'
                    signMi = f'<gost:signMi>{signMi}</gost:signMi>\n'
                    applicable_close = f'</gost:applicable>\n'
                    verification_res = applicable_start + stickerNum + signPass + signMi + applicable_close

                elif verification_marker.lower() == 'непригодно' or self.data_for_xml['reasons'] != '':
                    signCipher = f'<gost:signCipher>{signCipher_element}</gost:signCipher>\n'
                    if self.data_for_xml["miOwner"] != '':
                        miOwner = f'<gost:miOwner>{self.data_for_xml["miOwner"]}</gost:miOwner>\n'
                    else:
                        raise ValueError("Не заполнено поле Владелец СИ")

                    vrfDate = f'<gost:vrfDate>{vrfDate}</gost:vrfDate>\n'

                    if self.data_for_xml["type"] != '':
                        typePov = f'<gost:type>{self.data_for_xml["type"]}</gost:type>\n'
                    else:
                        raise ValueError("Не заполнено поле Тип поверки")
                    if self.data_for_xml['calibration'] != '':
                        if self.data_for_xml['calibration'].lower() == 'да':
                            calibrate = 'true'
                            calibration = f'<gost:calibration>{calibrate}</gost:calibration>\n'
                        elif self.data_for_xml['calibration'].lower() == 'нет':
                            calibrate = 'false'
                            calibration = f'<gost:calibration>{calibrate}</gost:calibration>\n'
                    else:
                        raise ValueError("Не заполнено поле Результаты калибровки")

                    valid = signCipher + miOwner + vrfDate + typePov + calibration

                    inapplicable_start = f'<gost:inapplicable>\n'
                    if self.data_for_xml["reasons"] != '':
                        reasons = f'<gost:noticeNum>{self.data_for_xml["reasons"]}</gost:noticeNum>\n' #Причина непригодности СИ
                    else:
                        raise ValueError("Не заполнено поле Причина непригодности")
                    
                    inapplicable_close = f'</gost:inapplicable>\n'
                    verification_res = inapplicable_start + reasons + inapplicable_close

                if self.data_for_xml["docTitle"] != '':
                    docTitle = f'<gost:docTitle>{self.data_for_xml["docTitle"]}</gost:docTitle>\n' #Причина непригодности СИ
                else:
                    raise ValueError("Не заполнено поле Методика поверки")

                metrologist = ''
                if self.data_for_xml['metrologist'] != '':
                    metrologist = f'<gost:metrologist>{self.data_for_xml["metrologist"]}</gost:metrologist>\n'

                means_start = f'<gost:means>\n'

                npe = ''
                if self.data_for_xml['npe'] != '':
                    text = self.data_for_xml['npe'].rstrip('|')
                    text = text.split('|')
                    npe_list = ''
                    npe_start = f'<gost:npe>\n'
                    for t in text:
                        if t != '':
                            npe_number = f'<gost:number>{t}</gost:number>\n'
                            npe_list += npe_number
                    npe_close = f'</gost:npe>\n'

                    npe = npe_start + npe_list + npe_close

                uve = ''
                if self.data_for_xml['uve'] != '':
                    text = self.data_for_xml['uve'].rstrip('|')
                    text = text.split('|')
                    uve_list = ''
                    uve_start = f'<gost:uve>\n'
                    for t in text:
                        if t != '':
                            uve_number = f'<gost:number>{t}</gost:number>\n'
                            uve_list += uve_number
                    uve_close = f'</gost:uve>\n'

                    uve = uve_start + uve_list + uve_close

                ses = ''
                if self.data_for_xml['ses'] != '':
                    text = self.data_for_xml['ses'].rstrip('|')
                    text = text.split('|')
                    count = 1
                    se_list = ''
                    ses_start = f'<gost:ses>\n'
                    for i in range(len(text)):
                        text_list = text[i].split('*')
                        for t in text_list:
                            if count == 1:
                                se_start = f'<gost:se>\n'
                                typeNum = f'<gost:typeNum>{t}</gost:typeNum>\n'
                                se_many = se_start + typeNum
                            if count == 2:
                                ses_manufactureYear = f'<gost:manufactureYear>{t}</gost:manufactureYear>\n'
                                se_many = ses_manufactureYear
                            if count == 3:
                                ses_manufactureNum = f'<gost:manufactureNum>{t}</gost:manufactureNum>\n'
                                count = 0
                                se_close = f'</gost:se>\n'
                                se_many = ses_manufactureNum + se_close
                            count += 1

                            se_list += se_many
                    ses_close = f'</gost:ses>\n'
                    ses = ses_start + se_list + ses_close

                mieta = ''
                if self.data_for_xml['mieta'] != '':
                    text = self.data_for_xml['mieta'].rstrip('|')
                    text = text.split('|')
                    mieta_list = ''
                    mieta_start = f'<gost:mieta>\n'
                    for t in text:
                        if t != '':
                            mieta_number = f'<gost:number>{t}</gost:number>\n'
                            mieta_list += mieta_number
                    mieta_close = f'</gost:mieta>\n'

                    mieta = mieta_start + mieta_list + mieta_close

                mis = ''
                if self.data_for_xml['mis'] != '':
                    text = self.data_for_xml['mis'].rstrip('|')
                    text = text.split('|')
                    count = 1
                    mi_list = ''
                    mis_start =	f'<gost:mis>\n'
                    for i in range(len(text)):
                        text_list = text[i].split('*')
                        for t in text_list:
                            if count == 1:
                                mi_start = f'<gost:mi>\n'
                                typeNum = f'<gost:typeNum>{t}</gost:typeNum>\n'
                                mi_many = mi_start + typeNum
                            if count == 2:
                                mieta_manufactureNum = f'<gost:manufactureNum>{t}</gost:manufactureNum>\n'
                                count = 0
                                mi_close = f'</gost:mi>\n'
                                mi_many = mieta_manufactureNum + mi_close
                            count += 1

                            mi_list += mi_many
                    mis_close =	f'</gost:mis>\n'
                    mis = mis_start + mi_list + mis_close

                means_close = f'</gost:means>\n'

                conditions_start = f'<gost:conditions>\n'
                if self.data_for_xml["temperature"] != '':
                    temperature = f'<gost:temperature>{self.data_for_xml["temperature"]}</gost:temperature>\n'
                else:
                    raise ValueError("Не заполнено поле Температура")
                if self.data_for_xml["pressure"] != '':
                    pressure = f'<gost:pressure>{self.data_for_xml["pressure"]}</gost:pressure>\n'
                else:
                    raise ValueError("Не заполнено поле Давление")
                if self.data_for_xml["hymidity"] != '':
                    hymidity = f'<gost:hymidity>{self.data_for_xml["hymidity"]}</gost:hymidity>\n'
                else:
                    raise ValueError("Не заполнено поле Влажность")

                other = ''
                if self.data_for_xml['other'] != '':
                    other = f'<gost:other>{self.data_for_xml["other"]}</gost:other>\n'
                conditions_close = f'</gost:conditions>\n'

                structure = ''
                if self.data_for_xml['structure'] != '':
                    structure = f'<gost:structure>{self.data_for_xml["structure"]}</gost:structure>\n'

                characteristics = ''
                if self.data_for_xml['characteristics'] != '':
                    characteristics = f'<gost:brief_procedure>\n<gost:characteristics>{self.data_for_xml["characteristics"]}</gost:characteristics>\n</gost:brief_procedure>\n'

                additional_info = ''
                if self.data_for_xml['additional_info'] != '':
                    additional_info = f'<gost:additional_info>{self.data_for_xml["additional_info"]}</gost:additional_info>\n'

                result_close = f'</gost:result>\n'

                body = result_start + miInfo + valid + verification_res + docTitle + metrologist + means_start + npe + uve + ses + mieta + mis + means_close + conditions_start + temperature + pressure + hymidity + other + conditions_close + structure + characteristics + additional_info + result_close
                sample_body.write(body)

                csv_data.remove(csv_data[1])

                self.data_for_xml.clear()


        with open (FileFullPath, 'a', encoding='utf-8') as sample:
            footer = f'</gost:application>\n'
            sample.write(footer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    Logo()
    ex = main_window()
    ex.show()
    app.exec()