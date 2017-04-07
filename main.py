import unittest
from CanDigitalPanel import rs232c


class Test_CanDigitalPanel(unittest.TestCase):
    CDP = rs232c.rs232c(5, 115200)  # CDP
#    CDP = rs232c.rs232c(8, 38400)   # TDP39X
    dic = rs232c.CDP_config

    @classmethod
    def setUpClass(cls):
        cls.CDP.is_opened()
        cls.CDP.into_program_mode()
        cls.CDP.initial_setting()

    @classmethod
    def tearDownClass(cls):
        cls.CDP.initial_setting()
        cls.CDP.outof_program_mode()
        cls.CDP.is_closed()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_setting_WriteRead(self, item, value):
        ret_w = self.CDP.setting_write(item, value)
        self.assertEquals(b"O\r\n", ret_w)

        ret_r = self.CDP.setting_read(item)
        ret_r_uni = int((ret_r.decode("utf-8")).split()[0])
        exp_r = value
        self.assertEqual(exp_r, ret_r_uni)

    def _test_single_setting(self):
        self._test_setting_WriteRead(30, 0)
        self._test_setting_WriteRead(30, 2)

    def _test_all_setting(self):
        keys = self.dic.config.keys()
        for i in keys:
            with self.subTest(i=i):
                begin, end, float_change = self.dic.config[i]
                for j in range(begin, end + 1):
                    with self.subTest(j=j):
                        # 小数変換
                        deci = round(j * float_change, 6)
                        self._test_setting_WriteRead(i, deci)

    def _test_setting_x(self, item):
        begin, end, float_change = self.dic.config[item][0:3]
        for i in range(begin, end + 1):
            with self.subTest(i=i):
                # 小数変換
                deci = round(i * float_change, 6)
                self._test_setting_WriteRead(item, deci)

    def test_setting_1_2_4_7_13_14_15_16_17_30(self):
        """range(0, 10)"""
        one_digit = [1,
                     2,
                     4,
                     7,
                     13,
                     14,
                     15,
                     16,
                     17,
                     30,
                     ]
        for j in one_digit:
            with self.subTest(j=j):
                self._test_setting_x(j)

    def _test_setting_3(self):
        """range is float, return is int, bug???"""
        self._test_setting_x(3)

    def _test_setting_12(self):
        """bug!!!!!"""
        self._test_setting_x(12)

    def _test_setting_6(self):
        """range(0, 100)"""
        self._test_setting_x(6)

    def _test_setting_5_10_11(self):
        """range(0, 10000)"""
        self._test_setting_x(5)
        self._test_setting_x(10)
        self._test_setting_x(11)

    def _test_setting_20_21_22_23(self):
        """range(0, 1000000)"""
        self._test_setting_x(20)
        self._test_setting_x(21)
        self._test_setting_x(22)
        self._test_setting_x(23)


if __name__ == "__main__":
    unittest.main()
