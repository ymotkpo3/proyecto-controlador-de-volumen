import sys
import time
import serial

import pycaw.magic
import python_app.audioSessionListener

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from python_app import connection as con
from python_app import appBuilder as ab
from python_app import communication as com
from python_app import debug as deb
from python_app import systemTray
from python_app.overlay import manager as overlayManager
from python_app.models.app_state import state as ST


qt_app = QApplication(sys.argv)

overlayManager.init()
systemTray.init()

ST.apps = ab.refreshApps()
ST.selectedIndex = 0

deb.appDebug(ST.apps)
print(ST.apps[ST.selectedIndex])

ser = con.connect()

lastReconnectAttempt = 0.0
RECONNECT_INTERVAL = 1.0

def serialTick():
    """
    Runs one iteration of the serial communication loop.

    This replaces the old while True loop so Qt can keep control of the
    main event loop. The behavior is the same: reconnect if needed, read
    serial messages, process commands and update the global app state.
    """

    global ser

    try:
        if ser is None:
            global lastReconnectAttempt

            now = time.monotonic()

            if now - lastReconnectAttempt < RECONNECT_INTERVAL:
                return

            lastReconnectAttempt = now

            ser = con.reconnect()

            if ser is not None:
                ST.apps = ab.refreshApps()
                ST.selectedIndex = 0
                print(ST.apps[ST.selectedIndex])

            return

        msg = con.readSerial(ser)

        if msg:
            result = com.handleSerialCom(
                msg,
                ST.apps,
                ST.selectedIndex
            )

            ST.apps = result.apps
            ST.selectedIndex = result.selected_index

            deb.printDebugMessage(
                ST.apps,
                ST.selectedIndex,
                result.debug_message
            )

    except serial.SerialException:

        if ser is not None:
            print("DISCONNECTED")

        ser = None


def cleanup():
    """
    Closes the serial connection before the application exits.
    """

    if ser is not None:
        ser.close()


serial_timer = QTimer()
serial_timer.timeout.connect(serialTick)
serial_timer.start(10)

qt_app.aboutToQuit.connect(cleanup)

sys.exit(qt_app.exec())