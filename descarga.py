import argparse
import time
import datetime

from pyutil import DescargaSAT


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

    help = 'RFC del emisor. Por omisión no se usa en la búsqueda.'
    parser.add_argument('--rfc-emisor',
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

    help = 'Mes completo por día. Por omisión no se usa en la búsqueda.'
    parser.add_argument('--mes-completo', action='store_const', const=True,
                        help=help, default=False)

    args=parser.parse_args()
    return args

def main():

    args = process_command_line_arguments()
    rfc, pwd = open(args.archivo_de_credenciales).readline()[:-1].split()
    data = {'type_invoice': args.facturas_emitidas,
            'type_search': 1 * (args.uuid != ''),
            'user_sat': {'target_sat': args.carpeta_destino,
                            'user_sat': rfc,
                            'password': pwd},
            'search_uuid': args.uuid,
            'search_rfc': args.rfc_emisor,
            'search_year': args.año,
            'search_month': args.mes,
            'search_day': args.día,
            'sat_month': args.mes_completo
            }
    descarga = DescargaSAT(data)


if __name__ == '__main__':
	main()
