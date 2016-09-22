from PyQt4 import QtGui, QtCore
from zonal_new_column_dialog import Ui_Dialog
from zonal_stat_dialog import ZonalStatisticsDialog


class NewColumn(QtGui.QDialog, Ui_Dialog):
    def __init__(self):
        super(NewColumn, self).__init__()

        self.setupUi(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = NewColumn()
    main.show()
    sys.exit(app.exec_())