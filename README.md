## admin-cfdi ##
@pakage admin-cfdi<br/>
@author [Maurico Baeza](https://github.com/mauriciobaeza) <br/>
@date 04/12/2014<br/>
@version 0.2.2<br/>

Administrador de CFDIs / Proyecto de colaboración con [PythonCabal](http://wiki.cabal.mx/wiki/PythonCabal)

Pequeño sistema para administrar CFDIs, facturas electrónicas de México. Entre sus funcionalidades estan.

 - Descarga facturas del SAT, tanto emitidas como recibidas
 - Descarga facturas de correos electrónicos
 - Organiza las facturas en carpetas y las puede renombrar
 - Valida las facturas en el SAT y valida los sellos
 - Generar los PDF de las facturas
 - Reportea directamente de las facturas

## Requerimientos ##

- Python 3.4
- Tk si usas Linux, si usas Windows ya lo integra Python
- Firefox para la automatización de la descarga del SAT
- Selenium para la automatización de la descarga del SAT
- PyGubu para la interfaz gráfica.
- ReportLab si usas una plantilla JSON (por implementar, aunque podemos usar pyfpdf mucho más sencilla)
- LibreOffice si usas la plantilla ODS
- Extensiones win32 para Python si usas Windows

## Instalación ##

Si tienes instalado correctamente Python 3.4, puedes instalar con Pip
<pre><code>
sudo pip install selenium pygubu
</code></pre>

- Windows:
<pre><code>
pip install seleniumn pygubu
</code></pre>
Si usas Windows, asegúrate de abrir el script con el ejecutable pythonw.exe localizado en la carpeta de instalación de Python.

- ArchLinux:
<pre><code>
sudo pip install selenium pygubu
python admincfdi.py
</code></pre>

- Linux Mint:
<pre><code>
sudo apt-get install python3-pip python3-tk
sudo pip3 install selenium pygubu
python3 admincfdi.py
</code></pre>
