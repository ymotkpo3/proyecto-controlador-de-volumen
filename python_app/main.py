import time
import serial

import pycaw.magic
import python_app.audioSessionListener

from python_app import connection as con
from python_app import appBuilder as ab
from python_app import communication as com
from python_app import debug as deb
from python_app.models.app_state import state as ST


ST.apps = ab.refreshApps()
ST.selectedIndex = 0

deb.appDebug(ST.apps)
print(ST.apps[ST.selectedIndex])

ser = con.connect()

while True:

    try:

        if ser is None:
            ser = con.reconnect()

            if ser is not None:
                ST.apps = ab.refreshApps()
                ST.selectedIndex = 0
                print(ST.apps[ST.selectedIndex])

            else:
                time.sleep(1)
                continue

        msg = con.readSerial(ser)

        if msg:
            result = com.handleSerialCom(msg, ST.apps, ST.selectedIndex)

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