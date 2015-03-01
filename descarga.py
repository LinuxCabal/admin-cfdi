import time
from unittest.mock import Mock
from unittest.mock import MagicMock

from pyutil import DescargaSAT


def _set(widget_name, message, flag=True):
    print(message)

def sleep(sec=1):
    time.sleep(sec)

def main():
    page_init = 'https://cfdiau.sat.gob.mx/nidp/app/login?id=SATUPCFDiCon&' \
    'sid=0&option=credential&sid=0'
    page_cfdi = 'https://portalcfdi.facturaelectronica.sat.gob.mx/{}'

    rfc, pwd = open('pwd').readline()[:-1].split()
    data = {'type_invoice': 0, # recibidas
            'type_search': 0,  # por fecha
            'user_sat': {'target_sat': 'cfdi',
                            'user_sat': rfc,
                            'password': pwd},
            'search_uuid': '',
            'search_rfc': '',
            'search_year': '2014',
            'search_month': '10',
            'search_day': '00',
            'sat_month': ''
            }

    app = Mock()
    app._set.side_effect = _set

    pb = MagicMock()
    app._get_object.return_value = pb
    app.util.sleep = sleep

    app.g.SAT = {
        'ftp': 'ftp2.sat.gob.mx',
        'folder': '/Certificados/FEA',
        'form_login': 'IDPLogin',
        'user': 'Ecom_User_ID',
        'password': 'Ecom_Password',
        'date': 'ctl00_MainContent_RdoFechas',
        'date_from': 'ctl00_MainContent_CldFechaInicial2_Calendario_text',
        'date_from_name': 'ctl00$MainContent$CldFechaInicial2$Calendario_text',
        'date_to': 'ctl00_MainContent_CldFechaFinal2_Calendario_text',
        'date_to_name': 'ctl00$MainContent$CldFechaFinal2$Calendario_text',
        'year': 'DdlAnio',
        'month': 'ctl00_MainContent_CldFecha_DdlMes',
        'day': 'ctl00_MainContent_CldFecha_DdlDia',
        'submit': 'ctl00_MainContent_BtnBusqueda',
        'download': 'BtnDescarga',
        'emisor': 'ctl00_MainContent_TxtRfcReceptor',
        'receptor': 'ctl00_MainContent_TxtRfcReceptor',
        'uuid': 'ctl00_MainContent_TxtUUID',
        'combos': 'sbToggle',
        'found': 'No existen registros que cumplan con los criterios de',
        'subtitle': 'subtitle',
        'page_init': page_init,
        'page_cfdi': page_cfdi,
        'page_receptor': page_cfdi.format('ConsultaReceptor.aspx'),
        'page_emisor': page_cfdi.format('ConsultaEmisor.aspx'),
        }
    descarga = DescargaSAT(data, app)


if __name__ == '__main__':
	main()
