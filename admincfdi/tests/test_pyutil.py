import unittest


class DescargaSAT(unittest.TestCase):

    def test_get_firefox_profile(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        descarga = DescargaSAT()
        profile = descarga.get_firefox_profile('carpeta_destino')
        self.assertIsInstance(profile, webdriver.FirefoxProfile)


if __name__ == '__main__':
    unittest.main()
