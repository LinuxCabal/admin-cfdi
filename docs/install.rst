===========
Instalación
===========

Para instalar :term:`admin-cfdi` descarga la ultima versión de producción desde
`Github`_ e instala con el comando.

::

    sudo python setup.py install

Si lo prefieres usa un entorno virtual.

#. Para `LinuxMint`_

    * Crea el entorno virtual

    ::

        pyvenv-3.4 test_admin --without-pip

    * Activalo

    ::

        cd test_admin/
        source bin/activate

    * Instala pip

    ::

        wget https://bootstrap.pypa.io/get-pip.py
        python get-pip.py

    * Instala :term:`admin-cfdi`

    ::

        python setup.py install

#. Para `ArchLinux`_

    * Crea el entorno virtual

    ::

        pyvenv test_admin

    * Activalo

    ::

        cd test_admin/
        source bin/activate

    * Instala :term:`admin-cfdi`

    ::

        python setup.py install


.. _Github: https://github.com/LinuxCabal/admin-cfdi
.. _LinuxMint: http://linuxmint.com/
.. _ArchLinux: https://www.archlinux.org/
