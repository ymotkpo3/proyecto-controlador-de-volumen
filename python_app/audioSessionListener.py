from pycaw.magic import MagicManager
from pycaw.magic import MagicSession

from python_app.models.app_state import state as AS
from python_app import audio as au
from python_app import processes as proc
from python_app import appBuilder as ab


defaultVolume = 1.0


class SessionListener(MagicSession):
    """
    Handles audio session creation events.

    Existing sessions are initialized before the application list is built.
    New sessions created later are synchronized with the volume of the
    matching AudioApp when possible.
    """

    def __init__(self):

        super().__init__()

        session_pid = self.magic_root_session.pid

        if session_pid == 0:
            return

        if not AS.apps:
            au.setMagicSessionVolume(
                self.magic_root_session,
                defaultVolume
            )
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