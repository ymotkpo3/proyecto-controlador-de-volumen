from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QGuiApplication


class Overlay(QWidget):
    """
    Small always-on-top overlay used to display app selection and volume.

    Selection mode shows only the app icon or a text fallback.
    Volume mode shows the app icon and a circular volume indicator.
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

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True
        )

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            True
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 220))

        painter.drawRoundedRect(
            QRect(0, 0, self.width(), self.height()),
            13,
            13
        )

        if self.mode == "volume":
            self._drawVolumeRing(painter)

        self._drawIconOrLabel(painter)

        painter.end()

    def _drawVolumeRing(self, painter: QPainter) -> None:
        """
        Draws the volume progress ring.

        No background ring is drawn. Only the current volume arc is visible.
        """

        if self.volume <= 0.0:
            return

        ring_rect = QRect(
            10,
            10,
            36,
            36
        )

        accent_color = QGuiApplication.palette().highlight().color()

        progress_pen = QPen(accent_color)
        progress_pen.setWidth(3)

        if self.volume < 0.999:
            progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        else:
            progress_pen.setCapStyle(Qt.PenCapStyle.FlatCap)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(progress_pen)

        if self.volume >= 0.999:
            painter.drawEllipse(ring_rect)
            return

        span = int(
            360 *
            self.volume *
            16
        )

        painter.drawArc(
            ring_rect,
            90 * 16,
            -span
        )

    def _drawIconOrLabel(self, painter: QPainter) -> None:
        """
        Draws the app icon or a text fallback.
        """

        if self.icon:
            icon_size = 22

            x = (self.width() - icon_size) // 2
            y = (self.height() - icon_size) // 2

            painter.drawPixmap(
                x,
                y,
                icon_size,
                icon_size,
                self.icon
            )

            return

        if self.label:
            painter.setPen(Qt.GlobalColor.white)

            font = QFont()
            font.setBold(True)
            font.setPointSize(12)

            painter.setFont(font)

            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                self.label
            )

    def showVolume(self, icon, volume: float, label: str = "") -> None:
        """
        Shows the overlay in volume mode.

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
        Shows the overlay in selection mode.

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