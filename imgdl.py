# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 18:25:05 2015

@author: hara
"""

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from imgdl_UI1 import Ui_Form
from image_downloader import Img_DLClass
import time


class MyForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.list = []
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show()
        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.imgdownload)        
        
    def imgdownload(self):
        url = str(self.ui.lineEdit.text())
        directry = str(self.ui.lineEdit_2.text())
        th = Img_DLClass(url,directry)
        self.ui.lineEdit.clear()
        self.ui.label_2.setText(u"画像取得")
        th.start()
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = MyForm()
    sys.exit(app.exec_())
    #test