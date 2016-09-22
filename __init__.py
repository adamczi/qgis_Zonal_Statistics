# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZonalStatistics
                                 A QGIS plugin
 This plugin shows statistics for regions
                             -------------------
        begin                : 2016-09-13
        copyright            : (C) 2016 by Adam Borczyk
        email                : ad.borczyk@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ZonalStatistics class from file ZonalStatistics.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .zonal_stat import ZonalStatistics
    return ZonalStatistics(iface)
