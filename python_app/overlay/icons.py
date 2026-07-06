from PySide6.QtGui import QImage, QPixmap
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