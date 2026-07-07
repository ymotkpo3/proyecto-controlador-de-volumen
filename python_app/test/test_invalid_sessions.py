import psutil

from python_app import audio
from python_app import audioSessionListener


class FakeProcess:
    def __init__(self, pid):
        self.pid = pid


class FakeSession:
    def __init__(self, pid=None):
        if pid is None:
            self.Process = None
        else:
            self.Process = FakeProcess(pid)


class FakeCtl2:
    def __init__(self, pid):
        self._pid = pid

    def GetProcessId(self):
        return self._pid

    def IsSystemSoundsSession(self):
        return 1


class FakeMagicRootSession:
    def __init__(self, pid):
        self._ctl2 = FakeCtl2(pid)


def _unsafeGetAppExec(self) -> str:
    """
    Simulates PyCAW's original unsafe behavior.
    This should crash when psutil.Process raises NoSuchProcess.
    """

    self.pid = self._ctl2.GetProcessId()
    return psutil.Process(self.pid).name()


def test_invalid_audio_session_without_process():
    session = FakeSession()

    result = audio.isValidAudioSession(session)

    print("Session without process:", result)


def test_invalid_audio_session_dead_pid():
    dead_pid = 99999999
    session = FakeSession(dead_pid)

    result = audio.isValidAudioSession(session)

    print("Session with dead PID:", result)


def test_original_pycaw_behavior_would_crash():
    fake_root_session = FakeMagicRootSession(1916)

    original_process = psutil.Process

    try:
        def process_that_disappeared(pid):
            raise psutil.NoSuchProcess(pid=pid)

        psutil.Process = process_that_disappeared

        try:
            _unsafeGetAppExec(fake_root_session)
            print("Original PyCAW behavior would crash: False")

        except psutil.NoSuchProcess:
            print("Original PyCAW behavior would crash: True")

    finally:
        psutil.Process = original_process


def test_safe_magic_get_app_exec_forced_nosuchprocess():
    fake_root_session = FakeMagicRootSession(1916)

    original_process = psutil.Process

    try:
        def process_that_disappeared(pid):
            raise psutil.NoSuchProcess(pid=pid)

        psutil.Process = process_that_disappeared

        result = audioSessionListener._safeGetAppExec(fake_root_session)

        print("Safe Magic forced NoSuchProcess:", result)
        print("PID preserved:", fake_root_session.pid)

    finally:
        psutil.Process = original_process


if __name__ == "__main__":
    test_invalid_audio_session_without_process()
    test_invalid_audio_session_dead_pid()
    test_original_pycaw_behavior_would_crash()
    test_safe_magic_get_app_exec_forced_nosuchprocess()