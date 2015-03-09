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

import tkinter as tk
import pygubu
from selenium import webdriver
from pyutil import Util
from pyutil import Mail
from pyutil import LibO
from pyutil import CFDIPDF
from pyutil import DescargaSAT
from values import Global


class Application(pygubu.TkApplication):

    def __init__(self, parent):
        self.parent = parent
        self.util = Util()
        self.g = Global()
        self._init_var()
        self._create_ui()

    def _init_var(self):
        self.builder = pygubu.Builder()
        self.config = self.util.load_config(self.g.FILES['config'])
        self.users_sat = {}
        self.mail_servers = {}
        self.users_xml = {}
        self.users_pdf = {}
        self.users_report = {}
        #~ self.reports = {}
        return

    def _create_ui(self):
        self.builder.add_from_file(self.g.FILES['main'])
        self.builder.add_resource_path(self.g.PATHS['img'])
        self.main = self.builder.get_object(self.g.MAIN, self.parent)
        # Send mail author, remove wend bug fix
        for k, v in self.g.CONTROLS.items():
            control = self.builder.get_object(k)
            for p, v in self.g.CONTROLS[k].items():
                    control[p] = v

        self.builder.connect_callbacks(self)
        self.parent.title(self.g.TITLE)
        self.parent.resizable(0, 0)
        self._center_window(self.parent)
        if self.config:
            key = 'contribuyentes'
            if key in self.config:
                self.users_sat = self.config[key]
                listbox = self._get_object('listbox_contribuyentes')
                for k, _ in self.config[key].items():
                    self.util.listbox_insert(listbox, k)
                if len(self.users_sat) == 1:
                    self._set('current_user', k)
            key = 'mail_servers'
            if key in self.config:
                self.mail_servers = self.config[key]
                listbox = self._get_object('listbox_mail_servers')
                for k, _ in self.config[key].items():
                    self.util.listbox_insert(listbox, k)
            key = 'users_xml'
            if key in self.config:
                self.users_xml = self.config[key]
                listbox = self._get_object('listbox_users_xml')
                for k, _ in self.config[key].items():
                    self.util.listbox_insert(listbox, k)
                if len(self.users_xml) == 1:
                    self._set('current_user_xml', k)
            key = 'users_pdf'
            if key in self.config:
                self.users_pdf = self.config[key]
                listbox = self._get_object('listbox_users_pdf')
                for k, _ in self.config[key].items():
                    self.util.listbox_insert(listbox, k)
                if len(self.users_pdf) == 1:
                    self._set('current_user_pdf', k)
            key = 'users_report'
            if key in self.config:
                self.users_report = self.config[key]
                listbox = self._get_object('listbox_users_report')
                for k, _ in self.config[key].items():
                    self.util.listbox_insert(listbox, k)
                if len(self.users_report) == 1:
                    self._set('current_user_report', k)
                    listbox = self._get_object('listbox_reports')
                    reports = self.users_report[k]['reports']
                    for k, _ in reports.items():
                        self.util.listbox_insert(listbox, k)

            options = (
                'options_mail',
                'options_xml',
                'options_pdf',
                'options_report',
            )
            for opt in options:
                if opt in self.config:
                    data = self.config[opt]
                    for k, v in self.config[opt].items():
                        self._set(k, v)

        now = self.util.now()
        combo = self._get_object('combo_year')
        years = range(self.g.YEAR_INIT, now.year + 1)
        self.util.combo_values(combo, years)
        combo = self._get_object('combo_month')
        months = ['%02d' % x for x in range(1, 13)]
        self.util.combo_values(combo, months, now.month - 1)
        combo = self._get_object('combo_day')
        days_month = self.util.get_days(now.year, now.month) + 1
        days = ['%02d' % x for x in range(0, days_month)]
        self.util.combo_values(combo, days, 0)
        self._set('mail_port', 993)
        self._get_object('check_ssl').invoke()
        self._focus_set('text_rfc')
        return

    def _center_window(self, root):
        w = 710
        h = 560
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        return

    def _get(self, name, var=False):
        if var:
            return self.builder.get_variable(name)
        else:
            return self.builder.get_variable(name).get()

    def _set(self, name, value='', update=False):
        self.builder.get_variable(name).set(value)
        if update:
            self.parent.update_idletasks()
        return

    def _get_object(self, name):
        return self.builder.get_object(name)

    def _focus_set(self, name):
        control = name
        if isinstance(name, str):
            control = self._get_object(name)
        control.focus_set()
        return

    def _config(self, name, properties):
        control = name
        if isinstance(name, str):
            control = self._get_object(name)
        control.config(**properties)
        return

    def _focus_in(self, event):
        w = event.widget
        w['bg'] = self.g.COLORS['FOCUS_IN']
        if isinstance(w, tk.Entry):
            w.selection_range(0, tk.END)
        return

    def _focus_out(self, event):
        event.widget['bg'] = self.g.COLORS['FOCUS_OUT']
        return

    def listbox_contribuyentes_click(self, event):
        w = event.widget
        if w.curselection():
            self._set('current_user', event.widget.get(w.curselection()[0]))
        return

    def listbox_contribuyentes_double_click(self, event):
        w = event.widget
        if w.curselection():
            sel = w.get(w.curselection()[0])
            info = 'Destino: ' + self.users_sat[sel]['target_sat']
            self.util.msgbox(info, 2)
        return

    def listbox_mail_servers_click(self, event):
        w = event.widget
        sel = w.get(w.curselection()[0])
        self.util.msgbox(self.mail_servers[sel]['mail_target'], 2)
        return

    def radio_type_query(self, event):
        w = event.widget
        w['bg'] = self.g.COLORS['FOCUS_IN']
        opt = self._get('type_invoice')
        if opt == 1:
            radio = 'radio_invoice_receive'
            msg = 'RFC Receptor '
        else:
            radio = 'radio_invoice_send'
            msg = 'RFC Emisor '
        self._config(radio, {'bg': self.g.COLORS['DEFAULT']})
        self._set('info_rfc', msg)
        return

    def radio_type_search(self, event):
        w = event.widget
        w['bg'] = self.g.COLORS['FOCUS_IN']
        opt = self._get('type_search')
        if opt == 1:
            self._focus_set('text_uuid')
            radio = 'radio_search_date'
        else:
            self._focus_set('text_rfc')
            radio = 'radio_search_uuid'
        self._config(radio, {'bg': self.g.COLORS['DEFAULT']})
        return

    def radio_organizate_xml(self, event):
        w = event.widget
        w['bg'] = self.g.COLORS['FOCUS_IN']
        opt = self._get('xml_organizate')
        if opt == 1:
            self._config('radio_emisor', {'bg': self.g.COLORS['DEFAULT']})
            self._config('radio_receptor', {'bg': self.g.COLORS['DEFAULT']})
        elif opt == 2:
            self._config('radio_only_date', {'bg': self.g.COLORS['DEFAULT']})
            self._config('radio_receptor', {'bg': self.g.COLORS['DEFAULT']})
        elif opt == 3:
            self._config('radio_only_date', {'bg': self.g.COLORS['DEFAULT']})
            self._config('radio_emisor', {'bg': self.g.COLORS['DEFAULT']})
        return

    def radio_rename_xml(self, event):
        w = event.widget
        w['bg'] = self.g.COLORS['FOCUS_IN']
        opt = self._get('xml_rename')
        if opt == 1:
            self._config('radio_uuid', {'bg': self.g.COLORS['DEFAULT']})
            self._config('radio_template', {'bg': self.g.COLORS['DEFAULT']})
        elif opt == 2:
            self._config('radio_original', {'bg': self.g.COLORS['DEFAULT']})
            self._config('radio_template', {'bg': self.g.COLORS['DEFAULT']})
        elif opt == 3:
            self._config('radio_original', {'bg': self.g.COLORS['DEFAULT']})
            self._config('radio_uuid', {'bg': self.g.COLORS['DEFAULT']})
        return

    def radio_template_type(self, event):
        w = event.widget
        w['bg'] = self.g.COLORS['FOCUS_IN']
        opt = self._get('template_type')
        radio = 'radio_ods'
        button = 'button_select_template_ods'
        self._config(button, {'state': 'normal'})
        self._config('button_select_template_json', {'state': 'normal'})
        if opt == 1:
            radio = 'radio_json'
            button = 'button_select_template_json'
        self._config(radio, {'bg': self.g.COLORS['DEFAULT']})
        self._config(button, {'state': 'disabled'})
        return

    def button_save_emisor_click(self):
        ok, data = self._validate_save_emisor()
        if not ok:
            return
        self.users_sat[data['razon_social']] = data
        listbox = self._get_object('listbox_contribuyentes')
        self.util.listbox_insert(listbox, data['razon_social'])
        var = ('razon_social', 'user_sat', 'password', 'target_sat')
        for v in var:
            self._set(v)
        self.util.save_config(
            self.g.FILES['config'], 'contribuyentes', self.users_sat)
        self._set('current_user', data['razon_social'])
        return

    def _validate_save_emisor(self):
        data = ()
        razon_social = self._get('razon_social').upper().strip()
        user_sat = self._get('user_sat').upper().strip()
        password = self._get('password').strip()
        target_sat = self._get('target_sat')
        if not razon_social:
            self._focus_set('text_razon_social')
            msg = 'El campo RAZON SOCIAL es requerido'
            self.util.msgbox(msg)
            return False, data
        if razon_social in self.users_sat:
            self._focus_set('text_razon_social')
            msg = 'Esta RAZON SOCIAL ya esta guardada'
            self.util.msgbox(msg)
            return False, data
        if not user_sat:
            self._focus_set('text_user_sat')
            msg = 'El campo RFC es requerido'
            self.util.msgbox(msg)
            return False, data
        if len(user_sat) < 12 or len(user_sat) > 13:
            self._focus_set('text_user_sat')
            msg = 'La longitud del RFC es incorrecta'
            self.util.msgbox(msg)
            return False, data
        for k, v in self.users_sat.items():
            if self.users_sat[k]['user_sat'] == user_sat:
                self._focus_set('text_user_sat')
                msg = 'Este RFC ya esta dado de alta'
                self.util.msgbox(msg)
                return False, data
        if not password:
            self._focus_set('text_password')
            msg = 'El campo CLAVE CIEC es requerido'
            self.util.msgbox(msg)
            return False, data
        if not target_sat:
            self._focus_set('text_target_sat')
            msg = 'El campo DIRECTORIO DESTINO es requerido'
            self.util.msgbox(msg)
            return False, data

        data = {
            'razon_social': razon_social,
            'user_sat': user_sat,
            'password': password,
            'target_sat': self.util.path_config(target_sat)
        }
        return True, data

    def button_delete_emisor_click(self):
        listbox = self._get_object('listbox_contribuyentes')
        sel = self.util.listbox_selection(listbox)
        if sel:
            var = ('razon_social', 'user_sat', 'password', 'target_sat')
            for v in var:
                self._set(v, self.users_sat[sel][v])
            del self.users_sat[sel]
            self.util.listbox_delete(listbox)
            self.util.save_config(
                self.g.FILES['config'], 'contribuyentes', self.users_sat)
            self._set('current_user')
        else:
            self._focus_set(listbox)
            msg = 'Selecciona el contribuyente a eliminar de la lista'
            self.util.msgbox(msg)
        return

    def button_select_folder_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('target_sat', folder)
        return

    def combo_month_click(self, event):
        combo = self._get_object('combo_day')
        days_month = self.util.get_days(
            self._get('search_year'), self._get('search_month')) + 1
        days = ['%02d' % x for x in range(0, days_month)]
        self.util.combo_values(combo, days, 0)
        return

    def msg_user(self, msg):
        self._set('msg_user', msg, True)

    def progress(self, value, maximum):
        pb = self._get_object('progressbar')
        pb['value'] = value
        pb['maximum'] = maximum
        self.parent.update_idletasks()

    def button_download_sat_click(self):
        ok, data = self._validate_download_sat()
        if not ok:
            return
        DescargaSAT(data, status_callback=self.msg_user,
                    download_callback=self.progress)
        return

    def _validate_download_sat(self):
        '''Valida requisitos y crea datos para descarga

        Las validaciones son:

        - Al menos una tríada RFC, CIEC y carpeta
          destino ha sido registrada
        - Una tríada RFC, CIEC y carpeta destino
          está seleccionada
        - La UUID no es nula y tiene 36 caracteres,
          si se seleccionó *Buscar por folio
          fiscal (UUID)*
        - El RFC del emisor tiene 12 o 13
          caracteres, si se proporciona

        Si falta alguna de estas condiciones,
        se abre un diálogo con un texto informativo
        y un botón 'OK' en el ambiente gráfico
        y se regresa (False, {})

        Si las validaciones pasan, se construye un
        diccionario ``data`` con estas llaves y valores:

        - user_sat: un diccionario con el
          RFC, la CIEC y la carpeta destino
          que se seleccionaron, con las llaves
          ``user_sat``, ``password`` y ``target_sat``.
        - type_invoice: La selección hecha en
          *Tipo de consulta*: 2 facturas recibidas,
          1 facturas emitidas
        - type_search: La selección hecha en *Tipo
          de búsqueda*: 0 por fecha,
          1 por folio fiscal (UUID)
        - search_uuid: el valor llenado para *UUID*,
          es cadena vacía por omisión
        - search_rfc: el valor llenado en *RFC Emisor*,
          es cadena vacía por omisión
        - search_year: el valor seleccionado en *Año*
          como cadena, es el año en curso por omisión
        - search_month: el valor seleccionado en *Mes*
          como cadena, es el mes en curso por omisión
        - search_day: el valor seleccionado en *Día*
          como cadena, es '00' por omisión o si sat_month
          es verdadero.
        - sat_month: Representa la caja a la izquierda de
          *Descargar mes completo por día*.

        La función regresa (True, data)
        '''

        data = {}
        if not self.users_sat:
            msg = 'Agrega un RFC y contraseña a consultar'
            self.util.msgbox(msg)
            return False, data
        current_user = self._get('current_user')
        if not current_user:
            msg = 'Selecciona primero una Razón Social'
            self.util.msgbox(msg)
            return False, data
        uuid = self._get('search_uuid')
        opt = self._get('type_search')
        rfc = ''
        if opt == 1:
            if not uuid:
                self._focus_set('text_uuid')
                msg = 'El campo UUID es requerido'
                self.util.msgbox(msg)
                return False, data
            if len(uuid) != 36:
                self._focus_set('text_uuid')
                msg = 'La longitud del campo UUID es incorrecta'
                self.util.msgbox(msg)
                return False, data
        else:
            rfc = self._get('search_rfc').strip().upper()
            if rfc:
                if len(rfc) < 12 or len(rfc) > 13:
                    self._focus_set('text_rfc')
                    msg = 'La longitud del RFC es incorrecta'
                    self.util.msgbox(msg)
                    return False, data
        sat_month = self._get('sat_month')
        if sat_month:
            search_day = '00'
        else:
            search_day = self._get('search_day')
        data = {
            'user_sat': self.users_sat[current_user],
            'type_invoice': self._get('type_invoice'),
            'type_search': opt,
            'search_uuid': uuid,
            'search_rfc': rfc,
            'search_year': self._get('search_year'),
            'search_month': self._get('search_month'),
            'search_day': search_day,
            'sat_month': sat_month,
        }

        return True, data

    def check_ssl_click(self, event):
        port = 143
        mail_ssl = self._get('mail_ssl')
        if mail_ssl == 1:
            port = 993
        self._set('mail_port', port)
        return

    def button_select_folder_mail_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('mail_target', folder)
        return

    def button_save_mail_server_click(self):
        ok, data = self._validate_mail()
        if not ok:
            return
        self.mail_servers[data['mail_user']] = data
        listbox = self._get_object('listbox_mail_servers')
        self.util.listbox_insert(listbox, data['mail_user'])
        var = ('mail_server', 'mail_user', 'mail_password', 'mail_target')
        for v in var:
            self._set(v)
        self._set('mail_port', 993)
        self._set('mail_ssl', 1)
        self.util.save_config(
            self.g.FILES['config'], 'mail_servers', self.mail_servers)
        return

    def _validate_mail(self):
        data = {}
        mail_server = self._get('mail_server')
        if not mail_server:
            self._focus_set('text_mail_server')
            msg = 'Captura el servidor IMAP'
            self.util.msgbox(msg)
            return False, data

        mail_port = self._get('mail_port')
        mail_ssl = self._get('mail_ssl')

        mail_user = self._get('mail_user')
        if not mail_user:
            self._focus_set('text_mail_user')
            msg = 'Captura el nombre de usuario'
            self.util.msgbox(msg)
            return False, data

        if mail_user in self.mail_servers:
            msg = 'Este servidor y usuario ya esta en la lista, si ' \
                'quieres cambiar los datos, primero eliminalo.'
            self.util.msgbox(msg)
            return False, data

        mail_password = self._get('mail_password')
        if not mail_password:
            self._focus_set('text_mail_password')
            msg = 'Captura la contraseña de acceso'
            self.util.msgbox(msg)
            return False, data

        mail_target = self._get('mail_target')
        if not mail_target:
            self._focus_set('text_mail_target')
            msg = 'Selecciona el directorio destino de descarga'
            self.util.msgbox(msg)
            return False, data

        if not self.util.validate_dir(mail_target, 'w'):
            self._focus_set('text_mail_target')
            msg = 'No tienes derechos de escritura en el directorio destino'
            self.util.msgbox(msg)
            return False, data

        data['mail_server'] = mail_server
        data['mail_port'] = mail_port
        data['mail_ssl'] = mail_ssl
        data['mail_user'] = mail_user
        data['mail_password'] = mail_password
        data['mail_target'] = self.util.path_config(mail_target)

        mail = Mail(data)
        if mail.error:
            self.util.msgbox(mail.error)
            del mail
            return False, {}
        return True, data

    def button_delete_mail_server_click(self):
        listbox = self._get_object('listbox_mail_servers')
        sel = self.util.listbox_selection(listbox)
        if sel:
            var = (
                'mail_server',
                'mail_port',
                'mail_ssl',
                'mail_user',
                'mail_password',
                'mail_target')
            for v in var:
                self._set(v, self.mail_servers[sel][v])
            del self.mail_servers[sel]
            self.util.listbox_delete(listbox)
            self.util.save_config(
                self.g.FILES['config'], 'mail_servers', self.mail_servers)
        else:
            self._focus_set(listbox)
            msg = 'Selecciona el contribuyente a eliminar de la lista'
            self.util.msgbox(msg)
        return

    def button_download_mail_click(self):
        ok, data = self._validate_download_mail()
        if not ok:
            return
        self.util.save_config(
            self.g.FILES['config'], 'options_mail', data)

        pb = self._get_object('progressbar')
        info = self._get('msg_user', True)
        for k, v in self.mail_servers.items():
            mail = Mail(v)
            if mail.error:
                msg = mail.error
                del mail
                self.util.msgbox(msg)
                continue
            #~ try:
            mail.down_all_mails(pb, info, data)
            #~ except Exception as e:
                #~ print (e)
            #~ finally:
            del mail
        pb['value'] = 0
        pb.stop()
        self._set('msg_user', 'Descarga completa...')
        return

    def _validate_download_mail(self):
        data = {}
        if not self.mail_servers:
            msg = 'Agrega una cuenta de correo primero.'
            self.util.msgbox(msg)
            return False, data

        data['mail_subfolder'] = self._get('mail_subfolder')
        data['mail_name'] = self._get('mail_name')
        data['mail_delete1'] = self._get('mail_delete1')
        data['mail_delete2'] = self._get('mail_delete2')
        return True, data

    def button_select_folder_source_xml_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('xml_source', folder)
            self._set('xml_target', folder)
        return

    def button_select_folder_target_xml_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('xml_target', folder)
        return

    def listbox_users_xml_double_click(self, event):
        w = event.widget
        if w.curselection():
            sel = w.get(w.curselection()[0])
            info = 'Origen: ' + self.users_xml[sel]['xml_source'] + '\n\n'
            info += 'Destino: ' + self.users_xml[sel]['xml_target'] + '\n'
            self.util.msgbox(info, 2)
        return

    def listbox_users_xml_click(self, event):
        w = event.widget
        if w.curselection():
            self._set('current_user_xml', w.get(w.curselection()[0]))
        return

    def listbox_users_pdf_click(self, event):
        w = event.widget
        if w.curselection():
            sel = w.get(w.curselection()[0])
            info = 'Origen: ' + self.users_pdf[sel]['pdf_source'] + '\n\n'
            info += 'Destino: ' + self.users_pdf[sel]['pdf_target'] + '\n\n'
            self.util.msgbox(info, 2)
        return

    def button_save_xml_user_click(self):
        ok, data = self._validate_xml_user()
        if not ok:
            return

        self.users_xml[data['xml_user']] = data
        listbox = self._get_object('listbox_users_xml')
        self.util.listbox_insert(listbox, data['xml_user'])
        var = ('xml_user', 'xml_source', 'xml_target')
        for v in var:
            self._set(v)
        self._set('xml_copy', 0)
        self.util.save_config(
            self.g.FILES['config'], 'users_xml', self.users_xml)
        self._set('current_user_xml', data['xml_user'])
        return

    def _validate_xml_user(self):
        data = {}

        xml_user = self._get('xml_user').strip().upper()
        if not xml_user:
            self._focus_set('text_xml_user')
            msg = 'Captura el campo USUARIO'
            self.util.msgbox(msg)
            return False, data

        if xml_user in self.users_xml:
            msg = 'Este usuario ya esta en la lista, si ' \
                'quieres cambiar los datos, primero eliminalo.'
            self.util.msgbox(msg)
            return False, data

        xml_source = self._get('xml_source')
        if not xml_source:
            self._focus_set('text_xml_source')
            msg = 'Selecciona el directorio origen para este usuario'
            self.util.msgbox(msg)
            return False, data

        if not self.util.validate_dir(xml_source, 'r'):
            self._focus_set('text_xml_source')
            msg = 'No tienes derechos de lectura en el directorio origen'
            self.util.msgbox(msg)
            return False, data

        xml_target = self._get('xml_target')
        if not xml_target:
            self._focus_set('text_xml_target')
            msg = 'Selecciona el directorio destino para este usuario'
            self.util.msgbox(msg)
            return False, data

        if not self.util.validate_dir(xml_target, 'w'):
            self._focus_set('text_xml_target')
            msg = 'No tienes derechos de escritura en el directorio destino'
            self.util.msgbox(msg)
            return False, data

        data['xml_user'] = xml_user
        data['xml_source'] = self.util.path_config(xml_source)
        data['xml_target'] = self.util.path_config(xml_target)
        data['xml_copy'] = self._get('xml_copy')
        return True, data

    def button_delete_xml_user_click(self):
        listbox = self._get_object('listbox_users_xml')
        sel = self.util.listbox_selection(listbox)
        if sel:
            var = (
                'xml_user',
                'xml_source',
                'xml_target',
                'xml_copy',
            )
            for v in var:
                self._set(v, self.users_xml[sel][v])
            del self.users_xml[sel]
            self.util.listbox_delete(listbox)
            self.util.save_config(
                self.g.FILES['config'], 'users_xml', self.users_xml)
            self._set('current_user_xml')
        else:
            self._focus_set(listbox)
            msg = 'Selecciona el usuario a eliminar de la lista'
            self.util.msgbox(msg)
        return

    def button_organizate_xml_click(self):
        ok, options = self._validate_organizate_xml()
        if not ok:
            return
        files = options['files']
        del options['files']
        total = len(files)
        data = self.users_xml[options['xml_user']]
        del options['xml_user']
        self.util.save_config(self.g.FILES['config'], 'options_xml', options)
        data.update(options)

        pb = self._get_object('progressbar')
        pb['maximum'] = total
        pb.start()
        j = 0
        for i, f in enumerate(files):
            pb['value'] = i + 1
            pb.update_idletasks()
            if self._organizate_xml(f, data):
                j += 1
        pb['value'] = 0
        pb.stop()
        msg = 'Archivos XML encontrados: {}\n'
        msg += 'Archivos XML organizados: {}'
        msg = msg.format(total, j)
        self.util.msgbox(msg, 2)
        return

    def _organizate_xml(self, path, data):
        pdf_ori = '{}_ORIGINAL.pdf'
        name_file_uuid = ''
        name_file_template = ''
        info_pdf = self.util.get_path_info(path)
        name_pdf_1 = pdf_ori.format(info_pdf[2])
        name_pdf_2 = '{}.pdf'.format(info_pdf[2])
        paths_pdf = (
            (self.util.join(info_pdf[0], name_pdf_1), name_pdf_1),
            (self.util.join(info_pdf[0], name_pdf_2), name_pdf_2),
        )
        info = self.util.get_info_xml(path, self.g.PREFIX)
        if info:
            subdir = ''
            if data['xml_organizate'] == 2:
                subdir = info['emisor_rfc']
            elif data['xml_organizate'] == 3:
                subdir = info['receptor_rfc']
            if data['xml_rename'] == 1:
                name_file = self.util.get_path_info(path, 2)
            elif data['xml_rename'] == 2:
                name_file = name_file_uuid = info['uuid']
            elif data['xml_rename'] == 3:
                name_file = name_file_template = self.util.get_name(
                    path, self.g.PREFIX,
                    data['template_name'],
                    self.g.FILE_NAME)
            name_file = '{}{}'.format(name_file.upper(), self.g.EXT_XML)
            path_dest = self.util.join(
                data['xml_target'], subdir, info['year'], info['month'])
            self.util.makedirs(path_dest)
            target = self.util.join(path_dest, name_file)
            for p in paths_pdf:
                if self.util.exists(p[0]):
                    if name_file_uuid:
                        path_dest = self.util.join(
                            path_dest,
                            pdf_ori.format(name_file_uuid.upper()))
                    elif name_file_template:
                        path_dest = self.util.join(
                            path_dest,
                            pdf_ori.format(name_file_template.upper()))
                    else:
                        path_dest = self.util.join(path_dest, p[1])
                    if data['xml_copy']:
                        self.util.copy(p[0], path_dest)
                    else:
                        self.util.move(p[0], path_dest)
            if data['xml_copy']:
                return self.util.copy(path, target)
            else:
                return self.util.move(path, target)
        return False

    def _validate_organizate_xml(self):
        xml_user = self._get('current_user_xml')
        if not xml_user:
            msg = 'Selecciona un usuario primero'
            self.util.msgbox(msg)
            return False, {}

        data = self.users_xml[xml_user]

        files = self.util.get_files(data['xml_source'])
        if not files:
            msg = 'No se encontraron archivos XML en el directorio origen\n\n'
            msg += data['xml_source']
            self.util.msgbox(msg)
            return False, {}

        msg = 'Se van a organizar {} archivos XML.\n\n' \
            '¿Estás seguro de continuar?'
        if not self.util.question(msg.format(len(files))):
            return False, {}

        data = {}
        data['xml_user'] = xml_user
        data['xml_organizate'] = self._get('xml_organizate')
        data['xml_rename'] = self._get('xml_rename')
        data['template_name'] = self._get('template_name').strip()
        data['files'] = files
        return True, data

    def button_select_folder_source_pdf_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('pdf_source', folder)
            self._set('pdf_target', folder)
        return

    def button_select_folder_target_pdf_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('target_pdf', folder)
        return

    def button_select_template_ods_click(self):
        file_name = self.util.get_file(self.parent, ext=self.g.EXT_ODS)
        if file_name:
            self._set('template_ods', file_name)
            self._set('template_json')
        return

    def button_select_template_json_click(self):
        file_name = self.util.get_file(self.parent, ext=self.g.EXT_JSON)
        if file_name:
            self._set('template_json', file_name)
            self._set('template_ods')
        return

    def button_save_pdf_user_click(self):
        ok, data = self._validate_pdf_user()
        if not ok:
            return

        self.users_pdf[data['pdf_user']] = data
        listbox = self._get_object('listbox_users_pdf')
        self.util.listbox_insert(listbox, data['pdf_user'])
        var = (
            'pdf_user',
            'pdf_source',
            'pdf_target',
            'template_ods',
            'template_json'
        )
        for v in var:
            self._set(v)
        self.util.save_config(
            self.g.FILES['config'], 'users_pdf', self.users_pdf)
        self._set('current_user_pdf', data['pdf_user'])
        return

    def _validate_pdf_user(self):
        data = {}

        pdf_user = self._get('pdf_user').strip().upper()
        if not pdf_user:
            self._focus_set('text_pdf_user')
            msg = 'Captura el campo USUARIO'
            self.util.msgbox(msg)
            return False, data

        if pdf_user in self.users_pdf:
            msg = 'Este usuario ya esta en la lista, si ' \
                'quieres cambiar los datos, primero eliminalo.'
            self.util.msgbox(msg)
            return False, data

        pdf_source = self._get('pdf_source')
        if not pdf_source:
            self._focus_set('text_pdf_source')
            msg = 'Selecciona el directorio origen para este usuario'
            self.util.msgbox(msg)
            return False, data

        if not self.util.validate_dir(pdf_source, 'r'):
            self._focus_set('text_pdf_source')
            msg = 'No tienes derechos de lectura en el directorio origen'
            self.util.msgbox(msg)
            return False, data

        pdf_target = self._get('pdf_target')
        if not pdf_target:
            self._focus_set('text_pdf_target')
            msg = 'Selecciona el directorio destino para este usuario'
            self.util.msgbox(msg)
            return False, data

        if not self.util.validate_dir(pdf_target, 'w'):
            self._focus_set('text_pdf_target')
            msg = 'No tienes derechos de escritura en el directorio destino'
            self.util.msgbox(msg)
            return False, data

        template_ods = self._get('template_ods')
        if template_ods:
            if not self.util.validate_dir(template_ods):
                msg = 'No se encontró la plantilla ODS'
                self.util.msgbox(msg)
                return False, data
            template_ods = self.util.path_config(template_ods)
        template_json = self._get('template_json')
        if template_json:
            if not self.util.validate_dir(template_json):
                msg = 'No se encontró la plantilla JSON'
                self.util.msgbox(msg)
                return False, data
            template_json = self.util.path_config(template_json)

        template_type = self._get('template_type')
        if template_type == 1:
            if not template_ods:
                msg = 'Selecciona una plantilla ODS'
                self.util.msgbox(msg)
                return False, data
        elif template_type == 2:
            if not template_json:
                msg = 'Selecciona una plantilla JSON'
                self.util.msgbox(msg)
                return False, data

        data['pdf_user'] = pdf_user
        data['pdf_source'] = self.util.path_config(pdf_source)
        data['pdf_target'] = self.util.path_config(pdf_target)
        data['template_ods'] = template_ods
        data['template_json'] = template_json
        #~ data['pdf_print'] = self._get('pdf_print')
        return True, data

    def button_delete_pdf_user_click(self):
        listbox = self._get_object('listbox_users_pdf')
        sel = self.util.listbox_selection(listbox)
        if sel:
            var = (
                'pdf_user',
                'pdf_source',
                'pdf_target',
                'template_ods',
                'template_json',
            )
            for v in var:
                self._set(v, self.users_pdf[sel][v])
            del self.users_pdf[sel]
            self.util.listbox_delete(listbox)
            self.util.save_config(
                self.g.FILES['config'], 'users_pdf', self.users_pdf)
            self._set('current_user_pdf')
        else:
            self._focus_set(listbox)
            msg = 'Selecciona el usuario a eliminar de la lista'
            self.util.msgbox(msg)
        return

    def button_generate_pdf_click(self):
        ok, data = self._validate_pdf()
        if not ok:
            return

        files = data['files']
        del data['files']
        total = len(files)

        libo = LibO()
        if libo.SM is None:
            del libo
            msg = 'No fue posible iniciar LibreOffice, asegurate de que ' \
                'este correctamente instalado e intentalo de nuevo'
            self.util.msgbox(msg)
            return False, data

        pb = self._get_object('progressbar')
        pb['maximum'] = total
        pb.start()
        j = 0
        for i, f in enumerate(files):
            pb['value'] = i + 1
            msg = 'Archivo {} de {}'.format(i + 1, total)
            self._set('msg_user', msg)
            self.parent.update_idletasks()
            if self._make_pdf(f, libo, data['pdf_user']):
                j += 1
        del libo
        pb['value'] = 0
        pb.stop()
        msg = 'Archivos XML encontrados: {}\n'
        msg += 'Archivos PDF generados: {}'
        msg = msg.format(total, j)
        self.util.msgbox(msg)
        return

    def _make_pdf(self, path, libo, data):
        xml = self.util.parse(path)
        if xml is None:
            return False
        source = data['pdf_source']
        target = data['pdf_target']
        template = data['template_ods']
        if data['template_json']:
            template = data['template_json']
        info = self.util.get_path_info(path)
        path_pdf = self.util.join(target, info[0][len(source)+1:])
        self.util.makedirs(path_pdf)
        path_pdf = self.util.join(path_pdf, info[2] + self.g.EXT_PDF)
        path_pdf = libo.path_to(path_pdf)
        try:
            doc = libo.doc_open(template)
            path_to = getattr(libo, 'path_to')
            size = getattr(libo, 'size')
            #~ sm = getattr(libo, 'SM')
            pdf = CFDIPDF(xml, path_pdf, doc, self.g, self.util, path_to, size)
            pdf.make(libo.SM)
            return True
        except Exception as e:
            print (e)
            return False

    def _validate_pdf(self):
        pdf_user = self._get('current_user_pdf')
        if not pdf_user:
            msg = 'Selecciona un usuario primero'
            self.util.msgbox(msg)
            return False, {}

        data = self.users_pdf[pdf_user]
        if not self.util.validate_dir(data['pdf_source'], 'r'):
            msg = 'No tienes derechos de lectura en el directorio origen'
            self.util.msgbox(msg)
            return False, {}

        files = self.util.get_files(data['pdf_source'])
        if not files:
            msg = 'No se encontraron archivos XML en el directorio origen'
            self.util.msgbox(msg)
            return False, {}

        if not self.util.validate_dir(data['pdf_target'], 'w'):
            msg = 'No tienes derechos de escritura en el directorio destino'
            self.util.msgbox(msg)
            return False, {}

        template_ods = data['template_ods']
        if data['template_ods']:
            if not self.util.exists(data['template_ods']):
                msg = 'No se encontró una plantilla en la ruta establecida'
                self.util.msgbox(msg)
                return False, {}
            ext = self.util.get_path_info(data['template_ods'], 3)
            if ext != self.g.EXT_ODS:
                msg = 'La plantilla no es un archivo ODS de Calc'
                self.util.msgbox(msg)
                return False, {}
            libo = LibO()
            if libo.SM is None:
                del libo
                msg = 'No fue posible iniciar LibreOffice, asegurate de que ' \
                    'este correctamente instalado e intentalo de nuevo'
                self.util.msgbox(msg)
                return False, data
            doc = libo.doc_open(data['template_ods'])
            if doc is None:
                del libo
                msg = 'No fue posible abrir la plantilla, asegurate de que ' \
                    'la ruta sea correcta'
                self.util.msgbox(msg)
                return False, data
            doc.dispose()
            del libo
        else:   # ToDO CSV
            return False, {}

        msg = 'Se van a generar {} PDFs\n\n¿Estas seguro de continuar?'
        if not self.util.question(msg.format(len(files))):
            return False, {}

        data['pdf_user'] = data
        data['files'] = files
        return True, data

    def button_select_folder_report_source_click(self):
        folder = self.util.get_folder(self.parent)
        if folder:
            self._set('report_source', folder)
        return

    def button_save_report_user_click(self):
        ok, data = self._validate_report_user()
        if not ok:
            return

        self.users_report[data['report_user']] = data
        listbox = self._get_object('listbox_users_report')
        self.util.listbox_insert(listbox, data['report_user'])
        var = (
            'report_user',
            'report_source',
        )
        for v in var:
            self._set(v)
        self.util.save_config(
            self.g.FILES['config'], 'users_report', self.users_report)
        self._set('current_user_report', data['report_user'])
        return

    def _validate_report_user(self):
        data = {}

        report_user = self._get('report_user').strip().upper()
        if not report_user:
            self._focus_set('text_report_user')
            msg = 'Captura el campo USUARIO'
            self.util.msgbox(msg)
            return False, data

        if report_user in self.users_report:
            msg = 'Este usuario ya esta en la lista, si ' \
                'quieres cambiar los datos, primero eliminalo.'
            self.util.msgbox(msg)
            return False, data

        report_source = self._get('report_source')
        if not report_source:
            self._focus_set('text_report_source')
            msg = 'Selecciona el directorio origen para este usuario'
            self.util.msgbox(msg)
            return False, data

        if not self.util.validate_dir(report_source, 'r'):
            self._focus_set('text_report_source')
            msg = 'No tienes derechos de lectura en el directorio origen'
            self.util.msgbox(msg)
            return False, data

        data['report_user'] = report_user
        data['report_source'] = self.util.path_config(report_source)
        data['reports'] = {}
        return True, data

    def button_delete_report_user_click(self):
        listbox = self._get_object('listbox_users_report')
        sel = self.util.listbox_selection(listbox)
        if sel:
            var = (
                'report_user',
                'report_source',
            )
            for v in var:
                self._set(v, self.users_report[sel][v])
            del self.users_report[sel]
            self.util.listbox_delete(listbox)
            self.util.save_config(
                self.g.FILES['config'], 'users_report', self.users_report)
            self._set('current_user_report')
        else:
            self._focus_set(listbox)
            msg = 'Selecciona el usuario a eliminar de la lista'
            self.util.msgbox(msg)
        return

    def listbox_users_report_double_click(self, event):
        w = event.widget
        if w.curselection():
            sel = w.get(w.curselection()[0])
            info = 'Origen: ' + self.users_report[sel]['report_source']
            self.util.msgbox(info, 2)
        return

    def listbox_users_report_click(self, event):
        w = event.widget
        if w.curselection():
            user = w.get(w.curselection()[0])
            self._set('current_user_report', user)
            if 'reports' in self.users_report[user]:
                listbox = self._get_object('listbox_reports')
                self.util.listbox_delete(listbox, -2)
                reports = self.users_report[user]['reports']
                for k, _ in reports.items():
                    self.util.listbox_insert(listbox, k)
        return

    def button_save_report_title_click(self):
        ok, data = self._validate_report_title()
        if not ok:
            return

        self.users_report[data['report_user']]['reports'][data['report_title']] = data['report_fields']
        listbox = self._get_object('listbox_reports')
        self.util.listbox_insert(listbox, data['report_title'])
        self._set('report_title')
        self._get_object('text_report_fields').delete('1.0', 'end')
        self.util.save_config(
            self.g.FILES['config'], 'users_report', self.users_report)
        return

    def _validate_report_title(self):
        data = {}

        current_user = self._get('current_user_report')
        if not current_user:
            msg = 'Selecciona primero un usuario'
            self.util.msgbox(msg)
            return False, data

        report_title = self._get('report_title').strip().upper()
        if not report_title:
            self._focus_set('text_report_title')
            msg = 'Captura el campo TITULO'
            self.util.msgbox(msg)
            return False, data

        reports = self.users_report[current_user]['reports']
        if report_title in reports:
            msg = 'Este reporte ya esta en la lista, si ' \
                'quieres cambiar los datos, primero eliminalo.'
            self.util.msgbox(msg)
            return False, data

        report_fields = self._get_object(
            'text_report_fields').get('1.0', 'end').rstrip('\n')
        if not report_fields:
            self._focus_set('text_report_fields')
            msg = 'Captura los campos del reporte'
            self.util.msgbox(msg)
            return False, data

        data['report_user'] = current_user
        data['report_title'] = report_title
        data['report_fields'] = report_fields
        return True, data

    def button_delete_report_title_click(self):
        listbox = self._get_object('listbox_reports')
        sel = self.util.listbox_selection(listbox)
        if sel:
            current_user = self._get('current_user_report')
            reports = self.users_report[current_user]['reports']
            self._set('report_title', sel)
            text_fields = self._get_object('text_report_fields')
            text_fields.delete('1.0', 'end')
            text_fields.insert(tk.END, reports[sel])
            del reports[sel]
            self.users_report[current_user]['reports'] = reports
            self.util.listbox_delete(listbox)
            self.util.save_config(
                self.g.FILES['config'], 'users_report', self.users_report)
        else:
            self._focus_set(listbox)
            msg = 'Selecciona el reporte a eliminar de la lista'
            self.util.msgbox(msg)
        return

    def listbox_reports_double_click(self, event):
        w = event.widget
        if w.curselection():
            sel = w.get(w.curselection()[0])
            current_user = self._get('current_user_report')
            info = 'Campos: ' + self.users_report[current_user]['reports'][sel]
            self.util.msgbox(info, 2)
        return

    def button_generate_report_click(self):
        ok, data = self._validate_report()
        if not ok:
            return
        files = data['files']
        del data['files']
        total = len(files)
        titles = self._set_titles(data)
        lines = [titles]
        pb = self._get_object('progressbar')
        pb['maximum'] = total
        pb.start()
        for i, f in enumerate(files):
            pb['value'] = i + 1
            msg = 'Archivo {} de {}'.format(i + 1, total)
            self._set('msg_user', msg)
            self.parent.update_idletasks()
            line_csv = self._make_report(f, data)
            for l in line_csv:
                lines.append(l)
        pb['value'] = 0
        pb.stop()
        path_csv = self.util.get_path_temp(
            '{}.csv'.format(data['title'].replace(' ', '_')))
        self.util.save_csv(lines, path_csv)
        return

    def _make_report(self, path, data):
        return self.util.get_info_report(path, data, self.g)

    def _set_titles(self, data):
        titles = data['fields_report'].split('|')
        for i, v in enumerate(titles):
            titles[i] = v[1:-1].replace('}{', '-')
        if data['validate_fac']:
            titles.append('Validar XML')
        if data['validate_sat']:
            titles.append('Validar SAT')
        return tuple(titles)

    def _validate_report(self):
        data = {}

        listbox = self._get_object('listbox_reports')
        title = self.util.listbox_selection(listbox)
        if not title:
            msg = 'Selecciona un reporte'
            self.util.msgbox(msg)
            return False, data

        current_user = self._get('current_user_report')
        fields_report = self.users_report[current_user]['reports'][title]
        source_report = self.users_report[current_user]['report_source']
        if not self.util.validate_dir(source_report):
            msg = 'No existe el directorio origen'
            self.util.msgbox(msg)
            return False, data
        if not self.util.validate_dir(source_report, 'r'):
            msg = 'No tienes derechos de lectura en el directorio origen'
            self.util.msgbox(msg)
            return False, data

        files = self.util.get_files(source_report)
        if not files:
            msg = 'No se encontraron archivos XML en el directorio origen'
            self.util.msgbox(msg)
            return False, data

        msg = 'Se va a generar el reporte de {} XMLs\n\n' \
            '¿Estas seguro de continuar?'
        if not self.util.question(msg.format(len(files))):
            return False, data

        data['title'] = title
        data['files'] = files
        data['fields_report'] = fields_report
        data['validate_fac'] = self._get('validate_fac')
        data['validate_sat'] = self._get('validate_sat')
        return True, data

    def button_exit_click(self):
        self.parent.quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
