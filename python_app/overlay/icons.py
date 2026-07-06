from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QPolygonF
from win32com.shell import shell, shellcon


def getAppPixmap(path: str | None) -> QPixmap | None:
    """
    Returns the Windows executable icon as a QPixmap.

    Args:
        path:
            Executable path.

    Returns:
        QPixmap if the icon could be loaded, otherwise None.
    """

    if not path:
        return None

    success, info = shell.SHGetFileInfo(
        path,
        0,
        shellcon.SHGFI_ICON | shellcon.SHGFI_LARGEICON
    )

    if not success:
        return None

    hicon = info[0]
    image = QImage.fromHICON(hicon)

    if image.isNull():
        return None

    return QPixmap.fromImage(image)


def getMasterPixmap(size: int = 24) -> QPixmap:
    """
    Creates a simple speaker icon for the master volume entry.

    Args:
        size:
            Width and height of the generated icon.

    Returns:
        QPixmap containing a speaker icon.
    """

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(Qt.GlobalColor.white)

    speaker = QPolygonF([
        QPointF(size * 0.15, size * 0.40),
        QPointF(size * 0.34, size * 0.40),
        QPointF(size * 0.58, size * 0.24),
        QPointF(size * 0.58, size * 0.76),
        QPointF(size * 0.34, size * 0.60),
        QPointF(size * 0.15, size * 0.60),
    ])

    painter.drawPolygon(speaker)

    pen = QPen(Qt.GlobalColor.white)
    pen.setWidthF(2.0)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    painter.drawArc(
        QRectF(size * 0.50, size * 0.35, size * 0.22, size * 0.30),
        -45 * 16,
        90 * 16
    )

    painter.drawArc(
        QRectF(size * 0.47, size * 0.25, size * 0.38, size * 0.50),
        -45 * 16,
        90 * 16
    )

    painter.end()

    return pixmap