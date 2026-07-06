from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QAction, QIcon, QPainter, QPen, QColor, QPixmap, QGuiApplication
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from python_app import startup


_tray = None
_menu = None
_startup_action = None
_exit_action = None


def init() -> None:
    """
    Initializes the system tray icon and context menu.

    Must be called after QApplication has been created.
    """

    global _tray
    global _menu
    global _startup_action
    global _exit_action

    if _tray is not None:
        return

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available.")
        return

    _tray = QSystemTrayIcon(
        _createTrayIcon(),
        QApplication.instance()
    )

    _tray.setToolTip("Megaknob")

    _menu = QMenu()

    _startup_action = QAction("Iniciar con Windows", _menu)
    _startup_action.setCheckable(True)
    _startup_action.setChecked(startup.isStartupEnabled())
    _startup_action.toggled.connect(_toggleStartup)

    _exit_action = QAction("Salir", _menu)
    _exit_action.triggered.connect(QApplication.quit)

    _menu.addAction(_startup_action)
    _menu.addSeparator()
    _menu.addAction(_exit_action)

    _tray.setContextMenu(_menu)
    _tray.show()

    print("System tray initialized")


def _toggleStartup(enabled: bool) -> None:
    """
    Enables or disables automatic startup from the tray menu.

    Args:
        enabled:
            Desired automatic startup state.
    """

    try:
        if enabled:
            startup.enableStartup()
        else:
            startup.disableStartup()

    except Exception as error:
        print(f"Could not update startup setting: {error}")

        if _startup_action is not None:
            _startup_action.blockSignals(True)
            _startup_action.setChecked(startup.isStartupEnabled())
            _startup_action.blockSignals(False)


def _createTrayIcon() -> QIcon:

    size = 64

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)

    painter.setRenderHint(
        QPainter.RenderHint.Antialiasing,
        True
    )

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(20, 20, 20))

    painter.drawRoundedRect(
        QRect(4, 4, 56, 56),
        14,
        14
    )

    accent_color = QGuiApplication.palette().highlight().color()

    ring_pen = QPen(accent_color)
    ring_pen.setWidth(5)
    ring_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(ring_pen)

    painter.drawArc(
        QRect(15, 15, 34, 34),
        110 * 16,
        -290 * 16
    )

    center_pen = QPen(Qt.GlobalColor.white)
    center_pen.setWidth(4)

    painter.setPen(center_pen)
    painter.setBrush(QColor(235, 235, 235))

    painter.drawEllipse(
        QRect(25, 25, 14, 14)
    )

    painter.end()

    return QIcon(pixmap)