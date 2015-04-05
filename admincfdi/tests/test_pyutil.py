import unittest


class DescargaSAT(unittest.TestCase):

    def setUp(self):
        import time
        from unittest.mock import Mock
        from selenium import webdriver
        from admincfdi import pyutil

        self.webdriver = pyutil.webdriver
        pyutil.webdriver = Mock()
        pyutil.webdriver.FirefoxProfile = webdriver.FirefoxProfile

        self.sleep = time.sleep
        time.sleep = Mock()

        self.status = Mock()

    def tearDown(self):
        import time
        from admincfdi import pyutil

        pyutil.webdriver = self.webdriver
        time.sleep = self.sleep

    def test_get_firefox_profile(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        descarga = DescargaSAT()
        profile = descarga.get_firefox_profile('carpeta_destino')
        self.assertIsInstance(profile, webdriver.FirefoxProfile)

    def test_connect(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        profile = descarga.connect(profile, rfc='x', ciec='y')
        self.assertEqual(2, self.status.call_count)

    def test_disconnect_not_connected(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        descarga = DescargaSAT(status_callback=self.status)
        descarga.disconnect()
        self.assertEqual(0, self.status.call_count)

    def test_disconnect(self):
        from unittest.mock import Mock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = Mock()
        descarga.disconnect()
        self.assertEqual(2, self.status.call_count)


if __name__ == '__main__':
    unittest.main()
