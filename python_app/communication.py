from python_app.models.audio_app import AudioApp
from python_app.models.serial_com_result import SerialComResult
from python_app import actions as act
from python_app.overlay import manager as overlayManager


def handleSerialCom(msg: str, apps: list[AudioApp], selected_index: int) -> SerialComResult:
    """
    Processes a command received from the volume controller.

    Depending on the received command, the application list,
    selected application, or audio volume may be modified.

    Args:
        msg:
            Command received through the serial connection.

        apps:
            Current AudioApp list.

        selected_index:
            Index of the currently selected AudioApp.

    Returns:
        SerialComResult:
            Result containing the updated application list,
            selected application index and debug message.
    """

    if msg == "update":
        apps = act.refresh(apps)

        if selected_index >= len(apps):
            selected_index = 0

        overlayManager.showSelection(apps[selected_index])

        return SerialComResult(apps, selected_index, "update")

    elif msg == "click":
        overlayManager.showSelection(apps[selected_index])

        return SerialComResult(apps, selected_index, "select")

    elif msg == "master":
        selected_index = 0

        overlayManager.showSelection(apps[selected_index])

        return SerialComResult(apps, selected_index, "master")

    elif msg == "appUP":
        selected_index = (selected_index + 1) % len(apps)

        overlayManager.showSelection(apps[selected_index])

        return SerialComResult(apps, selected_index, "appUP")

    elif msg == "appDWN":
        selected_index = (selected_index - 1) % len(apps)

        overlayManager.showSelection(apps[selected_index])

        return SerialComResult(apps, selected_index, "appDWN")

    elif msg == "volUP":
        if apps[selected_index].isMaster:
            act.masterVolUp()

            overlayManager.showVolume(apps[selected_index])

            return SerialComResult(apps, selected_index, "master volUP")

        act.volUp(apps[selected_index])

        overlayManager.showVolume(apps[selected_index])

        return SerialComResult(apps, selected_index, "volUP")

    elif msg == "volDWN":
        if apps[selected_index].isMaster:
            act.masterVolDown()

            overlayManager.showVolume(apps[selected_index])

            return SerialComResult(apps, selected_index, "master volDWN")

        act.volDown(apps[selected_index])

        overlayManager.showVolume(apps[selected_index])

        return SerialComResult(apps, selected_index, "volDWN")

    else:
        return SerialComResult(
            apps,
            selected_index,
            f"Unknown message: {msg}"
        )