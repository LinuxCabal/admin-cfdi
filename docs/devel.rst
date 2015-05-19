==========
Desarrollo
==========
Este capítulo contiene información útil para quienes desean
desarrollar aplicaciones que trabajen con CFDIs, para lo
cual pueden usar una o más de las clases disponibles dentro
del paquete `admincfdi`.


Estructura
==========

El paquete `admincfdi` incluye los siguientes módulos:

- `pyutil` Tiene varias clases que implementan
  las funcionalidades usadas por las aplicaciones.

- `values` Tiene la clase Global que centraliza
  valores que se usan en los otros módulos.  Por
  ejemplo, las URLs y valores id de la página web
  de CFDIs del SAT están en el atributo SAT,
  es un diccionario que es usado
  en la descarga de CFDIs.

admin-cfdi
==========

El botón ``Descargar`` está ligado al método
:func:`admin-cfdi.Application.button_download_sat_click`
de la aplicación, que ejecuta
estos dos métodos:

- :func:`admin-cfdi.Application._validate_download_sat`

- :func:`admin-cfdi.Application._download_sat`

Descarga de facturas del SAT
============================

El proceso de descarga mediante la aplicación de CFDIs
del SAT consiste en estos pasos:

#. Conectar
#. Buscar
#. Descargar
#. Desconectar

Los detalles de cada paso:

#. Conectar

     - Lanzar el navegador
     - Navegar a la página de login de CFDIs
     - Llenar el usuario y la contraseña (RFC y CIEC)
     - Enviar los datos al servidor
     - Esperar la respuesta
     - El título de la página cambia a *NetIQ Access Manager*
     - Hay un elemento iframe con id ``content``, el cual contiene:
        - En caso de éxito, el elemento con clase ``messagetext``
          con el texto *session has been authenticated*.
        - En caso de falla, un pop up con el elemento con id ``xacerror``
          que contiene el texto *Login failed*

#. Buscar

     - Navegar a la página de búsqueda de facturas emitidas,
       o a la de facturas recibidas
     - Esperar a que el título cambie a *Buscar CFDI*
     - Llenar los datos de la búsqueda
        - Si la búsqueda es por UUID, llenar el UUID en
          el input con id ``ctl00_MainContent_TxtUUID``.
        - Si la búsqueda es por fecha:
            - Hacer clic en el botón de radio a la izquierda
              de Fecha de Emisión con id
              ``ctl00_MainContent_RdoFechas``.
            - Esperar a que el input a la derecha de RFC Emisor
              con id ``ctl00_MainContent_TxtRfcReceptor``
              esté habilitado y se pueda hacer clic en él.
            - Si se buscan facturas emitidas:
                - Habilitar los inputs con id

                    - ``ctl00_MainContent_CldFechaInicial2_Calendario_text``
                    - ``ctl00_MainContent_CldFechaFinal2_Calendario_text``

                  y asignar valor de fecha inicial y fecha final de emisión
                  usando formato ``dd/mm/aaaa``
                - Asignar a los selects no visibles de tiempo final con ids

                    - ``ctl00_MainContent_CldFechaFinal2_DdlHora``
                    - ``ctl00_MainContent_CldFechaFinal2_DdlMinuto``
                    - ``ctl00_MainContent_CldFechaFinal2_DdlSegundo``

                  las cadenas 23, 59 y 59
            - Se se buscan facturas recibidas:
                - Asignar a los selects no visibles con ids

                    - ``DdlAnio``
                    - ``ctl00_MainContent_CldFecha_DdlMes``
                    - ``ctl00_MainContent_CldFecha_DdlDia``

                  los valores de los parámetros año, mes y día
     - Enviar los datos al servidor
     - Esperar a que no sea visible el elemento div de los
       resultados, o el botón mismo de enviar
     - Esperar a que uno de los dos div con id
       ``ctl00_MainContent_PnlResultados`` o id
       ``ctl00_MainContent_PnlNoResultados`` esté
       visible.
     - Si el div con id ``ctl00_MainContent_PnlResultados``
       es visible:

        - Esperar que un elemento con name ``BtnDescarga``
          se le pueda hacer clic
        - Encontrar la lista todos los elementos con name
          ``BtnDescarga``.  Son los íconos
          de descarga a la izquierda en cada renglón.

     - La lista de resultados está paginada en 500 elementos.
       Si los
       resultados son más de 500, una opción es dividir
       la búsqueda en dos o más búsquedas
       en las que se agregan criterios: La búsqueda de un
       mes se puede dividir en búsquedas por día; la
       búsqueda de un día puede dividirse en búsquedas en
       un rango de horas en ese día.



#. Descargar

     - Iterar en cada elemento de la lista
       de resultados:

         - Concatenar la URL base
           de CFDIs con el valor del atributo ``onclick``
           del elemento
         - Hacer la solicitud GET a esta URL

#. Desconectar
     - Cerrar la sesión
     - Cerrar el navegador. Este paso se realiza
       a pesar de que ocurra una falla en el paso
       anterior.

En caso de alguna falla en los primeros tres pasos,
la aplicación debe realizar el paso 4.


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
