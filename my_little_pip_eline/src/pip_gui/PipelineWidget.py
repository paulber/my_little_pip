"""
This module handles the pipeline widget of my_little_pip.eline application

Classes:
PipelineWidgetScene(QGraphicsScene)
PipelineWidgetView(QGraphicsView)
parameters: items_list
Functions:
setup_widget(self)
"""
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import (QModelIndex)
from PyQt6.QtGui import (QStandardItemModel)
from bin.pip_gui.PreprocessingGraphicItem import *
from bin.pip_gui.Connection import *


class PipelineWidgetScene(QGraphicsScene):
    startItem = newConnection = None

    def __init__(self):
        super().__init__()
        self.items_list = []

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if item := self.connection_point_at(event.scenePos()):
                self.startItem = item
                self.newConnection = Connection(item, event.scenePos())
                self.addItem(self.newConnection)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.newConnection:
            p2 = event.scenePos()
            self.newConnection.drawing_connection(p2)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.newConnection:
            item = self.connection_point_at(event.scenePos())
            if item and item.parentItem() != self.startItem.parentItem() and item.type != self.startItem.type:

                self.newConnection.drawing_connection(item)

                if self.startItem.add_line(self.newConnection):
                    item.add_line(self.newConnection)
                else:
                    self.removeItem(self.newConnection)
                    self.startItem.remove_line(self.newConnection)

            else:
                self.removeItem(self.newConnection)

            self.startItem = self.newConnection = None

        super().mouseReleaseEvent(event)

    def connection_point_at(self, pos):
        mask = QPainterPath()
        mask.setFillRule(Qt.FillRule.WindingFill)
        for item in self.items(pos):
            if mask.contains(pos):
                # ignore objects hidden by others
                return
            if isinstance(item, ConnectionPoint):
                return item
            if not isinstance(item, Connection):
                mask.addPath(item.shape().translated(item.scenePos()))


class PipelineWidgetView(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.scene = PipelineWidgetScene()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.setup_widget()

    def setup_widget(self):
        """
        Create and arrange widgets in window
        """
        self.setScene(self.scene)

    def dragEnterEvent(self, event):
        if event.source() in self.children():
            event.acceptProposedAction()

        if event.mimeData().hasFormat(
                "application/x-qabstractitemmodeldatalist"
        ):
            event.acceptProposedAction()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def dragMoveEvent(self, event):
        if event.source() in self.children():
            event.acceptProposedAction()
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        position = self.mapToScene(event.position().toPoint())
        dummy_model = QStandardItemModel()
        dummy_model.dropMimeData(event.mimeData(), event.dropAction(), 0, 0, QModelIndex())

        ix = dummy_model.index(0, 0)
        inter = ix.data()

        query = QSqlQuery()
        query.exec("SELECT name_id, symbol, number_input, number_output, GUI FROM functions WHERE name_id="
                   + "'" + inter + "'")

        if query.next():
            self._create_graphic_item(query, position)

    def _create_graphic_item(self, query, position):
        new_item = PreprocessingGraphicItem(query.value(1),
                                            int(query.value(2)),
                                            int(query.value(3)),
                                            option_gui_string=query.value(4))

        new_item.setScale(2)
        br = new_item.boundingRect()
        s = new_item.scale()
        w = int(br.width() * s) / 2
        h = int(br.height() * s) / 2
        new_item.setPos(position - QPointF(w, h))
        self.scene.addItem(new_item)
