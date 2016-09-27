# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZonalStatistics
                                 A QGIS plugin
 This plugin shows statistics for regions
                              -------------------
        begin                : 2016-09-13
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Adam Borczyk
        email                : ad.borczyk@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon, QTableWidgetItem, QToolBar
from qgis.core import QgsMapLayerRegistry, QgsField, QgsMapLayer, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from zonal_stat_dialog import ZonalStatisticsDialog
import os.path
from zonal_custom_table import QCustomTableWidgetItem
from zonal_stat_dialog import ZonalStatisticsDialog
import zonal_stat_graph, zonal_stat_table, zonal_stat_new_column
import pyqtgraph

class ZonalStatistics:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ZonalStatistics_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ZonalStatisticsDialog(self.iface.mainWindow())
        self.graph = zonal_stat_graph.Graph()
        self.table = zonal_stat_table.Table()
        self.newCol = zonal_stat_new_column.NewColumn()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Location Intelligence')
        
        ## Add to LI tooblar or create if doesn't exist
        toolbarName = u'Location Intelligence'
        self.toolbar = self.iface.mainWindow().findChild(QToolBar,toolbarName)
        print self.toolbar
        if self.toolbar is None:
            self.toolbar = self.iface.addToolBar(toolbarName)
            self.toolbar.setObjectName(toolbarName)
            

        ## Functions call on init
        self.statistics()

        self.availableLayers()

        self.dlg.comboBox_3.currentIndexChanged.connect(self.fieldsToAnalyse)

        self.dlg.pushButton.clicked.connect(self.spatialQuery_group)

        self.table.pushButton_5.clicked.connect(self.showGraph)

        self.dlg.pushButton_2.clicked.connect(self.addToAttrTable_group)

        self.table.pushButton_6.clicked.connect(self.spatialQuery)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ZonalStatistics', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ZonalStatistics/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Open Zonal Statistics'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Zonal Statistics'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        if len(self.toolbar.actions())==0:
            del self.toolbar

    def availableLayers(self):
        """ Adds layers to comboboxes """
        self.dlg.comboBox.clear()
        self.dlg.comboBox_3.clear()
        for i in self.iface.legendInterface().layers():
            if  i.type() == QgsMapLayer.VectorLayer and i.isValid():
                if  i.wkbType() % 3 == 0 and i.isValid(): ## Region layers
                    self.dlg.comboBox.addItem(i.name())        
                if  i.wkbType() % 3 == 1 and i.isValid(): ## Point layers
                    self.dlg.comboBox_3.addItem(i.name())
           

        ## Run function that fills the combobox below for the first time when plugin starts
        self.fieldsToAnalyse()

    def fieldsToAnalyse(self):
        """ Add fields of numeric type into combobox """
        try:
            chosenLayer = self.dlg.comboBox_3.currentText()
        
            layer = QgsMapLayerRegistry.instance().mapLayersByName(chosenLayer)[0]

            self.dlg.comboBox_2.clear()
            for field in layer.pendingFields():
                if field.typeName() in ("Real", "real", "Integer", "integer","Integer64", "integer64", "Double", "double") and field.name() not in ("id", "ID", "Id", "iD"):
                    self.dlg.comboBox_2.addItem(field.name())
        except IndexError:
            self.dlg.comboBox_2.clear()


    def statistics(self):
        """ Available statistics """
        stats = [u'Suma', u'Średnia', u'Liczba obiektów']
        for st in stats:
            self.dlg.comboBox_4.addItem(st)

    def spatialQuery(self):
        """ Creates lists of features within each polygon """
        try:
            PolyName = self.dlg.comboBox.currentText()
            layerList_Poly = QgsMapLayerRegistry.instance().mapLayersByName(PolyName)
            self.polygons = [feature for feature in layerList_Poly[0].getFeatures()]
            polyCRS = int(layerList_Poly[0].crs().authid()[5:])

            PointName = self.dlg.comboBox_3.currentText()
            layerList_Point = QgsMapLayerRegistry.instance().mapLayersByName(PointName)
            self.points = [feature for feature in layerList_Point[0].getFeatures()]
            pointCRS = int(layerList_Point[0].crs().authid()[5:])          

            self.groups = []
            self.values = []    
            count = -1
            maximum = len(self.polygons)
            currentField = self.dlg.comboBox_2.currentText()

            for fPoly in self.polygons:        
                self.values.append([])
                poly_geom = fPoly.geometry()

                ## Progress bar part
                status = count+2
                progress = int(round(status/float(maximum)*100))
                self.increaseProgressBar(progress)                

                ## Change CRS if different
                if polyCRS != pointCRS:
                    crsSrc = QgsCoordinateReferenceSystem(polyCRS)
                    crsDest = QgsCoordinateReferenceSystem(pointCRS)
                    xform = QgsCoordinateTransform(crsSrc, crsDest)
                    poly_geom.transform(xform)   

                try:
                    self.groups.append(fPoly[1])
                except KeyError:
                    self.iface.messageBar().pushMessage("Error", u"Druga kolumna warstwy regionów musi zawierać ich nazwy", level=QgsMessageBar.WARNING, duration=4)
                    return
                count += 1

                for fPoint in self.points:
                    pt_geom = fPoint.geometry()

                    if poly_geom.contains(pt_geom):
                        self.values[count].append(fPoint[currentField])

                ## Change back if it was different
                if polyCRS != pointCRS:
                    xform = QgsCoordinateTransform(crsDest, crsSrc)
                    poly_geom.transform(xform)


            self.x = list(enumerate(self.groups))

            self.prepareGraph()
            self.prepareTable()

        except IndexError:
            # self.iface.messageBar().pushMessage("Error", u"Brak dostępnych warstw wektorowych lub warstwa usunięta", level=QgsMessageBar.CRITICAL, duration=4)
            pass

    def prepareGraph(self):
        """ Prepare data to use """

        self.y = []
        # try:
        #     self.x = list(enumerate(self.groups))
        #     self.y = []
        #     selectedColumns = []
        #     ## If no or only 'Region' column loaded
        #     if self.dlg.tableWidget.columnCount() in (0,1):
        #         return
        #     else: 
        #         ## Check which columns are selected and get the first one if many
        #         for index in self.dlg.tableWidget.selectedIndexes():
        #             if index.column() != 0:
        #                 selectedColumns.append(index.column())

        #     ## In case none or Region column checked and the button was pressed
        #     try:
        #         columnToGraph = min(selectedColumns)-1
        #     except ValueError, NameError:
        #         columnToGraph = 0
        self.graphTitle = self.dlg.comboBox_3.currentText()+': '+self.dlg.comboBox_2.currentText()

        ## Select data
        for valGroup in range(len(self.values)):
            try:
                if self.dlg.comboBox_4.currentIndex() == 0:
                    self.y.append(round(sum(self.values[valGroup]),2))
                elif self.dlg.comboBox_4.currentIndex() == 1:
                    try:
                        self.y.append(round(sum(self.values[valGroup])/len(self.values[valGroup]),2))
                    except ZeroDivisionError:
                        self.y.append(0)
                else:
                    self.y.append(len(self.values[valGroup]))
            except TypeError:
                self.iface.messageBar().pushMessage("Error", u"Pusta kolumna z danymi ("+self.dlg.comboBox_2.currentText()+")", level=QgsMessageBar.WARNING, duration=4)

        self.buildGraph()

    def buildGraph(self):
        """ Add data to the graph """
        dataColor = (102,178,255)
        dataBorderColor = (180,220,255)
        barGraph = self.graph.plotWidget
        barGraph.clear()
        barGraph.addItem(pyqtgraph.BarGraphItem(x=range(len(self.x)), height=self.y, width=0.5, brush=dataColor, pen=dataBorderColor))
        barGraph.addItem(pyqtgraph.GridItem())
        barGraph.getAxis('bottom').setTicks([self.x])
        barGraph.setTitle(title=self.graphTitle)

    def showGraph(self):
        """ Just show the graph on click """
        self.graph.show()

    def prepareTable(self):
        """ Create table to view the data """
        qTable = self.table.tableWidget

        labels = ['Region', unicode(self.dlg.comboBox_2.currentText())]

        qTable.setSortingEnabled(False)
        qTable.setRowCount(len(self.groups))
        qTable.setColumnCount(len(labels))

        # Insert data
        try:
            for row in range(len(self.groups)):
                ## Add group name field
                group = QTableWidgetItem(unicode(self.groups[row]))
                qTable.setItem(row,0,group) 

                ## Calculate sum or average
                if self.dlg.comboBox_4.currentIndex() == 0:
                    item = QCustomTableWidgetItem(str(round(self.y[row],2)))
                elif self.dlg.comboBox_4.currentIndex() == 1:
                    try:
                        item = QCustomTableWidgetItem(str(round(self.y[row]/len(self.values[row]),2)))
                    except ZeroDivisionError:
                        item = QCustomTableWidgetItem(str(0))
                else:
                    item = QTableWidgetItem(str(len(self.values[row])))
                                                
                ## Set item
                qTable.setItem(row,1,item)
                    
        except TypeError:
            self.iface.messageBar().pushMessage("Error", u"Wybrane pole zawiera puste komórki ("+self.dlg.comboBox_2.currentText()+")", level=QgsMessageBar.WARNING, duration=4)

        qTable.setSortingEnabled(True)
        qTable.setHorizontalHeaderLabels(labels)
        qTable.resizeColumnsToContents()

    def showTable(self):
        """ Just show the table on click"""
        self.table.show()

    def rowSelection(self):
        """ Highlights selected groups on map """ 
        PointName = self.dlg.comboBox_3.currentText()
        layerList_Point = QgsMapLayerRegistry.instance().mapLayersByName(PointName)
        selectedFeatures = []

        layerList_Point[0].setSelectedFeatures([])

        qTable = self.table.tableWidget
        indexes = qTable.selectionModel().selectedRows()
        
        ## Get selected group name
        for index in sorted(indexes):
            selectedGroup = qTable.item(index.row(),0).text()

        ## Select features
        for fPoly in self.polygons:
            if fPoly[1] == selectedGroup:
                poly_geom = fPoly.geometry()

                for fPoint in self.points:
                    point_geom = fPoint.geometry()

                    if poly_geom.contains(point_geom):
                        selectedFeatures.append(fPoint)

        ## Set selection to chosen IDs
        ids = [i.id() for i in selectedFeatures]
        layerList_Point[0].setSelectedFeatures(ids)


    def showNewCol(self):
        """ Show a dialog box to input new column name """
        self.newCol.show()
        result = self.newCol.exec_()
        if result:
            newName = self.newCol.lineEdit.text()
            if newName == '':
                self.iface.messageBar().pushMessage("Error", u"Wpisz nazwę nowej kolumny (do 10 znaków)", level=QgsMessageBar.WARNING, duration=4)
                return
            else: 
                self.addToAttrTable(newName)

    def addToAttrTable(self, newName):
        """ Add statistics to the attribute table of regions layer """
        try:
            PolyName = self.dlg.comboBox.currentText()

            layerPoly = QgsMapLayerRegistry.instance().mapLayersByName(PolyName)[0]      
            features = layerPoly.getFeatures()         
            layerPoly.dataProvider().addAttributes([QgsField(newName, QVariant.Double, "double", 10, 2)])
            layerPoly.updateFields()             
            
            columnid = layerPoly.fieldNameIndex(newName)
            count = 0

            ## Progress bar part
            maximum = 0
            for feature in features:
                maximum += 1

            layerPoly.startEditing()

            ## Get features again as they were 'used' to get 'maximum'
            features = layerPoly.getFeatures() 

            for feature in features:
                fid = feature.id()
                ## Prepare data
                if self.dlg.comboBox_4.currentIndex() == 0:
                    item = round(self.y[count],2)
                elif self.dlg.comboBox_4.currentIndex() == 1:
                    try:
                        item = round((self.y[count])/len(self.values[count]),2)
                    except ZeroDivisionError:
                        item = 0
                else:
                    item = len(self.values[count])

                ## Progress bar part
                progress = int(round((count+1)/float(maximum)*100))
                self.increaseProgressBar(progress)  

                ## Update attribute table            
                layerPoly.changeAttributeValue(fid, columnid, item, True)
                count += 1

            layerPoly.commitChanges()

        except:
            try:
                ## Delete unsuccessful column
                layerPoly.rollBack()
                layerPoly.dataProvider().deleteAttributes([layerPoly.fieldNameIndex(newName)])
                layerPoly.updateFields()
                self.iface.messageBar().pushMessage("Error", u"Najpierw wczytaj dane", level=QgsMessageBar.CRITICAL, duration=4)
            except UnboundLocalError:
                self.iface.messageBar().pushMessage("Error", u"Błąd w dostępie do wybranej warstwy", level=QgsMessageBar.CRITICAL, duration=4)

    def addToAttrTable_group(self):
        """ Run spatial query and prepare data to input to attr table """
        self.spatialQuery()
        if self.dlg.comboBox_2.count() > 0:
            self.showNewCol()

    def spatialQuery_group(self):
        """ Run spatial query and view table """
        self.spatialQuery()
        if self.dlg.comboBox_2.count() > 0:
            self.showTable()

    def increaseProgressBar(self, value):
        self.dlg.progressBar.setValue(value)  

    def run(self):
        """Run method that performs all the real work"""

        ## Reset progress bar
        self.dlg.progressBar.setValue(0)

        ## Update available layers
        self.availableLayers()

        ## Update available fields
        # self.fieldsToAnalyse()    
        
        ## Listen to features selection on row click
        self.table.tableWidget.verticalHeader().sectionClicked.connect(self.rowSelection)
        
        # show the dialog
        self.dlg.show()
