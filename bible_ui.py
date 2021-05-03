'''
This code is written by Jiali Liang to provide quick access to bible verses within 3 seconds.

Users can define Chinese version, English version, and output w or w/o English verses.

Searching parameters will be saved to a file named: defaults.txt
the defaults.txt format will be:
T # Which Chinese character to use? Simplified or Traditional
True # Output verses with English or not
KJV # Which English version of bible to use
'''
##=============================================================
# commandline Code to convert UI file to python file
# pyuic5 -x file.ui -o file.py
##=============================================================
import codecs
import pyperclip
import pandas as pd
import convert as cvt
import argparse
import numpy as np
from opencc import OpenCC
import search_verse as sv
from PyQt5 import QtCore, QtGui, QtWidgets
import re
##=============================================================
# Global Variables
##=============================================================
global CN_Ver      # Default CN version T or S
global w_English   # Default using English or not
global EN_Ver      # Default EN version

##=============================================================
# Functions of commandline bible.py
##=============================================================
# Read default values from defaults.txt for search parameters
def read_defaults():
    global CN_Ver      # Default CN version T or S
    global w_English   # Default using English or not
    global EN_Ver      # Default EN version
    # read in default settings
    f = open("defaults.txt","r")
    defaults = f.readlines()
    CN_Ver = defaults[0][0]
    w_English = eval(defaults[1])
    EN_Ver = defaults[2][0:3]

# write default values to the defaults.txt
def write_defaults():
        f = open("defaults.txt","w")
        defaults = [CN_Ver,str(w_English),EN_Ver]
        for param in defaults:
            f.write(param + "\n")
        f.close()

# function determines which version Simplified or Traditional to be used
def read_text_ZH(var):
    if var == "S":
        text = 'simplified.txt'
        form = "GBK"
    elif var == "T":
        text ='triditional.txt'
        form ='utf-8'
    with codecs.open(text, 'U', form) as f:
        data = f.read()
        data = data.split("\n")
    return data

# Determine which English version to be used or not use English at all
def read_text_EN(var):
    if var == True:
        if EN_Ver == "ASV":
            bible = "ASV.txt"
        elif EN_Ver == "WEB":
            bible = "WEB.txt"
        elif EN_Ver == "NASB":
            bible = "NASB.txt"
        else:
            bible = "bible_KJV.txt"
        ASV = open(bible,"r+")
    elif var == False:
        ASV = ""
    return ASV


# This function search the bible verses in both Chinese and English (optional)
def search(data,ASV,string):
    matching = [s for s in data if str(string) in s]
    ZHEN = ""
    if len(matching) == 0:
        return ""
    for i in matching:
        # find the related english verse
        EN_verse = ZH2ENG_verse(ASV,i)
        # combine chinese and english verses
        ZHEN += i+"\n"+EN_verse+"\n"
    return ZHEN

# Find the English verse, else return empty string
def search_EN(data,string):
    string += " "
    for verse in data:
        if string in verse:
            return verse
    return ""


# Given a chinese bible verse, find the corresponding english verses
def ZH2ENG_verse(ASV,verse):
    # In the case of not searching English Version
    if (w_English == False):
        return ""
    ENG_book,ENG_verse = sv.sep_chapter(str.split(verse)[0])
    # becasue the book name table used triditional chinese, I have to convert them back to Traditional
    cc = OpenCC('s2t')
    ENG_book = cc.convert(ENG_book)
    verse2search_EN = cvt.CVT(ENG_book,"EN") +" "+ENG_verse
    ENG = str(search_EN(ASV,verse2search_EN))
    return ENG

# this function copies the code to your clipboard
def copy_paste(verses):
    # Copy the verses to the clip board
    pyperclip.copy(str(verses))
    spam = pyperclip.paste()
    return spam


#==============================================================
# UI codes
##=============================================================
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(759, 612)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verse_label = QtWidgets.QTextEdit(self.centralwidget)
        self.verse_label.setGeometry(QtCore.QRect(10, 20, 391, 541))
        self.verse_label.setTabletTracking(True)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.verse_label.setFont(font)
        self.verse_label.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.verse_label.setFrameShape(QtWidgets.QFrame.Box)
        self.verse_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.verse_label.setLineWidth(2)
        self.verse_label.setObjectName("verse_label")
        self.frame_setting = QtWidgets.QFrame(self.centralwidget)
        self.frame_setting.setGeometry(QtCore.QRect(410, 290, 341, 271))
        self.frame_setting.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_setting.setLineWidth(2)
        self.frame_setting.setObjectName("frame_setting")
        self.Trad_CH_label = QtWidgets.QLabel(self.frame_setting)
        self.Trad_CH_label.setGeometry(QtCore.QRect(210, 30, 121, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Trad_CH_label.setFont(font)
        self.Trad_CH_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Trad_CH_label.setObjectName("Trad_CH_label")
        self.horizontalSlider = QtWidgets.QSlider(self.frame_setting)
        self.horizontalSlider.setGeometry(QtCore.QRect(140, 60, 61, 21))
        self.horizontalSlider.setSingleStep(50)
        self.horizontalSlider.setPageStep(50)

        # Determine the slider location (Simplified or Traditional) based on default setting
        self.horizontalSlider.setSliderPosition(99)
        if CN_Ver == "S":
            self.horizontalSlider.setSliderPosition(0)

        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.sim_CH_label = QtWidgets.QLabel(self.frame_setting)
        self.sim_CH_label.setGeometry(QtCore.QRect(10, 30, 121, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.sim_CH_label.setFont(font)
        self.sim_CH_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sim_CH_label.setObjectName("sim_CH_label")
        self.checkbox_English = QtWidgets.QCheckBox(self.frame_setting)
        self.checkbox_English.setGeometry(QtCore.QRect(70, 150, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.checkbox_English.setFont(font)
        self.checkbox_English.setMouseTracking(False)
        self.checkbox_English.setFocusPolicy(QtCore.Qt.TabFocus)
        self.checkbox_English.setAcceptDrops(False)
        self.checkbox_English.setAutoFillBackground(False)
        self.checkbox_English.setIconSize(QtCore.QSize(40, 40))
        self.checkbox_English.setObjectName("checkbox_English")

        # Determine the status of checkbox of with_english based on default setting
        if w_English == True :
            self.checkbox_English.setChecked(True)
        else:
            self.checkbox_English.setChecked(False)

        self.combo_ENG_Version = QtWidgets.QComboBox(self.frame_setting)
        self.combo_ENG_Version.setGeometry(QtCore.QRect(50, 210, 231, 41))
        self.combo_ENG_Version.setObjectName("combo_ENG_Version")
        self.combo_ENG_Version.addItem("")
        self.combo_ENG_Version.addItem("")
        self.combo_ENG_Version.addItem("")
        self.frame_setting_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_setting_2.setGeometry(QtCore.QRect(410, 20, 341, 261))
        self.frame_setting_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_setting_2.setLineWidth(2)
        self.frame_setting_2.setObjectName("frame_setting_2")
        self.user_input = QtWidgets.QLineEdit(self.frame_setting_2)
        self.user_input.setGeometry(QtCore.QRect(30, 40, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.user_input.setFont(font)
        self.user_input.setObjectName("user_input")

        self.show_table = QtWidgets.QPushButton(self.frame_setting_2)
        self.show_table.setGeometry(QtCore.QRect(95, 160, 147, 32))
        self.show_table.setObjectName("show_table")

        self.Button_search = QtWidgets.QPushButton(self.frame_setting_2)
        self.Button_search.setGeometry(QtCore.QRect(90, 100, 161, 51))
        self.Button_search.setObjectName("Button_search")
        self.tips_label = QtWidgets.QLabel(self.frame_setting_2)
        self.tips_label.setGeometry(QtCore.QRect(10, 190, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setItalic(True)
        self.tips_label.setFont(font)
        self.tips_label.setTextFormat(QtCore.Qt.AutoText)
        self.tips_label.setIndent(1)
        self.tips_label.setObjectName("tips_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 759, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSearch = QtWidgets.QAction(MainWindow)
        self.actionSearch.setObjectName("actionSearch")
        self.actionAuthor = QtWidgets.QAction(MainWindow)
        self.actionAuthor.setObjectName("actionAuthor")
        self.actionInformation = QtWidgets.QAction(MainWindow)
        self.actionInformation.setObjectName("actionInformation")
        self.menuFile.addAction(self.actionSearch)
        self.menuWindow.addAction(self.actionInformation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ##=============================================================
        # Calling Trigger functions
        ##=============================================================
        self.actionSearch.triggered.connect(lambda: self.click_search(self.user_input.text()))
        self.Button_search.clicked.connect(lambda: self.click_search(self.user_input.text()))
        self.checkbox_English.clicked.connect(lambda: self.check_eng(self.checkbox_English.isChecked()))
        self.horizontalSlider.valueChanged.connect(lambda: self.check_CN_Ver(self.horizontalSlider.value()))
        self.show_table.clicked.connect(lambda: self.show_book_table())
        self.combo_ENG_Version.currentTextChanged.connect(lambda: self.check_EN_Ver(self.combo_ENG_Version.currentText()))
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bible Verse Search Tool"))
        self.verse_label.setText(_translate("MainWindow", "Your verses will be shown here! "))
        self.Trad_CH_label.setText(_translate("MainWindow", "Traditional\n"
"Chinese\n"
"繁"))
        self.sim_CH_label.setText(_translate("MainWindow", "Simplified\n"
"Chinese\n"
"简"))
        self.checkbox_English.setText(_translate("MainWindow", "  English Verse"))

        self.combo_ENG_Version.setItemText(0, _translate("MainWindow", "KJV - King James Version"))
        self.combo_ENG_Version.setItemText(1, _translate("MainWindow", "ASV - American Standard Version"))
        self.combo_ENG_Version.setItemText(2, _translate("MainWindow", "WEB - World English Bible"))
        self.combo_ENG_Version.setItemText(3, _translate("MainWindow", "NASB - New American Standard Bible"))
        # Set different default EN_version bible to use here
        if EN_Ver == "ASV":
            self.combo_ENG_Version.setCurrentText(_translate("MainWindow", "ASV - American Standard Version"))
        elif EN_Ver == "WEB":
            self.combo_ENG_Version.setCurrentText(_translate("MainWindow","WEB - World English Bible"))
        elif EN_Ver == "NASB":
            self.combo_ENG_Version.setCurrentText(_translate("MainWindow","NASB - New American Standard Bible"))
        else:
            self.combo_ENG_Version.setCurrentText(_translate("MainWindow", "KJV - King James Version"))
        self.user_input.setPlaceholderText(_translate("MainWindow", "Ex.  創 1 1 3"))
        self.show_table.setText(_translate("MainWindow", "Show Book Table"))
        self.Button_search.setText(_translate("MainWindow", "Search"))
        self.tips_label.setText(_translate("MainWindow", "Tips on search format: \n"
"1. Book Chapter Start Verse (optional: End Verse)\n"
"2. Each parameters are seperated by space"))
        self.menuFile.setTitle(_translate("MainWindow", "Function"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.actionSearch.setText(_translate("MainWindow", "Search"))
        self.actionSearch.setShortcut(_translate("MainWindow", "Return"))
        self.actionAuthor.setText(_translate("MainWindow", "Author"))
        self.actionInformation.setText(_translate("MainWindow", "Information"))


##=============================================================
# Trigger functions
##=============================================================
# Search Engine
    def click_search(self, search_key):
        # In the case of more than 4 or smaller than 3 variables
        # Return error message
        if len(search_key.split()) > 4 or len(search_key.split()) < 3:
            self.verse_label.setText("Please keep the correct format:\
            \n\nBook Chapter Start Verse (End Verse)\n\nExamples:\n太 2 2 4 \
            \n太 3 5 \n馬太福音 3 5 \nMatthew 2 2 4 \nMatthew 3 5\nMat 3 5\
            \n\nEach parameters are seperated by space")
            return

        # Split the Search key into diff variables
        book = str.split(search_key)[0]
        chapter = str.split(search_key)[1]
        begin_verse = str.split(search_key)[2]

        # Set up if there is only one verse search
        # End verse = begin verse
        if len(search_key.split()) == 3 :
            end_verse = begin_verse
        else:
            end_verse = str.split(search_key)[3]

        # Error checking to make sure chapter, begin verse, end verse is a valid digit
        if (chapter.isdigit() and begin_verse.isdigit() and end_verse.isdigit()):
            begin_verse = int(begin_verse)
            end_verse = int(end_verse)
        else:
            # return error message
            self.verse_label.setText("Wrong chapter and verse format!\n\n")
            return

        # if end verse is smaller than begin verse, switch them around
        if end_verse < begin_verse:
            temp = begin_verse
            begin_verse = end_verse
            end_verse = temp

        # convert the book name (either in English or Chinese, abbreviated or not)
        # to triditional chinese abbreviated setTextFormat
        # For example : Genesis -> 創, or Gen -> 創
        book = cvt.CVT(book)

        # convert book name to relative Chinese version
        if CN_Ver == "S":
            cc = OpenCC('t2s')
            book = cc.convert(book)
        else:
            cc = OpenCC('s2t')
            book = cc.convert(book)

        # If it is not key word search, run follows
        verses=""
        # determine which version to use, English or not
        ASV = read_text_EN(w_English)
        CHN = read_text_ZH(CN_Ver)

        Copy = True
        # find the verses from the beginning to the end
        for i in np.arange(begin_verse,end_verse+1):
            if i != 0:
                i = str(i) + " "
            # format the chinese verse to be searched
            verse2search_ZH = book + chapter + ":"+str(i)

            # Search the verse and add it to the string verses.
            searched_verse = str(search(CHN,ASV,verse2search_ZH))
            error_msg = "\n不好意思，没有相关经文，请确认输入的格式是否正确\n\nSorry ,  there is no such verse .\n"
            if len(searched_verse) == 0:
                Copy = False
                break
            else:
                verses = verses + searched_verse + ""

        # this copy the verses to your clipboard so you can just paste it out
        if Copy or len(verses)>len(error_msg):
            spam = copy_paste(verses[0:-2])
            # Update labels with searched verses and clear the search bar
            self.verse_label.setText(verses)
            self.user_input.setText("")
        else:
            # report error message
            self.verse_label.setText(error_msg)


    # funcion that check the status of the checkbox_English and write to defaults.txt
    def check_eng(self, checked):
        global w_English
        if checked:
            w_English = True
        else:
            w_English = False
        write_defaults()

    # Check the chinese version, slider value < 50 -> Simplified, else: Triditional
    # Also write to the default.txt
    def check_CN_Ver(self,value):
        global CN_Ver
        if value < 50:
            CN_Ver = "S"
        else:
            CN_Ver = "T"
        write_defaults()

    # Check which english version to used and wirte to defaults.txt
    def check_EN_Ver(self,version):
        global EN_Ver
        EN_Ver = str.split(version)[0]
        write_defaults()

    # display the book table
    def show_book_table(self):
        table = open("acronym.txt","r+")
        lines = ""
        for line in table:
            lines += line
        self.verse_label.setText(lines)

if __name__ == "__main__":
    read_defaults()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
