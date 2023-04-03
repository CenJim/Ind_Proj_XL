import serial
from serial.serialutil import SerialException
from time import sleep

# modified from https://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html
class SerialSender:
    TERMINATOR = '\n'.encode('UTF8')

    # Windows
    # def __init__(self, device='COM5', baud=115200, timeout=1):
    #     self.serial = serial.Serial(device, baud, timeout=timeout)

    # Mac
    def __init__(self, device='/dev/cu.usbmodem141301', baud=115200, timeout=1):
        self.serial = serial.Serial(device, baud, timeout=timeout)

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def send(self, text: str):
        line = '%s\n' % text
        self.serial.write(line.encode('UTF8'))

    def close(self):
        self.serial.close()


if __name__ == '__main__':

    previous_media_info = None

    # while True:
    #         # recreate the serial each time to allow handling disconnection
    #         try:
    #             serial_sender = SerialSender()
    #             serial_sender.send('something')
    #             print(serial_sender.receive())
    #             serial_sender.close()
    #         except SerialException:
    #             pass
    #         sleep(1)

    try:
        serial_sender = SerialSender()
        serial_sender.send('100')
        print(serial_sender.receive())
        serial_sender.close()
    except SerialException:
        pass
    sleep(1)