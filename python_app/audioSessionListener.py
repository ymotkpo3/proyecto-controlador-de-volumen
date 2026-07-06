from pycaw.magic import MagicManager
from pycaw.magic import MagicSession

from python_app.models.app_state import state as AS
from python_app import audio as au
from python_app import processes as proc
from python_app import appBuilder as ab

class SessionListener(MagicSession):
    """
    Handles audio session creation events.

    New sessions created later are synchronized with the volume of the
    matching AudioApp when possible.
    """

    def __init__(self):

        super().__init__()

        session_pid = self.magic_root_session.pid

        if session_pid == 0:
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