from pycaw.magic import MagicManager
from pycaw.magic import MagicSession
from python_app.models.app_state import state as AS
from python_app import audio as au
from python_app import processes as proc
from python_app import appBuilder as ab

defaultVolume = 1

class SessionListener(MagicSession):

    def __init__(self):

        super().__init__()

        print(vars(self.magic_root_session))

        if AS.apps == None or AS.apps == []:
            au.setFixedVolume(self.magic_root_session.pid, defaultVolume)
        else:
            friendly_pid = proc.resolveFriendlyProcessPID(
                self.magic_root_session.pid
            )

            for app in AS.apps:

                if app.isMaster:
                    print("MASTER")

                if friendly_pid == app.topProcessPID:

                    if self.magic_root_session.pid not in app.audioSessionPIDs:
                        print("sincronizando")
                        au.SyncVolume(
                            self.magic_root_session.pid,
                            app
                        )

                        break
                    else:
                        pass
            AS.apps = ab.refreshApps(AS.apps)
                        
                    

MagicManager.magic_session(
    SessionListener
)