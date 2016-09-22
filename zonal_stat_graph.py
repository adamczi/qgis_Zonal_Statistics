from PyQt4 import QtGui, QtCore
from zonal_plot_widget import Ui_Dialog
from zonal_stat_dialog import ZonalStatisticsDialog


class Graph(QtGui.QDialog, Ui_Dialog):
    def __init__(self):
        super(Graph, self).__init__()

        self.setupUi(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Graph()
    main.show()
    sys.exit(app.exec_())