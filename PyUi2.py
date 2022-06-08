import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem
from PyQt5 import uic
import Calculator
import OneRoadMapCreater

def list2string(tlist):
    tstring = ""
    for each in tlist:
        tstring += each
        tstring += ', '
    ttstring = tstring[:-2]
    return ttstring

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./QtUi/main.ui")
        self.ui.show()

        self.ui.StartUsingButton.clicked.connect(self.StartUsing)
        self.ui.InfoButton.clicked.connect(self.ShowInfo)
    def StartUsing(self):
        self.workdlg = WorkingWind()
        self.workdlg.domodle()
    def ShowInfo(self):
        self.infodlg = InfoWind()
        self.infodlg.domodle()


class InfoWind(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./QtUi/InfoWind.ui")
    def domodle(self):
        self.ui.show()
        self.ui.exec_()


class WorkingWind(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./QtUi/WorkingWind.ui")
        self.ui.DistanceFindButton.clicked.connect(self.distancefind)
        self.ui.TransferFindButton.clicked.connect(self.transferfind)
        self.ui.AllSiteButton.clicked.connect(self.allsite)

        self.init_combobox()

    def domodle(self):
        self.ui.show()
        self.ui.exec_()

    def distancefind(self):
        print("最短距离")
        #self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        start = self.ui.StartcomboBox.currentText()
        end = self.ui.EndcomboBox.currentText()
        Cost, Routes, BusIdMaps = Calculator.MinDistanceDijkstra(start, end)
        if Cost == float("inf"):
            self.ui.tableWidget.insertRow(0)
            item = QTableWidgetItem()
            item.setText("无路线")
            self.ui.tableWidget.setItem(0, 0, item)
        elif Cost == 0:
            self.ui.tableWidget.insertRow(0)
            item = QTableWidgetItem()
            item.setText(start)
            item2 = QTableWidgetItem()
            item2.setText("起点终点相同")
            self.ui.tableWidget.setItem(0, 1, item)
            self.ui.tableWidget.setItem(0, 0, item2)
        else:
            RouteArr2, BusIdArr2 = Calculator.getfinall(start, end, Routes, BusIdMaps, 1)
            row = 0
            couter = 1
            for routearr2 in RouteArr2:
                self.ui.tableWidget.insertRow(row)  #插入一行

                coutertext = "第" + str(couter) + "条路线"
                itemcoutertext = QTableWidgetItem()
                itemcoutertext.setText(coutertext)
                self.ui.tableWidget.setItem(row, 0, itemcoutertext)
                couter += 1
                row += 1

                for routearr in routearr2:
                    self.ui.tableWidget.insertRow(row)
                    itemroute = QTableWidgetItem()
                    itemroute.setText(routearr)
                    self.ui.tableWidget.setItem(row, 1, itemroute)
                    row += 1

            row = 0
            prebusarr = ""  # 前一个站点的公交路线，如果前一个和现在的不相等说明换乘
            for busidarr2 in BusIdArr2:
                row += 1
                for busidarr in busidarr2:
                    tstr = list2string(busidarr)
                    #tstr = busidarr
                    if prebusarr != tstr:
                        itemC = QTableWidgetItem()
                        itemC.setText("换乘站")
                        self.ui.tableWidget.setItem(row, 0, itemC)  #换乘站
                        prebusarr = tstr
                    itembus = QTableWidgetItem()
                    itembus.setText(tstr)
                    self.ui.tableWidget.setItem(row, 2, itembus)
                    row += 1





    def transferfind(self):
        print("最少换乘")
        # self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        start = self.ui.StartcomboBox.currentText()
        end = self.ui.EndcomboBox.currentText()
        Cost, Routes, BusIdMaps = Calculator.MinDistanceDijkstra(start, end)
        if Cost == float("inf"):
            self.ui.tableWidget.insertRow(0)
            item = QTableWidgetItem()
            item.setText("无路线")
            self.ui.tableWidget.setItem(0, 0, item)
        elif Cost == 0:
            self.ui.tableWidget.insertRow(0)
            item = QTableWidgetItem()
            item.setText(start)
            item2 = QTableWidgetItem()
            item2.setText("起点终点相同")
            self.ui.tableWidget.setItem(0, 1, item)
            self.ui.tableWidget.setItem(0, 0, item2)
        else:
            RouteArr2, BusIdArr2 = Calculator.getfinall(start, end, Routes, BusIdMaps, 0)
            row = 0
            couter = 1
            for routearr2 in RouteArr2:
                self.ui.tableWidget.insertRow(row)  # 插入一行

                coutertext = "第" + str(couter) + "条路线"
                itemcoutertext = QTableWidgetItem()
                itemcoutertext.setText(coutertext)
                self.ui.tableWidget.setItem(row, 0, itemcoutertext)
                couter += 1
                row += 1

                for routearr in routearr2:
                    self.ui.tableWidget.insertRow(row)
                    itemroute = QTableWidgetItem()
                    itemroute.setText(routearr)
                    self.ui.tableWidget.setItem(row, 1, itemroute)
                    row += 1

            row = 0
            prebusarr = ""  # 前一个站点的公交路线，如果前一个和现在的不相等说明换乘
            for busidarr2 in BusIdArr2:
                row += 1
                for busidarr in busidarr2:
                    #tstr = list2string(busidarr)
                    tstr = busidarr
                    if prebusarr != tstr:
                        itemC = QTableWidgetItem()
                        itemC.setText("换乘站")
                        self.ui.tableWidget.setItem(row, 0, itemC)  # 换乘站
                        prebusarr = tstr
                    itembus = QTableWidgetItem()
                    itembus.setText(tstr)
                    self.ui.tableWidget.setItem(row, 2, itembus)
                    row += 1
                row += 1    #因为最后一站没有相应的公交线路进行显示，所以row再次自增1来对齐


    def allsite(self):
        print("所有站点")
        #self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        row = 0

        for site in OneRoadMapCreater.SiteDic:
            self.ui.tableWidget.insertRow(row)
            item = QTableWidgetItem()
            item.setText(site)
            self.ui.tableWidget.setItem(row, 1, item)

            index = OneRoadMapCreater.SiteDic[site]
            item2 = QTableWidgetItem()
            item2.setText(list2string(OneRoadMapCreater.BusIdArr[index][index]))
            self.ui.tableWidget.setItem(row, 2, item2)

            row += 1

    def init_combobox(self):
        self.ui.StartcomboBox.clear()
        self.ui.EndcomboBox.clear()
        for site in OneRoadMapCreater.SiteDic:
            self.ui.StartcomboBox.addItem(site)
            self.ui.EndcomboBox.addItem(site)


if __name__ == "__main__":
    Calculator.init_data()
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
