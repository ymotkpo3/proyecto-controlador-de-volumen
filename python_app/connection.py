import serial.tools.list_ports
import serial

def findDevicePort() -> str | None:
    """
    Searches for the volume controller USB device.

    Returns:
        str | None:
            Serial port name assigned to the device if found
            (e.g. "COM5"), otherwise None.
    """
    for port in serial.tools.list_ports.comports():

        if (port.vid == 0x2E8A and port.pid == 0x000A):

            return port.device

    return None

def createSerialConnection(port: str) -> serial.Serial:
    """
    Creates a serial connection to the specified port.

    Args:
        port:
            Serial port name.

    Returns:
        serial.Serial:
            Configured serial connection object.
    """
    return serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.01
    )

def connect() -> serial.Serial | None:
    """
    Attempts to connect to the volume controller device.

    Returns:
        serial.Serial | None:
            Serial connection if the device is found,
            otherwise None.
    """
    port = findDevicePort()

    if port is None:

        return None

    return createSerialConnection(port)

def readSerial(ser: serial.Serial) -> str | None:
    """
    Reads a single line from the serial connection.

    Args:
        ser:
            Active serial connection.

    Returns:
        str | None:
            Decoded message if data was received,
            otherwise None.
    """

    if ser.in_waiting <= 0:
        return None

    line = ser.readline()

    if not line:
        return None

    return line.decode(errors="ignore").strip() or None

def reconnect() -> serial.Serial | None:
    """
    Attempts to reconnect to the volume controller device.

    Returns:
        serial.Serial | None:
            Serial connection if reconnection succeeds,
            otherwise None.
    """
    ser = connect()

    if ser is not None:

        print("RECONNECTED")

    return ser
