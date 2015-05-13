===
Uso
===

Aplicaciones
------------
Admincfdi incluye las siguientes aplicaciones:

- `admin-cfdi`

- `descarga-cfdi`

- `cfdi2pdf`



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
