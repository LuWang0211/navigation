from PyQt5.QtCore import Qt, QSize, QPointF, QRect
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QStyledItemDelegate, QStyle, QStyleOptionButton

Table_Widget_Activation_RoleId = 1000
Table_Widget_CheckState_RoleId = 1001

class CustomTableItemPainter(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CustomTableItemPainter, self).__init__(parent)

    def paint(self, painter, option, index):
        should_be_activated = index.data(Table_Widget_Activation_RoleId)
        is_checked = index.data(Table_Widget_CheckState_RoleId)

        if should_be_activated == True and not is_checked:
            self.paint_activated_item(painter, option, index)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def paint_activated_item(self, painter, option, index):
        original_pen = painter.pen()

        pen_width = 10
        hw = pen_width / 2
        color = QColor('#7fffd4')
        painter.setPen(QPen(QBrush(color), pen_width))
        rect = option.rect
        x, y, w, h = (rect.x(), rect.y(), rect.width(), rect.height())
        column = index.column()

        if column == 0:
            painter.drawPolyline(
                QPointF(x + w - hw, y + h - hw), 
                QPointF(x, y + h - hw),
                QPointF(x, y + hw), 
                QPointF(x + w - hw, y + hw)
            )
        elif column == 1 or column == 2:
            painter.drawLines(
                QPointF(x + hw, y + hw), 
                QPointF(x + w - hw, y + hw),
                QPointF(x + hw, y + h - hw), 
                QPointF(x + w - hw, y + h - hw)
            ) 
        elif column == 3:
            painter.drawPolyline(
                QPointF(x + hw, y + hw), 
                QPointF(x + w, y + hw),
                QPointF(x + w, y + h - hw),
                QPointF(x + hw, y + h - hw)
            )

            opts = QStyleOptionButton()
            spacing = 1
            shrinked_rect = QRect(x + spacing, y + spacing, w - spacing - spacing, h - spacing - spacing)
            opts.rect = shrinked_rect
            opts.state = QStyle.State_Active | QStyle.State_Enabled

            QApplication.style().drawControl(QStyle.CE_PushButton, opts, painter)

            overlayColor = QColor(color.red(), color.green(), color.blue(), 125)
            painter.fillRect(shrinked_rect, overlayColor)

            painter.setPen(QPen(QBrush(Qt.black), 3))
            painter.drawText(shrinked_rect, Qt.AlignCenter, 'Check!')
        
        painter.setPen(original_pen)

        if column in (0, 1, 2):
            QStyledItemDelegate.paint(self, painter, option, index)