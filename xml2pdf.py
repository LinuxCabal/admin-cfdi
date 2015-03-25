import argparse

from pyutil import CSVPDF
from pyutil import Util

def process_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Crea un PDF desde una plantilla CSV')

    help = 'Archivo XML origen.'
    parser.add_argument('-a', '--archivo-xml', help=help, default='')

    help = 'Directorio origen.'
    parser.add_argument('-o', '--directorio-origen', help=help, default='')

    args = parser.parse_args()
    return args


def main():
    ext_pdf = '.pdf'
    args = process_command_line_arguments()
    util = Util()

    if args.archivo_xml and util.exists(args.archivo_xml):
        path_pdf = util.replace_extension(args.archivo_xml, ext_pdf)
        pdf = CSVPDF(args.archivo_xml)
        if pdf.xml:
            pdf.make_pdf()
            pdf.output(path_pdf, 'F')
    if args.directorio_origen:
        files = util.get_files(args.directorio_origen)
        for f in files:
            path_pdf = util.replace_extension(f, ext_pdf)
            pdf = CSVPDF(f)
            if pdf.xml:
                pdf.make_pdf()
                pdf.output(path_pdf, 'F')

if __name__ == '__main__':
    main()
