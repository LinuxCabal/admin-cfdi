#!
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import os
import sys
import logging
import logging.config


class Global(object):
    DEBUG = False
    WIN = 'win32'
    OS = sys.platform
    MAIN = 'mainwindow'
    TITLE = 'Admin CFDI - Factura Libre'
    CWD = os.getcwd()
    PATHS = {
        'current': CWD,
        'img': os.path.join(CWD, 'img'),
        'ui': os.path.join(CWD, 'ui'),
        'OPENSSL': 'openssl',
        'XSLTPROC': 'xsltproc',
        'CER': os.path.join(CWD, 'cer_pac'),
        'BIN': os.path.join(CWD, 'bin'),
        'XSLT_CER': os.path.join(CWD, 'bin', 'get_certificado.xslt'),
        'XSLT_SELLO': os.path.join(CWD, 'bin', 'get_sello.xslt'),
        'XSLT_SELLO_SAT': os.path.join(CWD, 'bin', 'get_sello_sat.xslt'),
        'XSLT_CADENA': os.path.join(CWD, 'bin', 'cfdi_{}.xslt'),
        'XSLT_TIMBRE': os.path.join(CWD, 'bin', 'timbre_1.0.xslt'),
    }
    EXT_XML = '.xml'
    EXT_ODS = '.ods'
    EXT_CSV = '.csv'
    EXT_PDF = '.pdf'
    EXT_JSON = '.json'
    EXT_CER = '.cer'
    EXT_EXE = '.exe'
    if OS == WIN:
        PATHS['XSLTPROC'] = os.path.join(
            PATHS['BIN'], PATHS['XSLTPROC'] + EXT_EXE)
        PATHS['OPENSSL'] = os.path.join(
            PATHS['BIN'], PATHS['OPENSSL'] + EXT_EXE)
    FILES = {
        'main': os.path.join(PATHS['ui'], 'mainwindow.ui'),
        'config': os.path.join(PATHS['ui'], 'config.ini'),
        'log': os.path.join(CWD, 'admincfdi.log'),
    }
    FILE_NAME = '{serie}{folio:06d}_{fecha}_{receptor_rfc}'
    CADENA = '||{version}|{UUID}|{FechaTimbrado}|{selloCFD}|{noCertificadoSAT}||'
    CELL_TYPE = 'ScCellObj'
    LIMIT_MARGIN = 23000
    CLEAN = "\{(\w.+)\}"
    PESO = ('mxn', 'mxp', 'm.n.', 'p', 'mn', 'pmx', 'mex')
    DOLAR = ('dólar', 'dólares', 'dolar', 'dolares', 'usd')
    ICON = os.path.join(PATHS['img'], 'favicon.png')
    YEAR_INIT = 2011
    FIELDS_REPORT = '{UUID}|{serie}|{folio}|{emisor_rfc}|{emisor_nombre}|' \
        '{receptor_rfc}|{receptor_nombre}|{fecha}|{FechaTimbrado}|' \
        '{tipoDeComprobante}|{Moneda}|{TipoCambio}|{subTotal}|' \
        '{totalImpuestosTrasladados}|{total}'
    FIELDS_CURRENCY = (
        'TipoCambio',
        'subTotal',
        'totalImpuestosTrasladados',
        'totalImpuestosRetenidos',
        'total',
        'descuento')
    COLORS = {
        'FOCUS_IN': '#ffffca',
        'FOCUS_OUT': '#ffffff',
        'DEFAULT': '#d9d9d9',
    }
    CONTROLS = {
        'button_save_emisor': {
            'width': 100,
            },
        'button_delete_emisor': {
            'width': 100,
            },
        'button_download_sat': {
            'width': 100,
            },
        'button_exit': {
            'width': 100,
            },
        'button_save_mail_server': {
            'width': 100,
            },
        'button_delete_mail_server': {
            'width': 100,
            },
        'button_download_mail': {
            'width': 100,
            },
        'button_organizate_xml': {
            'width': 100,
            },
        'button_generate_pdf': {
            'width': 100,
            },
        'button_generate_report': {
            'width': 120,
            },
        'button_save_xml_user': {
            'width': 100,
            },
        'button_delete_xml_user': {
            'width': 100,
            },
        'button_save_pdf_user': {
            'width': 100,
            },
        'button_delete_pdf_user': {
            'width': 100,
            },
        'button_save_report_user': {
            'width': 100,
            },
        'button_delete_report_user': {
            'width': 100,
            },
        'button_save_report_title': {
            'width': 100,
            },
        'button_delete_report_title': {
            'width': 100,
            },

        }
    PREFIX = {
        '2.0': '{http://www.sat.gob.mx/cfd/2}',
        '2.2': '{http://www.sat.gob.mx/cfd/2}',
        '3.0': '{http://www.sat.gob.mx/cfd/3}',
        '3.2': '{http://www.sat.gob.mx/cfd/3}',
        'TIMBRE': '{http://www.sat.gob.mx/TimbreFiscalDigital}',
        'NOMINA': '{http://www.sat.gob.mx/nomina}',
        'IMP_LOCAL': '{http://www.sat.gob.mx/implocal}',
        'IEDU': '{http://www.sat.gob.mx/iedu}',
        'DONATARIA': '{http://www.sat.gob.mx/donat}',
    }
    page_init = 'https://cfdiau.sat.gob.mx/nidp/app/login?id=SATUPCFDiCon&' \
        'sid=0&option=credential&sid=0'
    page_cfdi = 'https://portalcfdi.facturaelectronica.sat.gob.mx/{}'
    SAT = {
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
    frm_1 = '%(asctime)s - %(levelname)s - %(lineno)s - %(message)s'
    CONF_LOG = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
                'to_file': {
                    'class': 'logging.FileHandler',
                    'formatter': 'myFormat',
                    'filename': FILES['log']
                    },
                'to_screen': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'myFormat',
                    },
                },
        'loggers': {
            'AdminCFDI':{
                'handlers': ['to_file'],
                'level': 'ERROR',
                },
            'AdminCFDI_screen':{
                'handlers': ['to_screen'],
                'level': 'DEBUG',
                'propagate': True,
                },
            },
        'formatters': {
            'myFormat': {
                'format': frm_1,
                'datefmt': '%d-%b-%Y %H:%M:%S'
            }
        }
    }
    logging.config.dictConfig(CONF_LOG)
    if DEBUG:
        LOG = logging.getLogger('AdminCFDI_screen')
    else:
        LOG = logging.getLogger('AdminCFDI')