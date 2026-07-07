import psutil
import pycaw.magic as pycaw_magic

from pycaw.magic import MagicManager
from pycaw.magic import MagicSession

from python_app.models.app_state import state as AS
from python_app import audio as au
from python_app import processes as proc
from python_app import appBuilder as ab

def _safeGetAppExec(self) -> str:
    """
    Safely resolves the executable name for a PyCAW magic root session.

    PyCAW's original _get_app_exec also initializes self.pid, so this
    replacement must preserve that behavior.
    """

    try:
        if hasattr(self, "_ctl2"):
            self.pid = self._ctl2.GetProcessId()
        elif not hasattr(self, "pid"):
            self.pid = 0

    except Exception:
        self.pid = 0
        return "unknown_pid_unresolved"

    if self.pid != 0:
        try:
            return psutil.Process(self.pid).name()

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            return f"unknown_pid_{self.pid}"

    try:
        returned_hresult = self._ctl2.IsSystemSoundsSession()

        if returned_hresult == 0:
            return "SndVol.exe"

    except Exception:
        pass

    return "unknown_pid_0"


pycaw_magic._MagicRootSession._get_app_exec = _safeGetAppExec


class SessionListener(MagicSession):
    """
    Handles audio session creation events.

    Existing sessions discovered during startup are not modified.
    New sessions created after the app list is available are synchronized
    with the volume of their matching AudioApp when possible.
    """

    def __init__(self):

        super().__init__()

        session_pid = self.magic_root_session.pid

        if session_pid == 0:
            return

        if not AS.apps:
            return

        friendly_pid = proc.resolveFriendlyProcessPID(session_pid)

        if friendly_pid is None:
            return

        for app in AS.apps:

            if app.isMaster:
                continue

            if friendly_pid == app.topProcessPID:
                au.syncVolume(session_pid, app)
                break

        AS.apps = ab.refreshApps(AS.apps)

MagicManager.magic_session(
    SessionListener
)