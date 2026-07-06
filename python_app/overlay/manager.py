from PySide6.QtCore import QTimer
from PySide6.QtGui import QGuiApplication

from python_app.overlay.overlay import Overlay
from python_app.overlay.icons import getAppPixmap, getMasterPixmap
from python_app import audio


_overlay: Overlay | None = None
_hide_timer: QTimer | None = None
_icon_cache = {}


def init() -> None:
    """
    Initializes the overlay system.

    Must be called after QApplication has been created.
    """

    global _overlay
    global _hide_timer

    if _overlay is not None:
        return

    _overlay = Overlay()
    _positionOverlay()

    _hide_timer = QTimer()
    _hide_timer.setSingleShot(True)
    _hide_timer.timeout.connect(_overlay.hide)


def showSelection(app) -> None:
    """
    Shows the overlay in app-selection mode.

    Args:
        app:
            Selected AudioApp.
    """

    if _overlay is None or _hide_timer is None:
        return

    _positionOverlay()

    _overlay.showSelection(
        _getIcon(app),
        _getLabel(app)
    )

    _hide_timer.start(900)


def showVolume(app) -> None:
    """
    Shows the overlay in volume mode.

    Args:
        app:
            Selected AudioApp.
    """

    if _overlay is None or _hide_timer is None:
        return

    _positionOverlay()

    _overlay.showVolume(
        _getIcon(app),
        audio.getVolume(app),
        _getLabel(app)
    )

    _hide_timer.start(900)


def _positionOverlay() -> None:
    """
    Places the overlay near the bottom-right corner of the primary screen.
    """

    if _overlay is None:
        return

    screen = QGuiApplication.primaryScreen()

    if screen is None:
        return

    geometry = screen.availableGeometry()
    margin = 24

    x = geometry.right() - _overlay.width() - margin
    y = geometry.bottom() - _overlay.height() - margin

    _overlay.move(x, y)


def _getIcon(app):
    """
    Returns a cached icon for an AudioApp.
    """

    if app is None:
        return None

    if app.isMaster:
        key = "__master__"

        if key not in _icon_cache:
            _icon_cache[key] = getMasterPixmap()

        return _icon_cache[key]

    if app.execPath is None:
        return None

    if app.execPath not in _icon_cache:
        _icon_cache[app.execPath] = getAppPixmap(app.execPath)

    return _icon_cache[app.execPath]


def _getLabel(app) -> str:
    """
    Returns a short text fallback for apps without icons.
    """

    if app is None:
        return ""

    if app.isMaster:
        return "M"

    name = app.friendlyName or ""

    if name.lower().endswith(".exe"):
        name = name[:-4]

    return name[:2].upper()