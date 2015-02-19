# admin-cfdi
Administrador de CFDIs / Proyecto de colaboración con PythonCabal

Pequeño sistema para administrar CFDIs, facturas electrónicas de México. Entre sus funcionalidades estan.

 - Descarga facturas del SAT, tanto emitidas como recibidas
 - Descarga facturas de correos electrónicos
 - Organiza las facturas en carpetas y las puede renombrar
 - Valida las facturas en el SAT y valida los sellos
 - Generar los PDF de las facturas
 - Reportea directamente de las facturas

## Requerimientos:

- Python 3.2+
- Tk si usas Linux, si usas Windows ya lo integra Python
- Firefox para la automatización de la descarga del SAT
- Selenium para la automatización de la descarga del SAT
- PyGubu para la interfaz gráfica.
- ReportLab si usas una plantilla JSON (por implementar, aunque podemos usar pyfpdf mucho más sencilla)
- LibreOffice si usas la plantilla ODS
- Extensiones win32 para Python si usas Windows
