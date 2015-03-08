import unittest


class DescargaSAT(unittest.TestCase):

    def setUp(self):
        import configparser

        self.config = configparser.ConfigParser()
        self.config.read('functional_DescargaSAT.conf' )

    def test_uuid(self):
        import os
        import tempfile
        from pyutil import DescargaSAT

        def no_op(*args):
            pass

        rfc, ciec = open('credenciales.conf').readline()[:-1].split()
        seccion = self.config['uuid']
        uuid = seccion['uuid']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(uuid=uuid,
                type_search=1,
                día='00',
                rfc=rfc, ciec=ciec,
                carpeta_destino=destino,
                status_callback=no_op, download_callback=no_op)
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_rfc(self):
        import os
        import tempfile
        from pyutil import DescargaSAT

        def no_op(*args):
            pass

        rfc, ciec = open('credenciales.conf').readline()[:-1].split()
        seccion = self.config['rfc_emisor']
        rfc_emisor = seccion['rfc_emisor']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(año=año, mes=mes, día=día,
                rfc_emisor=rfc_emisor,
                rfc=rfc, ciec=ciec,
                carpeta_destino=destino,
                status_callback=no_op, download_callback=no_op)
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_año_mes_día(self):
        import os
        import tempfile
        from pyutil import DescargaSAT

        def no_op(*args):
            pass

        rfc, ciec = open('credenciales.conf').readline()[:-1].split()
        seccion = self.config['año_mes_día']
        año = seccion['año']
        mes = seccion['mes']
        día = seccion['día']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(año=año, mes=mes, día=día,
                rfc=rfc, ciec=ciec,
                carpeta_destino=destino,
                status_callback=no_op, download_callback=no_op)
            self.assertEqual(expected, len(os.listdir(destino)))

    def test_mes_completo(self):
        import os
        import tempfile
        from pyutil import DescargaSAT

        def no_op(*args):
            pass

        rfc, ciec = open('credenciales.conf').readline()[:-1].split()
        seccion = self.config['mes_completo_por_día']
        año = seccion['año']
        mes = seccion['mes']
        expected = int(seccion['expected'])
        with tempfile.TemporaryDirectory() as tempdir:
            destino = os.path.join(tempdir, 'cfdi-descarga')
            descarga = DescargaSAT(año=año, mes=mes, día='00',
                mes_completo_por_día=True,
                rfc=rfc, ciec=ciec,
                carpeta_destino=destino,
                status_callback=no_op, download_callback=no_op)
            self.assertEqual(expected, len(os.listdir(destino)))


if __name__ == '__main__':
	unittest.main()
