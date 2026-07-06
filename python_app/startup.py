import sys
import winreg
from pathlib import Path


APP_NAME = "Megaknob"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _getStartupCommand() -> str:
    """
    Builds the command used by Windows to start the app at login.

    Returns:
        Command string stored in the Windows Run registry key.
    """

    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'

    project_root = Path(__file__).resolve().parent.parent

    return (
        f'cmd /c start "" '
        f'/D "{project_root}" '
        f'"{sys.executable}" -m python_app.main'
    )


def isStartupEnabled() -> bool:
    """
    Checks whether automatic startup is enabled for the current user.

    Returns:
        True if the startup registry entry exists.
    """

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            RUN_KEY,
            0,
            winreg.KEY_READ
        ) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True

    except FileNotFoundError:
        return False


def enableStartup() -> None:
    """
    Enables automatic startup for the current Windows user.
    """

    command = _getStartupCommand()

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        RUN_KEY,
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(
            key,
            APP_NAME,
            0,
            winreg.REG_SZ,
            command
        )


def disableStartup() -> None:
    """
    Disables automatic startup for the current Windows user.
    """

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            RUN_KEY,
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(
                key,
                APP_NAME
            )

    except FileNotFoundError:
        pass