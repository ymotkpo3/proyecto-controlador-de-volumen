import psutil
from python_app.config import SYSTEM, IGNORED

# Known limitation:
# Some applications based on helper processes or WebView2 may appear under the helper process name instead of the user-facing application name and that is the reason why this file does what it does.
# This will be improved in a future version using Windows application identity resolution instead of an heuristic.

def resolveFriendlyProcessPID(PID: int) -> int | None:
    """
    Resolves the user-facing process associated with an audio session.

    Starting from the provided PID, the process tree is traversed
    upwards until a suitable parent process is found.

    Processes listed in IGNORED are skipped.
    Traversal stops when a process listed in SYSTEM is reached.

    Audio sessions are often attached to helper or child processes
    instead of the application visible to the user.

    This function walks the process hierarchy to identify the most
    representative application process.

    Args:
        PID:
            Audio session process ID.

    Returns:
        int | None:
            PID of the best matching application process,
            or None if no suitable process can be resolved.
    """
    try:
        
        current = psutil.Process(PID)
        best_match = None

        while current:

            if current.name() in SYSTEM:

                if best_match:

                    break


            elif current.name() not in IGNORED:
                best_match = current

            current = current.parent()

        return best_match.pid
    
    except(AttributeError, psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

        return None

def getProcessNameAndPath(PID: int) -> str:
    """
    Returns the executable name of a process and the executable path of a process.

    Args:
        PID:
            Target process ID.

    Returns:
        Process executable name.
        Full executable path if available,
        otherwise None.
    """

    try:
        session = psutil.Process(PID)
        
        return session.name(), session.exe()

    except (psutil.NoSuchProcess, psutil.AccessDenied):

        return None, None