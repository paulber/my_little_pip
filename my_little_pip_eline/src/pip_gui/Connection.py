from collections import Counter
from typing import Union

from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsPathItem, QMenu
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainterPath, QPen, QContextMenuEvent


class ConnectionPoint(QGraphicsEllipseItem):

    def __init__(self, parent, type_point, x=0, y=0, width=10):

        super().__init__(0, 0, width, width, parent)

        self.type = type

        self.type = type_point
        self.parent = parent
        self.moveBy(x - width / 2, y - width / 2)
        self.line_draw = []

        # this flag **must** be set after creating self.lines!
        self.setFlags(self.GraphicsItemFlag.ItemSendsScenePositionChanges)

    def add_line(self, line_item):
        for existing in self.line_draw:
            if Counter(existing.connection_points()) == Counter(line_item.connection_points()):
                return False
        self.line_draw.append(line_item)
        return True

    def remove_line(self, line_item):
        for existing in self.line_draw:
            if Counter(existing.connection_points()) == Counter(line_item.connection_points()):
                start_connection_points, end_connection_points = line_item.connection_points()
                start_connection_points.line_draw.remove(existing)
                end_connection_points.line_draw.remove(existing)
                self.scene().removeItem(line_item)
                self.scene().removeItem(existing)
                return True
        return False

    def itemChange(self, change, value):
        for line in self.line_draw:
            line.update_line(self)
        return super().itemChange(change, value)

    def __str__(self):
        return "From str method of ConnectionPoint: type is %s, " \
               "parent is %s" % (self.type, self.parent.__str__())


class Connection(QGraphicsPathItem):

    def __init__(self, start_connection_point: ConnectionPoint, end_point: Union[ConnectionPoint, QPointF]):
        super().__init__()

        self.offset_end = None
        self.offset_start = None
        self.penBU = self.pen()
        self.start = start_connection_point
        self.end = end_point
        self.offset_connection = 6

        self.points_list = self.generate_point_list(self.start, self.end, self.offset_connection)

        self.path = self.draw_path(self.points_list)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu()

        # Add menu options
        exit_option = menu.addAction('Delete')

        exit_option.triggered.connect(self.delete_connection)

        menu.exec(event.screenPos())

    def delete_connection(self):
        self.scene().removeItem(self)

    def drawing_connection(self, end_connection_point: Union[ConnectionPoint, QPointF]):

        if type(end_connection_point) is QPointF:
            self.points_list[1] = end_connection_point
        else:
            self.points_list = self.generate_point_list(self.start, end_connection_point, self.offset_connection)
            self.end = end_connection_point

        self.path = self.draw_path(self.points_list)

    def update_line(self, source):

        if source == self.start:
            self.points_list = self.generate_point_list(source, self.end, self.offset_connection)
        else:
            self.points_list = self.generate_point_list(self.start, source, self.offset_connection)

        self.path = self.draw_path(self.points_list)

    def generate_point_list(self, start, end, offset):

        if start.type == 'input':
            self.offset_start = QPointF(start.boundingRect().width() - self.pen().width() / 2, 0)
        else:
            self.offset_start = QPointF(start.boundingRect().width() - self.pen().width() / 2,
                                        2 * start.boundingRect().height() - self.pen().width() / 2)

        p0 = start.scenePos() + self.offset_start
        p1 = p0 + QPointF(0, offset)

        if type(end) is QPointF:
            p2 = end

            return [p0, p2]
        else:
            if end.type == 'output':
                self.offset_end = QPointF(end.boundingRect().width() - self.pen().width() / 2,
                                          2 * end.boundingRect().height() - self.pen().width() / 2)
            else:
                self.offset_end = QPointF(end.boundingRect().width() - self.pen().width() / 2, 0)

            p2 = end.scenePos() + self.offset_end
            pc = (p1 + p2) / 2
            p3 = p2 + QPointF(0, offset)

            return [p0, p1, pc, p2, p3]

    def draw_path(self, path_list):
        path = QPainterPath()

        path.moveTo(path_list[0])

        if len(path_list) == 2:
            path.lineTo(path_list[1])
        else:
            self._line.setP2(source.scenePos() + self.offset)
        self.setLine(self._line)