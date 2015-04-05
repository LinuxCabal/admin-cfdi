import unittest


class DescargaSAT(unittest.TestCase):

    def setUp(self):
        import configparser

        self.config = configparser.ConfigParser()
        self.config.read('functional_DescargaSAT.conf' )

        self.rfc, self.ciec = open('credenciales.conf').readline()[:-1].split()

    def test_connect(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()

        def no_op(*args):
            pass

        descarga = DescargaSAT(status_callback=no_op)
        descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)

    def test_uuid(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['uuid']
        uuid = seccion['uuid']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(status_callback=no_op,
                                   download_callback=no_op)
            descarga._download_sat(uuid=uuid,
                type_search=1,
                día='00',
                rfc=self.rfc, ciec=self.ciec,
                carpeta_destino=destino)
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_rfc(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['rfc_emisor']
        rfc_emisor = seccion['rfc_emisor']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(status_callback=no_op,
                                   download_callback=no_op)
            descarga._download_sat(año=año, mes=mes, día=día,
                rfc_emisor=rfc_emisor,
                rfc=self.rfc, ciec=self.ciec,
                carpeta_destino=destino)
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_año_mes_día(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['año_mes_día']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(status_callback=no_op,
                                   download_callback=no_op)
            descarga._download_sat(año=año, mes=mes, día=día,
                rfc=self.rfc, ciec=self.ciec,
                carpeta_destino=destino)
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_mes_completo(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['mes_completo_por_día']
        año = seccion['año']
        mes = seccion['mes']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(status_callback=no_op,
                                   download_callback=no_op)
            descarga._download_sat(año=año, mes=mes, día='00',
                mes_completo_por_día=True,
                rfc=self.rfc, ciec=self.ciec,
                carpeta_destino=destino)
            self.assertEqual(expected, len(os.listdir(destino)))


if __name__ == '__main__':
	unittest.main()
