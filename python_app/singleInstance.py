import ctypes


ERROR_ALREADY_EXISTS = 183

_mutex_handle = None


def isAlreadyRunning() -> bool:
    """
    Checks whether another Megaknob instance is already running.

    Returns:
        True if another instance already owns the application mutex.
    """

    global _mutex_handle

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True
    )

    _mutex_handle = kernel32.CreateMutexW(
        None,
        False,
        "MegaknobSingleInstanceMutex"
    )

    last_error = ctypes.get_last_error()

    return last_error == ERROR_ALREADY_EXISTS