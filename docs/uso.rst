===
Uso
===

Aplicaciones
------------
Admincfdi incluye las siguientes aplicaciones:

- `admin-cfdi`

- `descarga-cfdi`

- `cfdi2pdf`

`admin-cfdi` es una aplicación gráfica, `descarga-cfdi`
y `cfdi2pdf` son aplicaciones de línea de comando.

admin-cfdi
==========

La descarga de los archivos XML del sitio web del SAT se
maneja en la primera pestaña de la interfase gráfica.

Primeramente el usuario debe llenar
datos y/o seleccionar opciones en estos tres apartados:

- Datos de acceso
- Tipo de consulta
- Opciones de búsqueda

El proceso de la descarga se inicia mediante el botón
``Descargar``.

descarga-cfdi
=============

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


Pruebas funcionales de descarga del SAT
---------------------------------------
Estas pruebas sirven para varios propósitos:

- Saber si el sitio del SAT esta funcionando
  normalmente,

- Saber si nuestra conexión entre la PC
  y el sito del SAT está funcionando y si
  su desempeño es el esperado,

- Saber si el sitio del SAT cambió su
  funcionamiento del tal forma que sea
  necesario actualizar la librería de
  descarga de admincfdi.

Las pruebas realizan descargas mediante
varios modos de búsqueda y validan
que la cantidad de archivos descargados
sea la esperada.  No requieren interacción
mientas corren.

Es necesario crear un archivo  de credenciales y un archivo de
configuración para las pruebas.  El archivo de configuración
especifica los criterios de cada búsqueda.  Este es un ejemplo::

    [uuid]
    uuid=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    expected=1

    [rfc_emisor]
    rfc_emisor=XXXXXXXXXXXX
    año=2014
    mes=09
    día=26
    expected=1

    [año_mes_día]
    año=2014
    mes=09
    día=26
    expected=1

    [mes_completo_por_día]
    año=2014
    mes=09
    expected=5

Se necesitan estas cuatro secciones.  Hay que ajustar los
valores para que la cantidad de CFDIs no sea muy grande.  La
variable ``expected`` se ajusta a la cantidad de CFDIs que se
descargan, para las credenciales que se utilicen.

Para ejecutar::

    python functional_DescargaSAT.py
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 254.376s

Agregar el parámetro ``-v`` para tener un renglón por
cada prueba que se ejecuta::

    python functional_DescargaSAT.py -v
    test_año_mes_día (__main__.DescargaSAT) ... ok
    test_mes_completo (__main__.DescargaSAT) ... ok
    test_rfc (__main__.DescargaSAT) ... ok
    test_uuid (__main__.DescargaSAT) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 254.376s
