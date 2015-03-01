import argparse
import time
import datetime
from unittest.mock import Mock
from unittest.mock import MagicMock

from pyutil import DescargaSAT


def _set(widget_name, message, flag=True):
    print(message)

def sleep(sec=1):
    time.sleep(sec)

def process_command_line_arguments():
    parser = argparse.ArgumentParser(description='Descarga CFDIs del SAT a una carpeta local')

    default_archivo_credenciales = 'pwd'
    help = 'Archivo con credenciales para el SAT. ' \
           'RFC y CIEC en el primer renglón y ' \
           'separadas por un espacio. ' \
           'El predeterminado es %(default)s'
    parser.add_argument('--archivo-de-credenciales',
                        help=help, default=default_archivo_credenciales)

    default_carpeta_destino = 'cfdi'
    help = 'Carpeta local para guardar los CFDIs descargados ' \
           'El predeterminado es %(default)s'
    parser.add_argument('--carpeta-destino',
                        help=help, default=default_carpeta_destino)

    help = 'Descargar facturas emitidas. ' \
           'Por omisión se descargan facturas recibidas'
    parser.add_argument('--facturas-emitidas',
                        action='store_const', const=1,
                        help=help, default=2)

    help = 'UUID. Por omisión no se usa en la búsqueda. ' \
           'Esta opción tiene precedencia sobre las demás ' \
           'opciones de búsqueda.'
    parser.add_argument('--uuid',
                        help=help, default='')

    today = datetime.date.today()
    help = 'Año. El valor por omisión es el año en curso'
    parser.add_argument('--año',
                        help=help, default=str(today.year))

    help = 'Mes. El valor por omisión es el mes en curso'
    parser.add_argument('--mes',
                        help=help, default='{:02d}'.format(today.month))

    help = "Día. El valor por omisión es '00', " \
           'significa no usar el día en la búsqueda'
    parser.add_argument('--día',
                        help=help, default='00')

    args=parser.parse_args()
    return args

def main():
    args = process_command_line_arguments()

    page_init = 'https://cfdiau.sat.gob.mx/nidp/app/login?id=SATUPCFDiCon&' \
    'sid=0&option=credential&sid=0'
    page_cfdi = 'https://portalcfdi.facturaelectronica.sat.gob.mx/{}'

    rfc, pwd = open(args.archivo_de_credenciales).readline()[:-1].split()
    data = {'type_invoice': args.facturas_emitidas,
            'type_search': 1 * (args.uuid != ''),
            'user_sat': {'target_sat': args.carpeta_destino,
                            'user_sat': rfc,
                            'password': pwd},
            'search_uuid': args.uuid,
            'search_rfc': '',
            'search_year': args.año,
            'search_month': args.mes,
            'search_day': args.día,
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
