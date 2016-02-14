import unittest


class DescargaSAT(unittest.TestCase):

    def setUp(self):
        import configparser
        from admincfdi.pyutil import Util

        self.config = configparser.ConfigParser()
        self.config.read('functional_DescargaSAT.conf' )

        util = Util()
        status, self.rfc, self.ciec = util.lee_credenciales('credenciales.conf')
        self.assertEqual('Ok', status)

    def test_connect_disconnect(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()

        def no_op(*args):
            pass

        descarga = DescargaSAT(status_callback=no_op)
        status = descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
        self.assertTrue(status)
        descarga.disconnect()

    def test_connect_fail(self):
        from admincfdi.pyutil import DescargaSAT
        from selenium import webdriver

        profile = webdriver.FirefoxProfile()

        def no_op(*args):
            pass

        descarga = DescargaSAT(status_callback=no_op)
        status = descarga.connect(profile, rfc='x', ciec='y')
        self.assertFalse(status)
        descarga.browser.close()

    def test_search_uuid(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['uuid']
        uuid = seccion['uuid']
        expected = int(seccion['expected'])
        descarga = DescargaSAT(status_callback=no_op,
                                download_callback=no_op)
        profile = descarga.get_firefox_profile('destino')
        descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
        result = descarga.search(uuid=uuid,
            día='00')
        descarga.disconnect()
        self.assertEqual(expected, len(result))

    def test_uuid(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['uuid']
        uuid = seccion['uuid']
        expected = int(seccion['expected'])
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(uuid=uuid, día='00')
            descarga.download(docs)
            descarga.disconnect()
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
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día=día,
                rfc_emisor=rfc_emisor)
            descarga.download(docs)
            descarga.disconnect()
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
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día=día)
            descarga.download(docs)
            descarga.disconnect()
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_hora_minuto_inicial(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['hora_minuto_inicial']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        hora_inicial =  seccion['hora_inicial']
        minuto_inicial = seccion['minuto_inicial']
        expected = int(seccion['expected'])
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día=día,
                                   hora_inicial=hora_inicial,
                                   minuto_inicial=minuto_inicial)
            descarga.download(docs)
            descarga.disconnect()
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_hora_minuto_final(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['hora_minuto_final']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        hora_final =  seccion['hora_final']
        minuto_final = seccion['minuto_final']
        expected = int(seccion['expected'])
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día=día,
                                   hora_final=hora_final, minuto_final=minuto_final)
            descarga.download(docs)
            descarga.disconnect()
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_segundo_inicial_final(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['segundo_inicial_final']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        hora_inicial =  seccion['hora_inicial']
        minuto_inicial = seccion['minuto_inicial']
        segundo_inicial = seccion['segundo_inicial']
        hora_final =  seccion['hora_final']
        minuto_final = seccion['minuto_final']
        segundo_final = seccion['segundo_final']
        expected = int(seccion['expected'])
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día=día,
                                   hora_inicial=hora_inicial, minuto_inicial=minuto_inicial,
                                   segundo_inicial=segundo_inicial,
                                   hora_final=hora_final, minuto_final=minuto_final,
                                   segundo_final=segundo_final)
            descarga.download(docs)
            descarga.disconnect()
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
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día='00',
                mes_completo_por_día=True)
            descarga.download(docs)
            descarga.disconnect()
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_emitidas(self):
        import os
        import tempfile
        from admincfdi.pyutil import DescargaSAT

        def no_op(*args):
            pass

        seccion = self.config['emitidas']
        año = seccion['año']
        mes = seccion['mes']
        expected = int(seccion['expected'])
        descarga = DescargaSAT(status_callback=no_op,
                               download_callback=no_op)
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            profile = descarga.get_firefox_profile(destino)
            descarga.connect(profile, rfc=self.rfc, ciec=self.ciec)
            docs = descarga.search(año=año, mes=mes, día='00',
                facturas_emitidas=True)
            descarga.disconnect()
            self.assertEqual(expected, len(docs))


if __name__ == '__main__':
	unittest.main()
