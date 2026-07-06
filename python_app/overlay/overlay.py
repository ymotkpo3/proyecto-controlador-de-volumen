from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QFont


class Overlay(QWidget):
    """
    Small always-on-top overlay used to display the selected app and volume.

    The widget is intentionally simple:
    - selection mode shows the app icon or a text fallback.
    - volume mode shows the app icon and a circular volume indicator.
    """

    def __init__(self):
        super().__init__()

        self.volume = 0.0
        self.icon = None
        self.label = ""
        self.mode = "selection"

        self.setFixedSize(56, 56)

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        background_rect = QRect(0, 0, self.width(), self.height())

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRoundedRect(background_rect, 12, 12)

        ring_rect = QRect(5, 5, 46, 46)

        # background_pen = QPen(Qt.darkGray)
        # background_pen.setWidth(3)
        # painter.setPen(background_pen)
        painter.drawEllipse(ring_rect)

        if self.mode == "volume":
            progress_pen = QPen(Qt.white)
            progress_pen.setWidth(3)
            painter.setPen(progress_pen)

            span = int(360 * self.volume * 16)

            painter.drawArc(
                ring_rect,
                90 * 16,
                -span
            )

        if self.icon:
            icon_size = 26

            x = (self.width() - icon_size) // 2
            y = (self.height() - icon_size) // 2

            painter.drawPixmap(
                x,
                y,
                icon_size,
                icon_size,
                self.icon
            )

        elif self.label:
            painter.setPen(Qt.white)

            font = QFont()
            font.setBold(True)
            font.setPointSize(13)
            painter.setFont(font)

            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                self.label
            )

    def showVolume(self, icon, volume: float, label: str = "") -> None:
        """
        Updates the overlay to display app volume.

        Args:
            icon:
                QPixmap shown at the center of the overlay.

            volume:
                Volume level in the range [0.0, 1.0].

            label:
                Text fallback used when no icon is available.
        """

        self.mode = "volume"
        self.icon = icon
        self.label = label
        self.volume = max(0.0, min(1.0, volume))

        self.update()
        self.show()
        self.raise_()

    def showSelection(self, icon, label: str = "") -> None:
        """
        Updates the overlay to display the selected app.

        Args:
            icon:
                QPixmap shown at the center of the overlay.

            label:
                Text fallback used when no icon is available.
        """

        self.mode = "selection"
        self.icon = icon
        self.label = label

        self.update()
        self.show()
        self.raise_()