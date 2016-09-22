from PyQt4 import QtGui, QtCore
from zonal_table_widget import Ui_ZonalTableWidget
from zonal_stat_dialog import ZonalStatisticsDialog


class Table(QtGui.QDialog, Ui_ZonalTableWidget):
    def __init__(self):
        super(Table, self).__init__()

        self.setupUi(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Table()
    main.show()
    sys.exit(app.exec_())