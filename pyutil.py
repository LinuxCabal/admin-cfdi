#!/usr/bin/env python
#! coding: utf-8

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
import re
import csv
import json
import ftplib
import time
import calendar
import imaplib
import email
import hashlib
import shutil
import subprocess
import tempfile
import signal
import pyqrcode
from datetime import datetime
from string import Template
from xml.etree import ElementTree as ET
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from pysimplesoap.client import SoapClient, SoapFault
from selenium import webdriver
from values import Global
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


WIN = 'win32'
MAC = 'darwin'
LINUX = 'linux'


if sys.platform == WIN:
    from win32com.client import Dispatch
elif sys.platform == LINUX:
    import uno
    from com.sun.star.beans import PropertyValue
    from com.sun.star.beans.PropertyState import DIRECT_VALUE
    from com.sun.star.awt import Size


class SAT(object):
    _webservice = 'https://consultaqr.facturaelectronica.sat.gob.mx/' \
        'consultacfdiservice.svc?wsdl'

    def __init__(self):
        self.error = ''
        self.msg = ''

    def get_estatus(self, data):
        try:
            args = '?re={emisor_rfc}&rr={receptor_rfc}&tt={total}&id={uuid}'
            client = SoapClient(wsdl = self._webservice)
            fac = args.format(**data)
            res = client.Consulta(fac)
            if 'ConsultaResult' in res:
                self.msg = res['ConsultaResult']['Estado']
                return True
            return False
        except SoapFault as sf:
            self.error = sf.faultstring
            return False


class ValidCFDI(object):
    WIN = 'win32'

    def __init__(self, path_xml, g):
        self.path_xml = path_xml
        self.g = g
        self.error = ''
        self.msg = ''
        self.PATHS = {}
        self.xml = ET.parse(path_xml).getroot()
        self.ver = self.xml.attrib['version']
        self._config()

    def _config(self):
        self.g.PATHS['XSLT_CADENA'] = self._join(
            self.g.PATHS['XSLT_CADENA'].format(self.ver))
        self.PATHS['KEY'] = self._get_path_temp('key')
        self.PATHS['SELLO'] = self._get_path_temp('stamp')
        self.PATHS['CADENA'] = self._get_path_temp('cadena')
        self.PATHS['CER'] = ''
        return

    def _join(self, *paths):
        return os.path.join(*paths)

    def _get_path_temp(self, name=''):
        if sys.platform == self.WIN:
            return tempfile.TemporaryFile(mode='w').name
        if name:
            return self._join(tempfile.gettempdir(), name)
        else:
            return tempfile.mkstemp()[1]

    def _exists(self, path):
        return os.path.exists(path)

    def _get_file_size(self, path):
        try:
            return os.path.getsize(path)
        except:
            return 0

    def _file_kill(self, path):
        try:
            os.remove(path)
        except:
            pass

    def _get_cer_sat(self):
        timbre = '{}Complemento/{}TimbreFiscalDigital'.format(
            self.g.PREFIX[self.ver], self.g.PREFIX['TIMBRE'])
        node = self.xml.find(timbre)
        cer_sat = node.attrib['noCertificadoSAT']
        self.PATHS['CER'] = self._join(
            self.g.PATHS['CER'], cer_sat + self.g.EXT_CER)
        if self._exists(self.PATHS['CER']):
            return True
        for i in range(5):
            if self._get_cer_ftp_sat(cer_sat, self.PATHS['CER']):
                return True
            else:
                time.sleep(1)
        return False

    def _get_cer_ftp_sat(self, cer, path_cer):
        ftp = ftplib.FTP(self.g.SAT['ftp'], timeout=5)
        folder = self._join(
            self.g.SAT['folder'],
            cer[0:6],
            cer[6:12],
            cer[12:14],
            cer[14:16],
            cer[16:18]
        )
        try:
            ftp.login('anonymous', '')
            ftp.cwd(folder)
            ftp.retrbinary(
                'RETR {}.cer'.format(cer), open(path_cer, 'wb').write)
            return True
        except ftplib.all_errors as e:
            if str(e) == 'timed out':
                self.error = 'Se agoto el tiempo de espera. asegurate de ' \
                    'tener conexión a Internet activa'
            else:
                code = str(e).split(None, 1)
                if isinstance(code, list):
                    code = int(code[0])
                if code == 550:
                    self.error = 'Servidor FTP del SAT fuera de línea'
                else:
                    self.error = str(code)
            self.g.LOG.error(self.error)
            return False
        finally:
            ftp.close()
        return False

    def _cadena_hex(self, cadena):
        return hashlib.sha1(cadena.encode('utf-8')).hexdigest()

    def _make_files(self, sat=False):
        xslt_sello = self.g.PATHS['XSLT_SELLO']
        xslt_cadena = self.g.PATHS['XSLT_CADENA']
        msg1 = 'No fue posible obtener la llave del certificado del CFDI'
        msg2 = 'No fue posible obtener el sello del CFDI'
        if sat:
            msg1 = 'No fue posible obtener la llave del certificado del SAT'
            msg2 = 'No fue posible obtener el sello del SAT'
            xslt_sello = self.g.PATHS['XSLT_SELLO_SAT']
            xslt_cadena = self.g.PATHS['XSLT_TIMBRE']
            if not self._get_cer_sat():
                return False
            # Generamos la llave publica del certificado SAT
            args = '"{}" x509 -inform DER -in "{}" -pubkey > "{}"'.format(
                self.g.PATHS['OPENSSL'],
                self.PATHS['CER'],
                self.PATHS['KEY'],
            )
        else:
            # Generamos la llave publica del certificado CFDI
            args = '"{}" "{}" "{}" | "{}" x509 -inform PEM -pubkey > ' \
                '"{}"'.format(
                    self.g.PATHS['XSLTPROC'],
                    self.g.PATHS['XSLT_CER'],
                    self.path_xml,
                    self.g.PATHS['OPENSSL'],
                    self.PATHS['KEY'],
                )
        try:
            subprocess.check_output(args, shell=True, stderr=DEVNULL).decode()
        except subprocess.CalledProcessError as e:
            self.g.LOG.error(e)
            self.error = msg1
            return False

        # Generamos el sello
        args = '"{}" "{}" "{}" | "{}" enc -base64 -d -A -out "{}"'.format(
            self.g.PATHS['XSLTPROC'],
            xslt_sello,
            self.path_xml,
            self.g.PATHS['OPENSSL'],
            self.PATHS['SELLO'],
        )
        try:
            res = subprocess.check_output(
                args, shell=True, stderr=DEVNULL).decode()
        except subprocess.CalledProcessError as e:
            self.g.LOG.error(e)
            self.error = msg2
            return False
        if not self._get_file_size(self.PATHS['SELLO']):
            self.g.LOG.error(msg2)
            self.error = msg2
            return False

        # Generamos la cadena original del CFDI
        args = '"{}" "{}" "{}" > "{}"'.format(
            self.g.PATHS['XSLTPROC'],
            xslt_cadena,
            self.path_xml,
            self.PATHS['CADENA'],
        )
        try:
            res = subprocess.check_output(
                args, shell=True, stderr=DEVNULL).decode()
        except subprocess.CalledProcessError as e:
            self.g.LOG.error(e)
            self.error = msg2
            return False
        if not self._get_file_size(self.PATHS['CADENA']):
            self.g.LOG.error(msg2)
            self.error = msg2
            return False
        return True

    def _valid_sello(self, sat=True):
        args = '"{}" dgst -sha1 -verify "{}" -signature "{}" "{}"'.format(
            self.g.PATHS['OPENSSL'],
            self.PATHS['KEY'],
            self.PATHS['SELLO'],
            self.PATHS['CADENA'],
        )
        try:
            valid = subprocess.check_output(
                args, shell=True, stderr=DEVNULL).decode()
        except subprocess.CalledProcessError as e:
            self.g.LOG.error(e)
            self.error = 'Documento inválido'
            return False
        msg = 'del CFDI'
        if sat:
            msg = 'del SAT'
        if valid.strip() != 'Verified OK':
            self.error = 'Documento inválido, sello {} inválido'.format(msg)
            self.g.LOG.error(self.error)
            return False
        return True

    def _delete(self):
        self._file_kill(self.PATHS['KEY'])
        self._file_kill(self.PATHS['SELLO'])
        self._file_kill(self.PATHS['CADENA'])
        return


    def verify_cfdi(self):
        if not self._make_files():
            return False
        if not self._valid_sello():
            return False
        #~ Obtenemos los archivos necesarios para validar el sello del SAT
        if not self._make_files(True):
            return False
        #~ Validamos el sello del SAT
        if not self._valid_sello(True):
            return False
        self._delete()
        self.msg = 'Documento válido'
        return True


class Util(object):
    WIN = 'win32'
    MAC = 'darwin'

    def __init__(self):
        self.OS = sys.platform

    def get_folder(self, parent):
        return askdirectory(parent=parent)

    def get_file(self, parent, ext='', title='Factura Libre'):
        filetypes = [(ext, ext)]
        return askopenfilename(
            parent=parent,
            title=title,
            defaultextension=ext,
            filetypes=filetypes)

    def dir_current(self):
        return os.getcwd()

    def get_path_info(self, path, index=-1):
        path, filename = os.path.split(path)
        name, extension = os.path.splitext(filename)
        data = (path, filename, name, extension)
        if index == -1:
            return data
        else:
            return data[index]

    def path_join(self, *paths):
        return os.path.join(*paths)

    def path_config(self, path):
        target = path
        if sys.platform == self.WIN:
            target = path.replace('/', '\\')
        return target

    def get_files(self, path, ext='*.xml'):
        xmls = []
        for folder, _, files in os.walk(path):
            pattern = re.compile('\.xml', re.IGNORECASE)
            xmls += [os.path.join(folder,f) for f in files if pattern.search(f)]
        return tuple(xmls)

    def join(self, *paths):
        return os.path.join(*paths)

    def exists(self, path):
        return os.path.exists(path)

    def makedirs(self, path):
        if not self.exists(path):
            os.makedirs(path)
        return

    def move(self, src, dest):
        try:
            shutil.move(src, dest)
            return True
        except:
            return False

    def copy(self, src, dest):
        try:
            shutil.copy(src, dest)
            return True
        except:
            return False

    def validate_dir(self, path, access='e'):
        if access == 'e':
            return self.exists(path)
        if access == 'r':
            return os.access(path, os.R_OK)
        if access == 'w':
            return os.access(path, os.W_OK)

    def msgbox(self, msg, icon=1):
        title = 'Factura Libre'
        if icon == 1:
            messagebox.showerror(title, msg)
        elif icon == 2:
            messagebox.showinfo(title, msg)
        else:
            messagebox.showwarning(title, msg)
        return

    def question(self, msg):
        return messagebox.askyesno('Factura Libre', msg)

    def sleep(self, sec=1):
        time.sleep(sec)
        return

    def load_config(self, path):
        data = {}
        try:
            with open(path, 'r') as f:
                data = json.loads(f.read())
        except:
            pass
        return data

    def save_config(self, path, key, value):
        data = self.load_config(path)
        data[key] = value
        try:
            with open(path, 'w') as f:
                data = json.dumps(data, indent=4)
                f.write(data)
        except:
            pass
        return

    def now(self):
        return datetime.now()

    def get_dates(self, year, month):
        days = calendar.monthrange(year, month)[1]
        d1 = '01/{:02d}/{}'.format(month, year)
        d2 = '{}/{:02d}/{}'.format(days, month, year)
        return d1, d2

    def get_days(self, year, month):
        if isinstance(year, str):
            year = int(year)
        if isinstance(month, str):
            month = int(month)
        return calendar.monthrange(year, month)[1]

    def combo_values(self, combo, values, select_pos=-1):
        if isinstance(values, tuple):
            combo['values'] = values
        else:
            combo['values'] = tuple(values)
        if select_pos == -1:
            combo.current(len(combo['values']) - 1)
        elif select_pos > -1:
            combo.current(select_pos)
        return

    def listbox_insert(self, listbox, value, pos=tk.END):
        listbox.insert(pos, value)
        return

    def listbox_delete(self, listbox, pos=-1):
        if pos == -2:
            listbox.delete(0, tk.END)
        elif pos == -1:
            listbox.delete(listbox.curselection()[0])
        else:
            listbox.delete(pos)
        return

    def listbox_selection(self, listbox):
        selection = listbox.curselection()
        if selection:
            selection = listbox.get(tk.ACTIVE)
        return selection

    def get_info_xml(self, path, PRE):
        data = {}
        try:
            xml = ET.parse(path).getroot()
        except Exception as e:
            #~ self.debug(path)
            #~ self.debug(e)
            return {}

        ver = xml.attrib['version']
        node = xml.find('{}Emisor'.format(PRE[ver]))
        if node is None:
            log = 'El documento no tiene el nodo requerido Emisor: {}'
            #~ self.debug(log.format(path))
            return {}
        data['emisor_rfc'] = node.attrib['rfc']

        node = xml.find('{}Receptor'.format(PRE[ver]))
        if node is None:
            log = 'El documento no tiene el nodo requerido Receptor: {}'
            #~ self.debug(log.format(path))
            return {}
        data['receptor_rfc'] = node.attrib['rfc']

        node = xml.find('{}Complemento/{}TimbreFiscalDigital'.format(
            PRE[ver], PRE['TIMBRE']))
        if node is None:
            log = 'El documento no esta timbrado: {}'
            #~ self.debug(log.format(path))
            return {}
        data['uuid'] = node.attrib['UUID']
        data['year'] = node.attrib['FechaTimbrado'][0:4]
        data['month'] = node.attrib['FechaTimbrado'][5:7]
        return data

    def get_name(self, path, PRE, format1='', format2=''):
        xml = ET.parse(path).getroot()
        data = xml.attrib.copy()
        del data['sello']
        del data['certificado']
        pre = PRE[data['version']]
        if not 'serie' in data:
            data['serie'] = ''
        data['fecha'] = data['fecha'].partition('T')[0]
        if 'folio' in data:
            data['folio'] = int(data['folio'])
        else:
            data['folio'] = 0
        node = xml.find('{}Emisor'.format(pre))
        data['emisor_rfc'] = node.attrib['rfc']
        data['emisor_nombre'] = ''
        if 'nombre' in node.attrib:
            data['emisor_nombre'] = node.attrib['nombre'].replace('/', '_')
        node = xml.find('{}Receptor'.format(pre))
        data['receptor_rfc'] = node.attrib['rfc']
        data['receptor_nombre'] = ''
        if 'nombre' in node.attrib:
            data['receptor_nombre'] = node.attrib['nombre'].replace('/', '_')
        node = xml.find('{}Complemento/{}TimbreFiscalDigital'.format(
            pre, PRE['TIMBRE']))
        data['uuid'] = node.attrib['UUID']
        if format1:
            try:
                name = format1.format(**data)
                name = name.replace("'", "").replace(" ", "_").replace(
                    ",", "").replace(".", "")
                return os.path.normpath(name)
            except:
                return os.path.normpath(format2.format(**data))
        else:
            return os.path.normpath(format2.format(**data))

    def parse(self, path):
        try:
            xml = ET.parse(path).getroot()
            return xml
        except:
            return None

    def get_qr(self, data):
        scale = 10
        path = self.get_path_temp('cbb.png')
        code = pyqrcode.QRCode(data, mode='binary')
        code.png(path, scale)
        return path

    def get_path_temp(self, name=''):
        if name:
            return self.join(tempfile.gettempdir(), name)
        if sys.platform == self.WIN:
            return tempfile.TemporaryFile(mode='w').name
        return tempfile.mkstemp()[1]

    def get_info_report(self, path, options, g):
        PRE = g.PREFIX
        data = {}
        try:
            xml = ET.parse(path).getroot()
        except Exception as e:
            g.LOG.error(path)
            g.LOG.error(e)
            return False
        ver = xml.attrib['version']
        data = xml.attrib.copy()
        del data['sello']
        del data['certificado']

        node = xml.find('{}Emisor'.format(PRE[ver]))
        if node is None:
            log = 'El documento no tiene el nodo requerido Emisor: {}'
            g.LOG.error(log.format(path))
            return False
        data['emisor_rfc'] = node.attrib['rfc']
        data['emisor_nombre'] = ''
        if 'nombre' in node.attrib:
            data['emisor_nombre'] = node.attrib['nombre']

        node = xml.find('{}Receptor'.format(PRE[ver]))
        if node is None:
            log = 'El documento no tiene el nodo requerido Receptor: {}'
            g.LOG.error(log.format(path))
            return False
        data['receptor_rfc'] = node.attrib['rfc']
        data['receptor_nombre'] = ''
        if 'nombre' in node.attrib:
            data['receptor_nombre'] = node.attrib['nombre']

        node = xml.find('{}Impuestos'.format(PRE[ver]))
        if node is not None:
            data.update(node.attrib)
            imp = node.find('{}Traslados'.format(PRE[ver]))
            if imp is not None:
                for n in list(imp):
                    key = 'traslado_{}_{}'.format(
                        n.attrib['impuesto'].lower(),
                        int(float(n.attrib['tasa'])))
                    data[key] = float(n.attrib['importe'])
            imp = node.find('{}Retenciones'.format(PRE[ver]))
            if imp is not None:
                for n in list(imp):
                    key = 'retencion_{}'.format(n.attrib['impuesto'].lower())
                    data[key] = float(n.attrib['importe'])
        node = xml.find('{}Complemento/{}TimbreFiscalDigital'.format(
            PRE[ver], PRE['TIMBRE']))
        if node is None:
            log = 'El documento no esta timbrado: {}'
            g.LOG.error(log.format(path))
            return False
        data['UUID'] = node.attrib['UUID'].upper()
        data['FechaTimbrado'] = node.attrib['FechaTimbrado'].replace('T', ' ')
        data['fecha'] = data['fecha'].replace('T', ' ')

        fields_details = (
            'noIdentificacion',
            'descripcion',
            'unidad',
            'cantidad',
            'valorUnitario',
            'importe'
        )
        details = []
        if any(d in options['fields_report'] for d in fields_details):
            node = xml.find('{}Conceptos'.format(PRE[ver]))
            for n in node.getchildren():
                details.append(n.attrib.copy())
        atr = (
            'serie',
            'folio',
            'Moneda',
            'TipoCambio',
            'validacion',
            'validacion_sat',
            'totalImpuestosRetenidos',
            'totalImpuestosTrasladados',
            'descuento',
            'traslado_iva_0',
            'traslado_iva_16',
            'retencion_iva',
            'retencion_isr',
        ) + fields_details
        for a in atr:
            if not a in data:
                data[a] = ''
        tmpl = Template(options['fields_report'].replace('{', '${'))
        if details:
            info = []
            for d in details:
                new_data = data.copy()
                new_data.update(d)
                info.append(tmpl.safe_substitute(**new_data).split('|'))
            return tuple(info)

        info = tmpl.safe_substitute(**data).split('|')
        if options['validate_fac']:
            cfdi = ValidCFDI(path, g)
            if cfdi.verify_cfdi():
                info.append(cfdi.msg)
            else:
                info.append(cfdi.error)
        if options['validate_sat']:
            data_sat = {
                'emisor_rfc': data['emisor_rfc'],
                'receptor_rfc': data['receptor_rfc'],
                'total': data['total'],
                'uuid': data['UUID']
            }
            sat = SAT()
            if sat.get_estatus(data_sat):
                info.append(sat.msg)
            else:
                info.append(sat.error)
        return tuple((info,))

    def save_csv(self, data, path=''):
        if not path:
            path = self.get_path_temp('reporte.csv')
        with open(path, 'w', newline='\n') as csvfile:
            datawriter = csv.writer(csvfile, delimiter='|',
                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for l in data:
                datawriter.writerow(l)
        if self.OS == self.WIN:
            os.startfile(path)
        elif self.OS == self.MAC:
            subprocess.call(['open', path])
        else:
            subprocess.call(['xdg-open', path])
        return


class Mail(object):
    PREFIX = {
        '3.0': '{http://www.sat.gob.mx/cfd/3}',
        '3.2': '{http://www.sat.gob.mx/cfd/3}',
        'TIMBRE': '{http://www.sat.gob.mx/TimbreFiscalDigital}',
    }

    def __init__(self, data):
        self.error = ''
        self.target = data['mail_target']
        self.con = self._connection(data)
        self.type_xml = ('text/xml', 'application/xml')
        self.type_pdf = ('application/pdf',)
        self.type_other = (
            'application/octet-stream', 'application/x-zip-compressed')
        self.types = self.type_xml + self.type_pdf + self.type_other
        self.ext = ('.xml', '.pdf', '.zip')

    def _connection(self, data):
        try:
            if data['mail_ssl']:
                M = imaplib.IMAP4_SSL(data['mail_server'], data['mail_port'])
            else:
                M = imaplib.IMAP4(data['mail_server'], data['mail_port'])
            M.login(data['mail_user'], data['mail_password'])
            M.select()
            return M
        except imaplib.IMAP4.error as e:
            self.error = str(e)
            return None
        except Exception as e:
            self.error = str(e)
            return None

    def _join(self, *paths):
        return os.path.join(*paths)

    def __del__(self):
        try:
            self.con.close()
            self.con.logout()
        except:
            pass

    def down_all_mails(self, pb, info, options):
        i = 0
        folders = self._get_folders(options['mail_subfolder'])
        mails = self._get_mails(folders)
        total = len(mails)
        pb['maximum'] = total
        pb.start()
        for f in folders:
            mails = self._get_mails((f,))
            for m in mails:
                i += 1
                pb['value'] = i
                pb.update_idletasks()
                msg = 'Correo {} de {}'.format(i, total)
                info.set(msg)
                message = self._get_mail(m)
                if not message:
                    continue
                files = self._get_files(message)
                if files:
                    self._save_files(files, options['mail_name'])
                    if options['mail_delete2']:
                        self.con.uid('STORE', m, '+FLAGS', '\\Deleted')
                else:
                    if options['mail_delete1']:
                        self.con.uid('STORE', m, '+FLAGS', '\\Deleted')
        self.con.expunge()
        return

    def _get_mails(self, folders):
        mails = []
        for f in folders:
            self.con.select(f)
            typ, data = self.con.uid('search', None, 'ALL')
            mails.extend(data[0].split())
        return mails

    def _get_folders(self, subfolders):
        folders = ['INBOX']
        if subfolders:
            typ, subdir = self.con.list()
            for s in subdir:
                name = s.decode('utf8').rpartition('"."')[-1].strip()
                if name in ('INBOX', 'INBOX.Trash', 'INBOX.Drafts',
                    'INBOX.Junk', 'INBOX.Sent'):
                    continue
                folders.append(name)
        return folders

    def _get_mail(self, uid):
        result, data = self.con.uid('fetch', uid, '(RFC822)')
        if not data[0]:
            return
        raw_email = data[0][1].decode('utf8', 'ignore')
        email_message = email.message_from_string(raw_email)
        return email_message

    def _get_files(self, message):
        sha_tmp = []
        files = {}
        for part in message.walk():
            #~ print ('part CMT', part.get_content_maintype())
            if part.get_content_maintype() == 'multipart':
                continue
            #~ print ('part CMT', part.get_content_maintype())
            #~ if part.get('Content-Disposition') is None:
                #~ continue
            file_name = part.get_filename()
            if not file_name:
                continue
            #~ print (file_name)
            content_type = part.get_content_type()
            if content_type in self.types:
                #~ print ('get', file_name, content_type)
                content = part.get_payload(decode=True)
                sha = hashlib.sha1(content).hexdigest()
                if sha in sha_tmp:
                    continue
                sha_tmp.append(sha)
                #~ files.append((file_name, content))
                name = file_name[:-4].replace(' ', '_').upper()
                ext = file_name[-4:].lower()

                # ToDo and delete
                if ext == '.zip':
                    continue

                if not ext in self.ext:
                    continue
                if not name in files:
                    files[name] = {'xml': '', 'pdf': ''}
                #~ print ('ext', ext)
                if content_type in self.type_xml:
                    files[name]['xml'] = content
                elif content_type in self.type_pdf:
                    files[name]['pdf'] = content
                elif content_type in self.type_other:
                    if ext == '.xml':
                        files[name]['xml'] = content
                    elif ext == '.pdf':
                        files[name]['pdf'] = content
                    elif ext == '.zip':
                        # ToDo ZIP
                        pass
        return files

    def _save_files(self, files, original):
        for k, v in files.items():
            if not v['xml'] and not v['pdf']:
                continue
            #~ print ('save', k)
            file_name = k
            if v['xml'] and v['pdf'] and not original:
                #~ xml = v['xml'].decode('utf8')
                tree = ET.fromstring(v['xml'])
                ver = tree.attrib['version']
                if float(ver) >= 3.0:
                    timbre = '{}Complemento/{}TimbreFiscalDigital'.format(
                        self.PREFIX[ver], self.PREFIX['TIMBRE'])
                    node = tree.find(timbre)
                    if node is not None:
                        file_name = node.attrib['UUID'].upper()
            name_xml = '{}_ORIGINAL.xml'
            name_pdf = '{}_ORIGINAL.pdf'
            if original:
                name_xml = '{}.xml'
                name_pdf = '{}.pdf'
            if v['xml'] and not v['pdf']:
                path = self._join(self.target, name_xml.format(file_name))
                with open(path, 'wb') as fd:
                    fd.write(v['xml'])
            elif not v['xml'] and v['pdf']:
                path = self._join(self.target, name_pdf.format(file_name))
                with open(path, 'wb') as fd:
                    fd.write(v['pdf'])
            else:
                path = self._join(self.target, '{}.xml'.format(file_name))
                with open(path, 'wb') as fd:
                    fd.write(v['xml'])
                path = self._join(self.target, name_pdf.format(file_name))
                with open(path, 'wb') as fd:
                    fd.write(v['pdf'])
        return


class LibO(object):
    WIN = 'win32'
    WIN_SM = 'com.sun.star.ServiceManager'
    OS = sys.platform
    SM = None

    def __init__(self):
        self._aoo = None
        self._run()
        self._init_var()

    def __del__(self):
        try:
            self.desktop.terminate()
        except Exception as e:
            print (e)
        if self._aoo:
            self._aoo.kill()
        if self.OS != self.WIN:
            ps = subprocess.Popen(['ps', '-e'], stdout=subprocess.PIPE)
            grep = subprocess.Popen(['grep', 'soffice'],
                stdin=ps.stdout, stdout=subprocess.PIPE)
            p = grep.communicate()[0]
            if p:
                pid = p.split()[0].strip()
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except Exception as e:
                    print (e)

    def _init_var(self):
        try:
            self.desktop = self._create_instance('com.sun.star.frame.Desktop')
            if self.OS == self.WIN:
                self.SM._FlagAsMethod("Bridge_GetStruct")
            self.fcp = self._create_instance(
                'com.sun.star.ucb.FileContentProvider')
        except:
            pass

    def _run(self):
        if self.OS == self.WIN:
            self.SM = Dispatch(self.WIN_SM)
        else:
            ps = subprocess.Popen(['ps', '-e'], stdout=subprocess.PIPE)
            grep = subprocess.Popen(
                ['grep', 'soffice'],
                stdin=ps.stdout,
                stdout=subprocess.PIPE)
            if not grep.communicate()[0]:
                args = '--accept=socket,host=localhost,port=8100;urp;'
                args += 'StarOffice.ComponentContext'
                self._aoo = subprocess.Popen(['soffice', '--headless', args])
                time.sleep(3)
            lc = uno.getComponentContext()
            local_resolver = lc.ServiceManager.createInstanceWithContext(
                'com.sun.star.bridge.UnoUrlResolver', lc )
            try:
                args = 'uno:socket,host=localhost,port=8100;urp;'
                args += 'StarOffice.ComponentContext'
                context = local_resolver.resolve(args)
                self.SM = context.ServiceManager
            except Exception as e:
                pass

    def _create_instance(self, name):
        return self.SM.createInstance(name)

    #~ def get_propertyvalue(self):
        #~ return self.SM.Bridge_GetStruct('com.sun.star.beans.PropertyValue')

    def _make_property(self, args):
        if self.OS == self.WIN:
            pv = []
            for a in args:
                p = self.SM.Bridge_GetStruct('com.sun.star.beans.PropertyValue')
                p.Name = a[0]
                p.Value = a[1]
                pv.append(p)
        else:
            pv = [PropertyValue(a[0], 0, a[1], DIRECT_VALUE) for a in args]
        return tuple(pv)

    def path_to(self, path, url=True):
        new_path = path
        if url:
            if not path.startswith('file:///'):
                new_path = self.fcp.getFileURLFromSystemPath('', path)
        else:
            if path.startswith('file:///'):
                new_path = self.fcp.getSystemPathFromFileURL(path)
        return new_path

    def size(self, obj, width, height):
        if self.OS == self.WIN:
            tam = self.SM.Bridge_GetStruct('com.sun.star.awt.Size')
        else:
            tam = Size()
        tam.Width = width
        tam.Height = height
        obj.setSize(tam)
        return

    def doc_open(self, path, pv=None):
        path = self.path_to(path)
        if pv is None:
            pv = (
                ('Hidden', True),
                ('AsTemplate', True),
            )
            pv = self._make_property(pv)
        doc = None
        try:
            doc = self.desktop.loadComponentFromURL(path, '_default', 0, pv)
        except Exception as e:
            print (e)
        return doc


class NumerosLetras(object):

    def __init__(self):
        pass

    def to_letters(
        self, numero, moneda='peso', texto_inicial='', texto_final='',
        fraccion_letras=False, fraccion=''):
        enletras = texto_inicial
        numero = abs(numero)
        numtmp = '%015d' % numero

        if numero < 1:
            enletras += 'cero ' + self.plural(moneda) + ' '
        else:
            enletras += self.numlet(numero)
            if numero == 1 or numero < 2:
                enletras += moneda + ' '
            elif int(''.join(numtmp[3:])) == 0 or int(''.join(numtmp[9:])) == 0:
                enletras += 'de ' + self.plural(moneda) + ' '
            else:
                enletras += self.plural(moneda) + ' '

        decimal = '%0.2f' % numero
        decimal = decimal.split('.')[1]
        #~ decimal = int((numero-int(numero))*100)
        if fraccion_letras:
            if decimal == 0:
                enletras += 'con cero ' + self.plural(fraccion)
            elif decimal == 1:
                enletras += 'con un ' + fraccion
            else:
                enletras += 'con ' + self.numlet(int(decimal)) + self.plural(fraccion)
        else:
            enletras += decimal

        enletras += texto_final
        return enletras

    def numlet(self, numero):
        numtmp = '%015d' % numero
        co1=0
        letras = ''
        leyenda = ''
        for co1 in range(0,5):
            inicio = co1*3
            cen = int(numtmp[inicio:inicio+1][0])
            dec = int(numtmp[inicio+1:inicio+2][0])
            uni = int(numtmp[inicio+2:inicio+3][0])
            letra3 = self.centena(uni, dec, cen)
            letra2 = self.decena(uni, dec)
            letra1 = self.unidad(uni, dec)

            if co1 == 0:
                if (cen+dec+uni) == 1:
                    leyenda = 'billon '
                elif (cen+dec+uni) > 1:
                    leyenda = 'billones '
            elif co1 == 1:
                if (cen+dec+uni) >= 1 and int(''.join(numtmp[6:9])) == 0:
                    leyenda = "mil millones "
                elif (cen+dec+uni) >= 1:
                    leyenda = "mil "
            elif co1 == 2:
                if (cen+dec) == 0 and uni == 1:
                    leyenda = 'millon '
                elif cen > 0 or dec > 0 or uni > 1:
                    leyenda = 'millones '
            elif co1 == 3:
                if (cen+dec+uni) >= 1:
                    leyenda = 'mil '
            elif co1 == 4:
                if (cen+dec+uni) >= 1:
                    leyenda = ''

            letras += letra3 + letra2 + letra1 + leyenda
            letra1 = ''
            letra2 = ''
            letra3 = ''
            leyenda = ''
        return letras

    def centena(self, uni, dec, cen):
        letras = ''
        numeros = ["","","doscientos ","trescientos ","cuatrocientos ","quinientos ","seiscientos ","setecientos ","ochocientos ","novecientos "]
        if cen == 1:
            if (dec+uni) == 0:
                letras = 'cien '
            else:
                letras = 'ciento '
        elif cen >= 2 and cen <= 9:
            letras = numeros[cen]
        return letras

    def decena(self, uni, dec):
        letras = ''
        numeros = ["diez ","once ","doce ","trece ","catorce ","quince ","dieci","dieci","dieci","dieci"]
        decenas = ["","","","treinta ","cuarenta ","cincuenta ","sesenta ","setenta ","ochenta ","noventa "]
        if dec == 1:
            letras = numeros[uni]
        elif dec == 2:
            if uni == 0:
                letras = 'veinte '
            elif uni > 0:
                letras = 'veinti'
        elif dec >= 3 and dec <= 9:
            letras = decenas[dec]
        if uni > 0 and dec > 2:
            letras = letras+'y '
        return letras

    def unidad(self, uni, dec):
        letras = ''
        numeros = ["","un ","dos ","tres ","cuatro ","cinco ","seis ","siete ","ocho ","nueve "]
        if dec != 1:
            if uni > 0 and uni <= 5:
                letras = numeros[uni]
        if uni >= 6 and uni <= 9:
            letras = numeros[uni]
        return letras

    def plural(self, palabra):
        if re.search('[aeiou]$', palabra):
            return re.sub('$', 's', palabra)
        else:
            return palabra + 'es'


class CFDIPDF(object):
    WIN = 'win32'
    WIN_SM = 'com.sun.star.ServiceManager'
    OS = sys.platform
    TIPO_REGIMEN = {
        '2': 'Sueldos y salarios',
        '3': 'Jubilados',
        '4': 'Pensionados',
        '5': 'Asimilados a salarios, Miembros de las Sociedades '
            'Cooperativas de Producción',
        '6': 'Asimilados a salarios, Integrantes de Sociedades y '
            'Asociaciones Civiles',
        '7': 'Asimilados a salarios, Miembros de consejos directivos, '
            'de vigilancia, consultivos, honorarios a administradores, '
            'comisarios y gerentes generales',
        '8': 'Asimilados a salarios, Actividad empresarial (comisionistas)',
        '9': 'Asimilados a salarios, Honorarios asimilados a salarios',
        '10': 'Asimilados a salarios, Ingresos acciones o títulos valor',
    }
    RIESGO_PUESTO = {
        '1': 'Clase I',
        '2': 'Clase II',
        '3': 'Clase III',
        '4': 'Clase IV',
        '5': 'Clase V'
    }

    def __init__(self, xml, path_pdf, template, g, util, path_to, size):
        self.xml = xml
        self.path_pdf = path_pdf
        self.template = template
        self.g = g
        self.util = util
        self.path_to = path_to
        self.size= size
        self.nomina = False
        self._config()

    def _config(self):
        pre = self.g.PREFIX[self.xml.attrib['version']]
        donat = self.g.PREFIX['DONATARIA']
        local = self.g.PREFIX['IMP_LOCAL']
        iedu = self.g.PREFIX['IEDU']
        timbre = self.g.PREFIX['TIMBRE']
        nomina = self.g.PREFIX['NOMINA']
        self.tree = {
            'emisor': '{}Emisor'.format(pre),
            'domicilio_fiscal': '{}DomicilioFiscal'.format(pre),
            'expedido_en': '{}ExpedidoEn'.format(pre),
            'regimen_fiscal': '{}RegimenFiscal'.format(pre),
            'receptor': '{}Receptor'.format(pre),
            'domicilio': '{}Domicilio'.format(pre),
            'donataria': '{}Complemento/{}Donatarias'.format(pre, donat),
            'impuestos': '{}Impuestos'.format(pre),
            'traslados': '{}Traslados'.format(pre),
            'retenciones': '{}Retenciones'.format(pre),
            'locales': '{}Complemento/{}ImpuestosLocales'.format(pre, local),
            'conceptos': '{}Conceptos'.format(pre),
            'aduana': '{}InformacionAduanera'.format(pre),
            'predial': '{}CuentaPredial'.format(pre),
            'iedu': '{}ComplementoConcepto/{}instEducativas'.format(pre, iedu),
            'timbre': '{}Complemento/{}TimbreFiscalDigital'.format(pre, timbre),
            'nomina': '{}Complemento/{}Nomina'.format(pre, nomina),
            'percepciones': '{}Percepciones'.format(nomina),
            'deducciones': '{}Deducciones'.format(nomina),
        }
        self.hoja = self.template.getSheets().getByIndex(0)
        self.search = self.hoja.getPrintAreas()
        if self.search:
            self.search = self.search[0]
        else:
            self.search = self.hoja.getRangeAddress()
        self.search = self.hoja.getCellRangeByPosition(
            self.search.StartColumn,
            self.search.StartRow,
            self.search.EndColumn,
            self.search.EndRow
        )
        self.sd = self.hoja.createSearchDescriptor()
        self.sd.SearchCaseSensitive = False
        self.sd.SearchRegularExpression = False
        nomina = self.xml.find(self.tree['nomina'])
        if nomina is not None:
            self.nomina = True
        return

    def make(self, sm):
        self._comprobante()
        self._emisor()
        self._receptor()
        self._donataria()
        if self.nomina:
            self._conceptos_nomina()
            self._nomina()
        else:
            self._totales()
            self._conceptos()
        #~ self._not_in_xml()
        self._timbre()
        self._cancelado()
        self._clean()
        self._save_pdf(sm)
        return True

    def _cancelado(self, cancel=False):
        if not cancel:
            pd = self.hoja.getDrawPage()
            if pd.getCount():
                pd.remove(pd.getByIndex(0))
        return

    def _timbre(self):
        timbre = self.xml.find(self.tree['timbre'])
        for k, v in timbre.attrib.items():
            self._set_cell('{timbre.%s}' % k, v)
        total_s = '%017.06f' % float(self.xml.attrib['total'])
        qr_data = '?re=%s&rr=%s&tt=%s&id=%s' % (
            self.rfc_emisor, self.rfc_receptor, total_s, timbre.attrib['UUID'])
        ruta_cbb = self.util.get_qr(qr_data)
        pd = self.hoja.getDrawPage()
        self.sd.setSearchString('{timbre.cbb}')
        ranges = self.search.findAll(self.sd)
        if ranges:
            ranges = ranges.getRangeAddressesAsString().split(';')
            for r in ranges:
                for c in r.split(','):
                    cell = self.hoja.getCellRangeByName(c)
                    image = self.template.createInstance(
                        'com.sun.star.drawing.GraphicObjectShape')
                    image.GraphicURL = self.path_to(ruta_cbb)
                    pd.add(image)
                    self.size(image, 3500, 3500)
                    image.Anchor = cell
                    pos = image.getPosition()
                    if pos.Y > self.g.LIMIT_MARGIN:
                        self.hoja.getRows().getByIndex(
                            cell.getCellAddress(
                                ).Row - 2).IsStartOfNewPage = True
                    break
        cadena = self.g.CADENA.format(**timbre.attrib)
        self._set_cell('{timbre.cadenaoriginal}', cadena)
        return

    def _nomina(self):
        nomina = self.xml.find(self.tree['nomina'])
        for k, v in nomina.attrib.items():
            if k == 'Banco':
                nv = '(%s) %s' % (v, '')
                self._set_cell('{nomina.%s}' % k, nv)
            elif k == 'TipoRegimen':
                nv = '(%s) %s' % (v, self.TIPO_REGIMEN[v])
                self._set_cell('{nomina.%s}' % k, nv)
            elif k == 'RiesgoPuesto':
                nv = '(%s) %s' % (v, self.RIESGO_PUESTO[v])
                self._set_cell('{nomina.%s}' % k, nv)
            else:
                self._set_cell('{nomina.%s}' % k, v)
        percepciones = nomina.find(self.tree['percepciones'])
        total = 0
        if percepciones is not None:
            for k, v in percepciones.attrib.items():
                total += float(v)
                #~ v = '$ %s' % self.format_s.format(float(v))
                self._set_cell('{percepciones.%s}' % k, float(v), value=True)
        #~ v = '$ %s' % self.format_s.format(total)
        self._set_cell('{total.percepciones}', total, value=True)
        if percepciones is not None:
            first = True
            for percepcion in percepciones.getchildren():
                #~ ig = '$ %s' % self.format_s.format(
                    #~ float(percepcion.attrib['ImporteGravado']))
                #~ ie = '$ %s' % self.format_s.format(
                    #~ float(percepcion.attrib['ImporteExento']))
                ig = float(percepcion.attrib['ImporteGravado'])
                ie = float(percepcion.attrib['ImporteExento'])
                tp = percepcion.attrib['TipoPercepcion']
                concepto = percepcion.attrib['Concepto']
                if first:
                    first = False
                    cell_1 = self._set_cell('{percepcion.TipoPercepcion}', tp)
                    cell_2 = self._set_cell('{percepcion.Concepto}', concepto)
                    cell_3 = self._set_cell('{percepcion.ImporteGravado}', ig, value=True)
                    cell_4 = self._set_cell('{percepcion.ImporteExento}', ie, value=True)
                else:
                    cell_1 = self._set_cell(v=tp, cell=cell_1)
                    cell_2 = self._set_cell(v=concepto, cell=cell_2)
                    cell_3 = self._set_cell(v=ig, cell=cell_3, value=True)
                    cell_4 = self._set_cell(v=ie, cell=cell_4, value=True)
        deducciones = nomina.find(self.tree['deducciones'])
        if deducciones is None:
            return
        total = 0
        for k, v in deducciones.attrib.items():
            total += float(v)
            #~ v = '$ %s' % self.format_s.format(float(v))
            self._set_cell('{deducciones.%s}' % k, float(v), value=True)
        #~ v = '$ %s' % self.format_s.format(total)
        self._set_cell('{total.deducciones}', total, value=True)
        first = True
        for deduccion in deducciones.getchildren():
            #~ ig = '$ %s' % self.format_s.format(
                #~ float(deduccion.attrib['ImporteGravado']))
            #~ ie = '$ %s' % self.format_s.format(
                #~ float(deduccion.attrib['ImporteExento']))
            ig = float(deduccion.attrib['ImporteGravado'])
            ie = float(deduccion.attrib['ImporteExento'])
            td = deduccion.attrib['TipoDeduccion']
            concepto = deduccion.attrib['Concepto']
            if first:
                first = False
                cell_1 = self._set_cell('{deduccion.TipoDeduccion}', td)
                cell_2 = self._set_cell('{deduccion.Concepto}', concepto)
                cell_3 = self._set_cell('{deduccion.ImporteGravado}', ig, value=True)
                cell_4 = self._set_cell('{deduccion.ImporteExento}', ie, value=True)
            else:
                cell_1 = self._set_cell(v=td, cell=cell_1)
                cell_2 = self._set_cell(v=concepto, cell=cell_2)
                cell_3 = self._set_cell(v=ig, cell=cell_3, value=True)
                cell_4 = self._set_cell(v=ie, cell=cell_4, value=True)
        return

    def _conceptos_nomina(self):
        conceptos = self.xml.find(self.tree['conceptos'])
        for concepto in conceptos.getchildren():
            for k, v in concepto.attrib.items():
                self._set_cell('{concepto.%s}' % k, v)
        pass

    def _conceptos(self):
        conceptos = self.xml.find(self.tree['conceptos'])
        if conceptos is None:
            return
        first = True
        for c in conceptos.getchildren():
            key = c.attrib.get('noIdentificacion', '')
            description = self._get_description(c)
            unidad = c.attrib['unidad']
            cantidad = c.attrib['cantidad']
            precio = c.attrib['valorUnitario']
            importe = c.attrib['importe']
            if first:
                first = False
                cell_1 = self._set_cell('{noIdentificacion}', key)
                cell_2 = self._set_cell('{descripcion}', description)
                cell_3 = self._set_cell('{unidad}', unidad)
                cell_4 = self._set_cell('{cantidad}', cantidad, value=True)
                cell_5 = self._set_cell('{valorUnitario}', precio, value=True)
                cell_6 = self._set_cell('{importe}', importe, value=True)
            else:
                row = cell_2.getCellAddress().Row + 1
                self.hoja.getRows().insertByIndex(row, 1)
                if cell_1:
                    self._copy_cell(cell_1)
                    cell_1 = self._set_cell(v=key, cell=cell_1)
                if cell_3:
                    self._copy_cell(cell_3)
                    cell_3 = self._set_cell(v=unidad, cell=cell_3)
                self._copy_cell(cell_2)
                self._copy_cell(cell_4)
                self._copy_cell(cell_5)
                self._copy_cell(cell_6)
                cell_2 = self._set_cell(v=description, cell=cell_2)
                cell_4 = self._set_cell(v=cantidad, cell=cell_4, value=True)
                cell_5 = self._set_cell(v=precio, cell=cell_5, value=True)
                cell_6 = self._set_cell(v=importe, cell=cell_6, value=True)
        return

    def _get_description(self, c):
        data = c.attrib['descripcion']
        n = c.find(self.tree['aduana'])
        if n is not None:
            data += '\nPedimento de Importación No. %s\n' % n.attrib['numero']
            data += 'Aduana: %s, Fecha del pedimento: %s' % (
                n.attrib['aduana'], n.attrib['fecha'])
        n = c.find(self.tree['predial'])
        if n is not None:
            data += '\n\nCuenta Predial Número: %s' % n.attrib['numero']
        iedu = c.find(self.tree['iedu'])
        if iedu is not None:
            data += '\n\nAlumno: %s\nCURP: %s' % (
                iedu.attrib['nombreAlumno'], iedu.attrib['CURP'])
            data += '\nAcuerdo de incorporación ante la SEP %s %s' % (
                iedu.attrib['nivelEducativo'], iedu.attrib['autRVOE'])
        return data

    def _totales(self):
        cell_title = self._set_cell('{subtotal.titulo}', 'Subtotal')
        value = self.xml.attrib['subTotal']
        cell_value = self._set_cell('{subtotal}', value, value=True)
        if 'descuento' in self.xml.attrib:
            self._copy_cell(cell_title)
            self._copy_cell(cell_value)
            cell_title = self._set_cell(v='Descuento', cell=cell_title)
            value = self.xml.attrib['descuento']
            cell_value = self._set_cell(v=value, cell=cell_value, value=True)
        imp = self.xml.find(self.tree['impuestos'])
        if imp is not None:
            for k, v in imp.attrib.items():
                v = float(v)
                self._set_cell('{impuestos.%s}' % k, v, value=True)
            node = imp.find(self.tree['traslados'])
            if node is not None:
                for t in node.getchildren():
                    self._copy_cell(cell_title)
                    self._copy_cell(cell_value)
                    title = '%s %s%%' % (t.attrib['impuesto'], t.attrib['tasa'])
                    value = t.attrib['importe']
                    cell_title = self._set_cell(v=title, cell=cell_title)
                    cell_value = self._set_cell(
                        v=value, cell=cell_value, value=True)
            node = imp.find(self.tree['retenciones'])
            if node is not None:
                for t in node.getchildren():
                    self._copy_cell(cell_title)
                    self._copy_cell(cell_value)
                    title = 'Retención {}'.format(t.attrib['impuesto'])
                    value = t.attrib['importe']
                    cell_title = self._set_cell(v=title, cell=cell_title)
                    cell_value = self._set_cell(
                        v=value, cell=cell_value, value=True)

        otros = self.xml.find(self.tree['locales'])
        if otros is not None:
            for otro in list(otros):
                rl = '{}RetencionesLocales'.format(self.g.PREFIX['IMP_LOCAL'])
                if otro.tag == rl:
                    name = 'ImpLocRetenido'
                    tasa = 'TasadeRetencion'
                else:
                    name = 'ImpLocTrasladado'
                    tasa = 'TasadeTraslado'
                title = '%s %s %%' % (otro.attrib[name], otro.attrib[tasa])
                value = otro.attrib['Importe']
                self._copy_cell(cell_title)
                self._copy_cell(cell_value)
                cell_title = self._set_cell(v=title, cell=cell_title)
                cell_value = self._set_cell(
                    v=value, cell=cell_value, value=True)

        if 'total' in self.xml.attrib:
            self._copy_cell(cell_title)
            self._copy_cell(cell_value)
            cell_title = self._set_cell(v='Total', cell=cell_title)
            value = self.xml.attrib['total']
            cell_value = self._set_cell(v=value, cell=cell_value, value=True)
        return

    def _donataria(self):
        donataria = self.xml.find(self.tree['donataria'])
        if donataria is not None:
            for k, v in donataria.attrib.items():
                self._set_cell('{donataria.%s}' % k, v)
        return

    def _receptor(self):
        receptor = self.xml.find(self.tree['receptor'])
        self.rfc_receptor = receptor.attrib['rfc']
        for k, v in receptor.attrib.items():
            self._set_cell('{receptor.%s}' % k, v)
        domicilio = receptor.find(self.tree['domicilio'])
        if domicilio is not None:
            for k, v in domicilio.attrib.items():
                if k == 'codigoPostal':
                    v = 'C.P. %s' % v
                self._set_cell('{receptor.%s}' % k, v)
        return

    def _emisor(self):
        emisor = self.xml.find(self.tree['emisor'])
        self.rfc_emisor = emisor.attrib['rfc']
        for k, v in emisor.attrib.items():
            self._set_cell('{emisor.%s}' % k, v)
        domicilio = emisor.find(self.tree['domicilio_fiscal'])
        if domicilio is not None:
            for k, v in domicilio.attrib.items():
                if k == 'codigoPostal':
                    v = 'C.P. %s' % v
                self._set_cell('{emisor.%s}' % k, v)
        domicilio = emisor.find(self.tree['expedido_en'])
        if domicilio is not None:
            for k, v in domicilio.attrib.items():
                if k == 'codigoPostal':
                    v = 'C.P. %s' % v
                self._set_cell('{expedidoen.%s}' % k, v)
        regimen = emisor.find(self.tree['regimen_fiscal'])
        if regimen is not None:
            for k, v in regimen.attrib.items():
                self._set_cell('{emisor.%s}' % k, v)
        return

    def _comprobante(self):
        for k, v in self.xml.attrib.items():
            if k == 'total':
                total = float(v)
                self._set_cell('{cfdi.%s}' % k, v, value=True)
            elif k == 'descuento' or k == 'subTotal':
                self._set_cell('{cfdi.%s}' % k, v, value=True)
            else:
                self._set_cell('{cfdi.%s}' % k, v)

        fecha = self.xml.attrib['fecha'].split('T')
        self._set_cell('{cfdi.hora}', fecha[1])
        fecha = self._format_date(fecha[0])
        self._set_cell('{cfdi.fechaformato}', fecha)
        data = {
            'formaDePago': 'Forma de Pago: ',
            'metodoDePago': 'Método de Pago: ',
            'condicionesDePago': 'Condiciones de Pago: ',
            'NumCtaPago': 'Número de Cuenta de Pago: ',
        }
        cfdi_data = ''
        for k, v in data.items():
            if k in self.xml.attrib:
                cfdi_data += '%s %s\n' % (v, self.xml.attrib[k])

        moneda = 'peso'
        mn = '/100 m.n.)-'
        if 'Moneda' in self.xml.attrib:
            moneda = self.xml.attrib['Moneda'].strip()
            cfdi_data += 'Moneda: {}\n'.format(moneda)
            if moneda.lower().startswith('peso'):
                moneda = 'peso'
            elif moneda.lower() in self.g.PESO:
                moneda = 'peso'
            elif moneda.lower() in self.g.DOLAR:
                moneda = 'dólar'
                mn = '/100 usd)-'
            else:
                mn = '/100 )-'
        if 'TipoCambio' in self.xml.attrib:
            tipo_cambio = self.xml.attrib['TipoCambio']
            cfdi_data += 'Tipo de Cambio: {}\n'.format(tipo_cambio)
        self._set_cell('{cfdi.datos}', cfdi_data)

        enletras = NumerosLetras().to_letters(total, moneda, '-( ', mn)
        self._set_cell('{cfdi.totalenletras}', enletras.upper())
        return

    def _save_pdf(self, sm):
        if self.OS == self.WIN:
            pv = sm.Bridge_GetStruct('com.sun.star.beans.PropertyValue')
        else:
            pv = PropertyValue()
        pv.Name = 'FilterName'
        pv.Value = 'calc_pdf_Export'
        self.template.storeToURL(self.path_pdf, (pv,))
        self.template.dispose()
        return

    def _set_cell(self, k='', v='', cell=None, value=False):
        if k:
            self.sd.setSearchString(k)
            ranges = self.search.findAll(self.sd)
            if ranges:
                ranges = ranges.getRangeAddressesAsString().split(';')
                for r in ranges:
                    for c in r.split(','):
                        cell = self.hoja.getCellRangeByName(c)
                        if cell.getImplementationName() == self.g.CELL_TYPE:
                            if value:
                                cell.setValue(float(v))
                            else:
                                pattern = re.compile(k, re.IGNORECASE)
                                value = pattern.sub(v, cell.getString())
                                cell.setString(value)
                return cell
        if cell:
            if cell.getImplementationName() == self.g.CELL_TYPE:
                ca = cell.getCellAddress()
                new_cell = self.hoja.getCellByPosition(ca.Column, ca.Row + 1)
                if value:
                    new_cell.setValue(float(v))
                else:
                    new_cell.setString(v)
                return new_cell

    def _next_cell(self, cell):
        col = cell.getCellAddress().Column
        row = cell.getCellAddress().Row + 1
        return self.hoja.getCellByPosition(col, row)

    def _copy_cell(self, cell):
        destino = self._next_cell(cell)
        self.hoja.copyRange(destino.getCellAddress(), cell.getRangeAddress())
        return destino

    def _clean(self):
        self.sd.SearchRegularExpression = True
        self.sd.setSearchString(self.g.CLEAN)
        self.search.replaceAll(self.sd)
        return

    def _format_date(self, date_string):
        m = (
            '',
            'Enero',
            'Febrero',
            'Marzo',
            'Abril',
            'Mayo',
            'Junio',
            'Julio',
            'Agosto',
            'Septiembre',
            'Octubre',
            'Noviembre',
            'Diciembre'
        )
        d = (
            'Lunes',
            'Martes',
            'Miércoles',
            'Jueves',
            'Viernes',
            'Sábado',
            'Domingo'
        )
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return date.strftime('{}, %d de {} de %Y'.format(
            d[date.weekday()], m[date.month]))


class DescargaSAT(object):

    def __init__(self, data, status_callback=print,
            download_callback=print):
        self.g = Global()
        self.util = Util()
        self.status = status_callback
        self.progress = download_callback
        self._download_sat(data)

    def _download_sat(self, data):
        'Descarga CFDIs del SAT a una carpeta local'

        self.status('Abriendo Firefox...')
        page_query = self.g.SAT['page_receptor']
        if data['type_invoice'] == 1:
            page_query = self.g.SAT['page_emisor']
        # To prevent download dialog
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            'browser.download.folderList', 2)
        profile.set_preference(
            'browser.download.manager.showWhenStarting', False)
        profile.set_preference(
            'browser.helperApps.alwaysAsk.force', False)
        profile.set_preference(
            'browser.helperApps.neverAsk.saveToDisk',
            'text/xml, application/octet-stream, application/xml')
        profile.set_preference(
            'browser.download.dir', data['user_sat']['target_sat'])
        # mrE - desactivar telemetry
        profile.set_preference(
            'toolkit.telemetry.prompted', 2)
        profile.set_preference(
            'toolkit.telemetry.rejected', True)
        profile.set_preference(
            'toolkit.telemetry.enabled', False)
        profile.set_preference(
            'datareporting.healthreport.service.enabled', False)
        profile.set_preference(
            'datareporting.healthreport.uploadEnabled', False)
        profile.set_preference(
            'datareporting.healthreport.service.firstRun', False)
        profile.set_preference(
            'datareporting.healthreport.logging.consoleEnabled', False)
        profile.set_preference(
            'datareporting.policy.dataSubmissionEnabled', False)
        profile.set_preference(
            'datareporting.policy.dataSubmissionPolicyResponseType', 'accepted-info-bar-dismissed')
        #profile.set_preference(
        #    'datareporting.policy.dataSubmissionPolicyAccepted'; False) # este me marca error, why?
        #oculta la gran flecha animada al descargar
        profile.set_preference(
            'browser.download.animateNotifications', False)
        try:
            browser = webdriver.Firefox(profile)
            self.status('Conectando...')
            browser.get(self.g.SAT['page_init'])
            txt = browser.find_element_by_name(self.g.SAT['user'])
            txt.send_keys(data['user_sat']['user_sat'])
            txt = browser.find_element_by_name(self.g.SAT['password'])
            txt.send_keys(data['user_sat']['password'])
            txt.submit()
            self.util.sleep(3)
            self.status('Conectado...')
            browser.get(page_query)
            self.util.sleep(3)
            self.status('Buscando...')
            if data['type_search'] == 1:
                txt = browser.find_element_by_id(self.g.SAT['uuid'])
                txt.click()
                txt.send_keys(data['search_uuid'])
            else:
                # Descargar por fecha
                opt = browser.find_element_by_id(self.g.SAT['date'])
                opt.click()
                self.util.sleep()
                if data['search_rfc']:
                    if data['type_search'] == 1:
                        txt = browser.find_element_by_id(self.g.SAT['receptor'])
                    else:
                        txt = browser.find_element_by_id(self.g.SAT['emisor'])
                    txt.send_keys(data['search_rfc'])
                # Emitidas
                if data['type_invoice'] == 1:
                    year = int(data['search_year'])
                    month = int(data['search_month'])
                    dates = self.util.get_dates(year, month)
                    txt = browser.find_element_by_id(self.g.SAT['date_from'])
                    arg = "document.getElementsByName('{}')[0]." \
                        "removeAttribute('disabled');".format(
                        self.g.SAT['date_from_name'])
                    browser.execute_script(arg)
                    txt.send_keys(dates[0])
                    txt = browser.find_element_by_id(self.g.SAT['date_to'])
                    arg = "document.getElementsByName('{}')[0]." \
                        "removeAttribute('disabled');".format(
                        self.g.SAT['date_to_name'])
                    browser.execute_script(arg)
                    txt.send_keys(dates[1])
                # Recibidas
                else:
                    #~ combos = browser.find_elements_by_class_name(
                        #~ self.g.SAT['combos'])
                    #~ combos[0].click()
                    combo = browser.find_element_by_id(self.g.SAT['year'])
                    combo = browser.find_element_by_id(
                        'sbToggle_{}'.format(combo.get_attribute('sb')))
                    combo.click()
                    self.util.sleep(2)
                    link = browser.find_element_by_link_text(
                        data['search_year'])
                    link.click()
                    self.util.sleep(2)
                    combo = browser.find_element_by_id(self.g.SAT['month'])
                    combo = browser.find_element_by_id(
                        'sbToggle_{}'.format(combo.get_attribute('sb')))
                    combo.click()
                    self.util.sleep(2)
                    link = browser.find_element_by_link_text(
                        data['search_month'])
                    link.click()
                    self.util.sleep(2)
                    if data['search_day'] != '00':
                        combo = browser.find_element_by_id(self.g.SAT['day'])
                        sb = combo.get_attribute('sb')
                        combo = browser.find_element_by_id(
                            'sbToggle_{}'.format(sb))
                        combo.click()
                        self.util.sleep()
                        if data['search_month'] == data['search_day']:
                            links = browser.find_elements_by_link_text(
                                data['search_day'])
                            for l in links:
                                p = l.find_element_by_xpath(
                                    '..').find_element_by_xpath('..')
                                sb2 = p.get_attribute('id')
                                if sb in sb2:
                                    link = l
                                    break
                        else:
                            link = browser.find_element_by_link_text(
                                data['search_day'])
                        link.click()
                        self.util.sleep()

            browser.find_element_by_id(self.g.SAT['submit']).click()
            sec = 3
            if data['type_invoice'] != 1 and data['search_day'] == '00':
                sec = 15
            self.util.sleep(sec)
            # Bug del SAT
            if data['type_invoice'] != 1 and data['search_day'] != '00':
                combo = browser.find_element_by_id(self.g.SAT['day'])
                sb = combo.get_attribute('sb')
                combo = browser.find_element_by_id(
                    'sbToggle_{}'.format(sb))
                combo.click()
                self.util.sleep(2)
                if data['search_month'] == data['search_day']:
                    links = browser.find_elements_by_link_text(
                        data['search_day'])
                    for l in links:
                        p = l.find_element_by_xpath(
                            '..').find_element_by_xpath('..')
                        sb2 = p.get_attribute('id')
                        if sb in sb2:
                            link = l
                            break
                else:
                    link = browser.find_element_by_link_text(
                        data['search_day'])
                link.click()
                self.util.sleep(2)
                browser.find_element_by_id(self.g.SAT['submit']).click()
                self.util.sleep(sec)
            elif data['type_invoice'] == 2 and data['sat_month']:
                return self._download_sat_month(data, browser)

            try:
                found = True
                content = browser.find_elements_by_class_name(
                    self.g.SAT['subtitle'])
                for c in content:
                    if self.g.SAT['found'] in c.get_attribute('innerHTML') \
                        and c.is_displayed():
                        found = False
                        break
            except Exception as e:
                print (str(e))

            if found:
                docs = browser.find_elements_by_name(self.g.SAT['download'])
                t = len(docs)
                for i, v in enumerate(docs):
                    msg = 'Factura {} de {}'.format(i+1, t)
                    self.progress(i + 1, t)
                    self.status(msg)
                    download = self.g.SAT['page_cfdi'].format(
                        v.get_attribute('onclick').split("'")[1])
                    browser.get(download)
                self.progress(0, t)
                self.util.sleep()
            else:
                self.status('Sin facturas...')
        except Exception as e:
            print (e)
        finally:
            try:
                self.status('Desconectando...')
                link = browser.find_element_by_partial_link_text('Cerrar Sesi')
                link.click()
            except:
                pass
            finally:
                browser.close()
        self.status('Desconectado...')
        return

    def _download_sat_month(self, data, browser):
        '''Descarga CFDIs del SAT a una carpeta local

        Todos los CFDIs del mes selecionado'''

        year = int(data['search_year'])
        month = int(data['search_month'])
        days_month = self.util.get_days(year, month) + 1
        days = ['%02d' % x for x in range(1, days_month)]
        for d in days:
            combo = browser.find_element_by_id(self.g.SAT['day'])
            sb = combo.get_attribute('sb')
            combo = browser.find_element_by_id('sbToggle_{}'.format(sb))
            combo.click()
            self.util.sleep(2)
            if data['search_month'] == d:
                links = browser.find_elements_by_link_text(d)
                for l in links:
                    p = l.find_element_by_xpath(
                        '..').find_element_by_xpath('..')
                    sb2 = p.get_attribute('id')
                    if sb in sb2:
                        link = l
                        break
            else:
                link = browser.find_element_by_link_text(d)
            link.click()
            self.util.sleep(2)
            browser.find_element_by_id(self.g.SAT['submit']).click()
            self.util.sleep(3)
            docs = browser.find_elements_by_name(self.g.SAT['download'])
            if docs:
                t = len(docs)
                for i, v in enumerate(docs):
                    msg = 'Factura {} de {}'.format(i+1, t)
                    self.progress(i + 1, t)
                    self.status(msg)
                    download = self.g.SAT['page_cfdi'].format(
                        v.get_attribute('onclick').split("'")[1])
                    browser.get(download)
                    self.util.sleep()
                self.progress(0, t)
                self.util.sleep()
        return
