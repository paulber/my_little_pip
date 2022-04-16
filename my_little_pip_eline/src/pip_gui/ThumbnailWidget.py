"""
This module handles the thumbnail widget of my_little_pip.eline application

Classes: ThumbnailWidget(QListWidget)
Functions:
setup_widget(self)
"""
import sys

from PyQt6.QtWidgets import (QListWidget, QListWidgetItem)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap

from bin.pip_gui.PreprocessingGraphicItem import PreprocessingGraphicItem
import bin.pip_db.browse_db as browse_db


class ThumbnailWidget(QListWidget):

    def __init__(self):

        super().__init__()

        self.setup_widget()

        self.setDragEnabled(True)

        self.setViewMode(QListWidget.ViewMode.IconMode)

    def setup_widget(self):
        """
        Create and arrange element inside the widget, for now just browse function from a folder with picture
        TODO: start using dictionary for manipulated object to differentiate between element type
        TODO: initiate thumbnail with elements inside a pipeline database (public + private)
        TODO: make multiple list depending of the element type (loading/preprocessing/post-processing/...)
        """

        query = browse_db.initiate_thumbnail()

        while query.next():
            list_item = QListWidgetItem()
            list_item.setText(query.value(0))
            list_item.data = 'test'
            inter = PreprocessingGraphicItem(query.value(1), int(query.value(2)), int(query.value(3)))
            list_item.setIcon(QIcon(QPixmap(inter.to_pixmap())))
            self.setIconSize(QSize(50, 50))
            self.addItem(list_item)

        self.setAcceptDrops(False)
