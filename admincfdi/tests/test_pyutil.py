import unittest


class LeeCredenciales(unittest.TestCase):

    def setUp(self):
        from unittest.mock import Mock
        from admincfdi import pyutil

        self.onefile = Mock()
        self.onefile.readline.return_value = 'rfc pwd'
        pyutil.open = Mock(return_value=self.onefile)

    def tearDown(self):
        from admincfdi import pyutil

        del pyutil.open

    def test_file_not_found(self):
        from admincfdi import pyutil

        pyutil.open.side_effect = FileNotFoundError
        util = pyutil.Util()
        status, rfc, pwd = util.lee_credenciales('ruta')
        self.assertEqual('Archivo no encontrado: ruta', status)

    def test_not_two_fields(self):
        from admincfdi import pyutil

        self.onefile.readline.return_value = ''
        util = pyutil.Util()
        status, rfc, pwd = util.lee_credenciales('ruta')
        self.assertEqual('No contiene dos campos: ruta', status)

    def test_success(self):
        from admincfdi import pyutil

        util = pyutil.Util()
        status, rfc, pwd = util.lee_credenciales('ruta')
        self.assertEqual('Ok', status)

    def test_surplus_whitespace_is_ok(self):
        from admincfdi import pyutil

        self.onefile.readline.return_value = ' \t rfc \t  pwd  \r\n'
        util = pyutil.Util()
        status, rfc, pwd = util.lee_credenciales('ruta')
        self.assertEqual('rfc', rfc)
        self.assertEqual('pwd', pwd)


class DescargaSAT(unittest.TestCase):

    def setUp(self):
        import time
        from unittest.mock import Mock
        from selenium import webdriver
        from admincfdi import pyutil

        self.webdriver = pyutil.webdriver
        pyutil.webdriver = Mock()
        pyutil.webdriver.FirefoxProfile = webdriver.FirefoxProfile

        self.WebDriverWait = pyutil.WebDriverWait
        pyutil.WebDriverWait = Mock()

        self.sleep = time.sleep
        time.sleep = Mock()

        self.status = Mock()
        self.transfer = Mock()

        pyutil.print = Mock()

    def tearDown(self):
        import time
        from admincfdi import pyutil

        pyutil.webdriver = self.webdriver
        pyutil.WebDriverWait = self.WebDriverWait
        time.sleep = self.sleep
        del pyutil.print

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
        self.assertEqual(3, self.status.call_count)

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

    def test_search_not_connected(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        results = descarga.search(uuid='uuid')
        self.assertEqual(0, len(results))

    def test_search_uuid(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        results = descarga.search(uuid='uuid', día='00')
        self.assertEqual(0, len(results))

    def test_search_facturas_emitidas(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        results = descarga.search(facturas_emitidas=True,
                    año=1, mes=1)
        self.assertEqual(0, len(results))

    def test_search_rfc_emisor(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        results = descarga.search(rfc_emisor='x')
        self.assertEqual(0, len(results))

    def test_search_not_found(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.g.SAT['found'] = 'no'
        descarga.browser = MagicMock()
        c = MagicMock()
        descarga.browser.find_elements_by_class_name.return_value = [c]
        c.get_attribute.return_value = 'x no x'
        c.is_displayed.return_value = True
        results = descarga.search()
        self.assertEqual(0, len(results))

    def test_search_not_found_exception(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        c = MagicMock()
        descarga.browser.find_elements_by_class_name.side_effect = Exception()
        results = descarga.search()
        self.assertEqual(0, len(results))

    def test_search_mes_eq_día(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        link = MagicMock()
        descarga.browser.find_elements_by_link_text.return_value = [link]
        combo = descarga.browser.find_element_by_id.return_value
        combo.get_attribute.return_value = 'sb'
        r = link.find_element_by_xpath.return_value
        p = r.find_element_by_xpath.return_value
        p.get_attribute.return_value = 'sb2'
        results = descarga.search(día='01', mes='01')
        self.assertEqual(0, len(results))

    def test_search_mes_completo_por_día(self):
        from unittest.mock import MagicMock, Mock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        descarga._download_sat_month = Mock(return_value=[])
        results = descarga.search(día='00',
                                  mes_completo_por_día=True)
        self.assertEqual(0, len(results))

    def test_search_mes_ne_día(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status)
        descarga.browser = MagicMock()
        results = descarga.search(día='01', mes='02')
        self.assertEqual(0, len(results))

    def test_download(self):
        from unittest.mock import MagicMock
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()
        descarga = DescargaSAT(status_callback=self.status,
            download_callback=self.transfer)
        descarga.browser = MagicMock()
        docs = [MagicMock()]
        descarga.download(docs)


if __name__ == '__main__':
    unittest.main()
