==========
Desarrollo
==========

Estructura
==========

La aplicación consta de los siguientes archivos:

- admincfdi.py Implementa la interfase gráfica y
  es la aplicación principal.

- values.py Tiene la clase Global que centraliza
  valores que se usan en los otros módulos.  Por
  ejemplo, las URLs y valores id de la página web
  de CFDIs del SAT están en el atributo SAT,
  es un diccionario que es usado
  en la descarga de CFDIs.

- pyutil.py Tiene varias clases que implementan
  utilerías usadas por los otros módulos.

Descarga de facturas del SAT
============================

La descarga de los archivos XML del sitio web del SAT se
maneja en la primera pestaña de la interfase gráfica.

Primeramente el usuario debe llenar
datos y/o seleccionar opciones en estos tres apartados:

- Datos de acceso
- Tipo de consulta
- Opciones de búsqueda

El proceso de la descarga se inicia mediante el botón
``Descargar``, el cual está ligado al método
:func:`admincfdi.Application.button_download_sat_click`
de la aplicación, que ejecuta
estos dos métodos:

- :func:`admincfdi.Application._validate_download_sat`

- :func:`admincfdi.Application._download_sat`

El proceso de descarga consiste en estos pasos:

#. Lanzar el navegador

#. Entrar a la página de búsquedas de CFDIs

     - Navegar a la página de login de CFDIs

     - Llenar el usuario y la contraseña (RFC y CIEC)

     - Enviar los datos al servidor

     - Navegar a la página de búsqueda de facturas emitidas,
       o a la de facturas recibidas

#. Solicitar la búsqueda

     - Seleccionar el tipo de búsqueda
     - Llenar los datos de la búsqueda
     - Enviar los datos al servidor

#. Descargar cada renglón de los resultados

     - Encontrar los elementos con atributo ``name``
       igual a *download*, corresponden al ícono
       de descarga a la izquierda en cada renglón.

     - Iterar en cada elemento de esta lista:

         - Concatenar la URL base
           de CFDIs con el valor del atributo ``onclick``
           del elemento
         - Hacer la solicitud GET a esta URL

#. Cerrar la sesión
#. Cerrar el navegador

En caso de alguna falla en los primeros cuatro pasos,
se intenta el 5, y por último y en todos los casos
se realiza el paso 6.

El avance del proceso se indica al usuario mediante
textos cortos que se muestran en una línea de estado
de la interfase gráfica, en esta secuencia::

    Abriendo Firefox...
    Conectando...
    Conectado...
    Buscando...
    Factura 1 de 12
    Factura 2 de 12
    Factura 3 de 12
    Factura 4 de 12
    Factura 5 de 12
    Factura 6 de 12
    Factura 7 de 12
    Factura 8 de 12
    Factura 9 de 12
    Factura 10 de 12
    Factura 11 de 12
    Factura 12 de 12
    Desconectando...
    Desconectado...

API
===
El módulo :mod:`admincfdi.pyutil` provee varias clases, las cuales
pueden ser usadas por las aplicaciones.  En las siguientes
secciones se explican y dan ejemplos de uso cada una de estas clases.


SAT
---

ValidCFDI
---------

Util
----

Mail
----

LibO
----

NumerosLetras
-------------

CFDIPDF
-------

DescargaSAT
-----------
Lleva a cabo al descarga de CFDIs del sitio del SAT.  Para descargar
un conjunto de CFDIs con ciertos criterios de búsqueda, se
utilizan los siguientes pasos:

#. Instanciar :class:`~admincfdi.pyutil.DescargaSAT`::

    descarga = DescargaSAT()

#. Crear un perfil de Firefox::

    profile = descarga.get_firefox_profile(carpeta_destino)

#. Conectar al sitio del SAT, lanzando Firefox::

    descarga.connect(profile, rfc=rfc, ciec=pwd)

#. Realizar una búsqueda, guardando la lista de resultados
   obtenida::

        docs = descarga.search(facturas_emitidas=facturas_emitidas,
                uuid=uuid,
                rfc_emisor=rfc_emisor,
                año=año,
                mes=mes,
                día=día,
                mes_completo_por_día=mes_completo_por_día)

#. Descargar los CFDIs::

        descarga.download(docs)

#. Desconectar la sesión del sitio del SAT y terminar
   Firefox::

        descarga.disconnect()

Los pasos 4. de búsqueda y 5. de descarga pueden repetirse, si
se desean descargar dos o más conjuntos de CFDIs con diferentes
criterios de búsqueda, manteniendo la sesión original abierta.

Como ejemplo, a continuación se muestra el uso de los
pasos en las aplicaciones ``admin-cfdi`` y ``descarga-cfdi``
que son parte del proyecto::

    descarga = DescargaSAT()
    profile = descarga.get_firefox_profile(args.carpeta_destino)
    try:
        descarga.connect(profile, rfc=rfc, ciec=pwd)
        docs = descarga.search(facturas_emitidas= args.facturas_emitidas,
                uuid=args.uuid,
                rfc_emisor=args.rfc_emisor,
                año=args.año,
                mes=args.mes,
                día=args.día,
                mes_completo_por_día=args.mes_completo_por_día)
        descarga.download(docs)
    except Exception as e:
        print (e)
    finally:
        descarga.disconnect()

Las cláusulas ``try/except/finally`` son para manejar alguna
excepción que ocurra en cualquiera de los pasos, y garantizar
que en cualquier caso se hace la desconexión de la sesión
y se termina Firefox.

CSVPDF
------
