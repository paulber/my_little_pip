
from PyQt6.QtWidgets import QGraphicsItem, QMenu
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QRadialGradient, QContextMenuEvent, QPixmap
from PyQt6.QtCore import Qt, QRectF, QPoint
from src.pip_gui.Connection import ConnectionPoint
import src.pip_db.browse_db as browse_db


def gui_load_data():
    print("test complete")


def gui_load_data():
    print("test complete")


class PipelineGraphicItem(QGraphicsItem):

    def __init__(self, text="?", input_number=0, output=0,
                 basis_color=QColor(170, 170, 170), option_gui_string=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        super().setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        self.connexions_list = []
        self.text = text
        self.basis_color = basis_color
        self.option_gui = option_gui_string
        self.options = None

        self.pen = QPen(self.basis_color, 0)

        gradient = QRadialGradient(0, 0, 20)
        gradient.setColorAt(0, self.basis_color.lighter(125))
        gradient.setColorAt(0.82, self.basis_color)

        self.brush = QBrush(gradient)

        self.controlBrush = QBrush(QColor(214, 13, 36))
        self.rect = QRectF(0, 0, 50, 30)

        self.input = input_number
        self.output = output

        for i in range(self.input):
            connexions = ConnectionPoint(self, 'input', (i+1) * self.rect.width()/(self.input+1), 0, 5)

            connexions.setPen(QColor(0, 255, 0))
            connexions.setBrush(QColor(0, 255, 0))

            self.connexions_list.append(connexions)

        for i in range(self.output):
            connexions = ConnectionPoint(self, 'output', (i+1) * self.rect.width()/(self.output+1),
                                         self.rect.height(), 5)

            connexions.setPen(QColor(255, 0, 0))
            connexions.setBrush(QColor(255, 0, 0))

            self.connexions_list.append(connexions)

    def boundingRect(self):
        adjust = self.pen.width() / 2
        return self.rect.adjusted(-adjust, -adjust, adjust, adjust)

    def paint(self, painter, option, widget=None):
        painter.save()

        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect, 10, 10)

        painter = self.get_painter(painter)

        painter.restore()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu()

        # Add menu options
        set_option = menu.addAction('Set options')
        exit_option = menu.addAction('Delete')

        exit_option.triggered.connect(self.delete_item)
        set_option.triggered.connect(self.call_item_gui)

        menu.exec(event.screenPos())

    def delete_item(self):
        """
        TODO
        """
        for i in self.connexions_list:
            while i.line_draw:
                i.remove_line(i.line_draw[0])

        self.scene().removeItem(self)

    def call_item_gui(self):
        """
        Call specific GUI for the item
        """
        query = browse_db.find_import_list_for_gui(self.option_gui)

        while query.next():
            exec("from " + query.value(0) + " import " + self.option_gui)
        self.options = eval(f"{self.option_gui}()")

    def __str__(self):
        return f"From str method of PipelineGraphicItem: text is {self.text}, "

    def to_pixmap(self):
        r = self.boundingRect()
        pixmap = QPixmap(int(r.width()), int(r.height()))
        pixmap.fill(self.basis_color)
        painter = QPainter(pixmap)
        painter.drawRect(r)

        painter = self.get_painter(painter)

        painter.end()
        return pixmap

    def get_painter(self, painter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setFont(QFont("Helvetica", 10))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        text_size = painter.fontMetrics().size(Qt.TextFlag.TextSingleLine, self.text)

        new_x = self.rect.center().x() - text_size.width() / 2
        new_y = self.rect.center().y() + text_size.height() / 2

        painter.drawText(QPoint(int(new_x), int(new_y)), self.text)

        return painter
