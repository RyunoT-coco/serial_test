import serial
import math

class CDP_config:
    config = {
        # item: [begin, end, float_change]
        1: [0, 2, 1],
        2: [0, 5, 1],
        3: [1, 99, 0.1],  # [0.1, 9.9]
        4: [1, 9, 1],
        5: [2, 9999, 1],
        6: [1, 99, 1],
        7: [0, 1, 1],
        10: [1, 9999, 1],
        11: [1, 9999, 1],
        12: [0, 6, 1],
        13: [0, 1, 1],
        14: [0, 1, 1],
        15: [0, 1, 1],
        16: [0, 1, 1],
        17: [0, 1, 1],
        20: [1, 99999, 1],
        21: [1, 99999, 1],
        22: [1, 99999, 1],
        23: [1, 99999, 1],
        30: [0, 3, 1],
    }


class rs232c:
    def __init__(self, port_num):
        self.ser = serial.Serial(port=port_num - 1,
                                 baudrate=2400,
                                 bytesize=8,
                                 parity='N',
                                 stopbits=1,
                                 timeout=1)
        self.read_buff = None
        self.write_buff = None

    def rs232c_close(self):
        self.ser.close()
        return

    def _rs232c_readline(self):
        self.read_buff = self.ser.readline()
        return

    def _rs232c_write(self, write_line):
        self.write_buff = write_line
        self.ser.write(self.write_buff.encode("utf-8"))
        return self._rs232c_readline()

    def into_program_mode(self):
        self._rs232c_write("P")
        return self.read_buff

    def outof_program_mode(self):
        self._rs232c_write("E\r")
        return self.read_buff

    def CDP_setting_read(self, item):
        line = "RP" + str(item).zfill(2) + "\r"
        self._rs232c_write(line)
        return self.read_buff

    def CDP_setting_write(self, item, value):
        line = "WP" + str(item).zfill(2) + ", " + str(value) + "\r"
        self._rs232c_write(line)
        return self.read_buff

    def CDP_setting_test(self, item, value_range):
        for i in range(value_range):
            """writing test"""
            ret_w = self.CDP_setting_write(item, i)
            if not ret_w == "O\r\n":
                print("test failed {0}".format(self.write_buff))

            """reading test"""
            ret_r = self.CDP_setting_read(item)
            if not ret_r == str(i) + "\r\n":
                print("test failed {0}".format(self.write_buff))

    def all_CDP_setting_test(self):
        keys = CDP_config.config.keys()
        for i in keys:
            begin, end, float_change = CDP_config.config[i]
            for j in range(begin, end + 1):
                # 小数変換
                deci = round(j * float_change, 6)
                self.CDP_setting_test(i, j)
            print("Finish WP{0} and RP{0} test".format(str(i).zfill(2)))

        print("Finish all_setting_test")
