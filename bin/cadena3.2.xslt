<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:cfdi="http://www.sat.gob.mx/cfd/3" xmlns:ecc="http://www.sat.gob.mx/ecc" xmlns:psgecfd="http://www.sat.gob.mx/psgecfd" xmlns:donat="http://www.sat.gob.mx/donat" xmlns:divisas="http://www.sat.gob.mx/divisas" xmlns:detallista="http://www.sat.gob.mx/detallista" xmlns:ecb="http://www.sat.gob.mx/ecb" xmlns:implocal="http://www.sat.gob.mx/implocal" xmlns:terceros="http://www.sat.gob.mx/terceros" xmlns:iedu="http://www.sat.gob.mx/iedu" xmlns:ventavehiculos="http://www.sat.gob.mx/ventavehiculos" xmlns:pfic="http://www.sat.gob.mx/pfic" xmlns:tpe="http://www.sat.gob.mx/TuristaPasajeroExtranjero" xmlns:leyendasFisc="http://www.sat.gob.mx/leyendasFiscales" xmlns:nomina="http://www.sat.gob.mx/nomina">
    <!-- Con el siguiente método se establece que la salida deberá ser en texto -->
    <!-- <xsl:output method="text" version="1.0" encoding="UTF-8" indent="no"/> -->
    <xsl:output method="text" version="1.0" encoding="UTF-8" indent="no"/>
    <!--
        En esta sección se define la inclusión de las plantillas de utilerías para colapsar espacios
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/2/cadenaoriginal_2_0/utilerias.xslt"/>
        En esta sección se define la inclusión de las demás plantillas de transformación para
        la generación de las cadenas originales de los complementos fiscales
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/ecc/ecc.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/psgecfd/psgecfd.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/donat/donat11.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/divisas/divisas.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/ecb/ecb.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/detallista/detallista.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/implocal/implocal.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/terceros/terceros11.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/iedu/iedu.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/ventavehiculos/ventavehiculos.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/pfic/pfic.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/TuristaPasajeroExtranjero/TuristaPasajeroExtranjero.xslt"/>
    <xsl:include href="http://www.sat.gob.mx/sitio_internet/cfd/leyendasFiscales/leyendasFisc.xslt"/>
    -->

    <!-- Manejador de datos requeridos -->
    <xsl:template name="Requerido">
        <xsl:param name="valor"/>|<xsl:call-template name="ManejaEspacios">
            <xsl:with-param name="s" select="$valor"/>
        </xsl:call-template>
    </xsl:template>

    <!-- Manejador de datos opcionales -->
    <xsl:template name="Opcional">
        <xsl:param name="valor"/>
        <xsl:if test="$valor">|<xsl:call-template name="ManejaEspacios"><xsl:with-param name="s" select="$valor"/></xsl:call-template></xsl:if>
    </xsl:template>

    <!-- Normalizador de espacios en blanco -->
    <xsl:template name="ManejaEspacios">
        <xsl:param name="s"/>
        <xsl:value-of select="normalize-space(string($s))"/>
    </xsl:template>

    <xsl:template match="donat:Donatarias">
        <!-- Iniciamos el tratamiento de los atributos de donat:Donatarias -->
        <xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@version"/></xsl:call-template>
        <xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@noAutorizacion"/></xsl:call-template>
        <xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@fechaAutorizacion"/></xsl:call-template>
        <xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@leyenda"/></xsl:call-template>
    </xsl:template>

  <!-- Manejador de nodos tipo nomina -->
  <xsl:template match="nomina:Nomina">
    <!--Iniciamos el tratamiento de los atributos de Nómina -->
    <xsl:choose>
      <xsl:when test="./@Version='1.0'">
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@Version" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@RegistroPatronal" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@NumEmpleado" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@CURP" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@TipoRegimen" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@NumSeguridadSocial" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@CLABE" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@Banco" />
        </xsl:call-template>
        <!--Iniciamos el tratamiento de los atributos de Ingresos -->
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./nomina:Ingresos/@TotalGravado" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./nomina:Ingresos/@TotalExento" />
        </xsl:call-template>
        <!--Iniciamos el tratamiento de los atributos de descuentos -->
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./nomina:Descuentos/@Total" />
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="./@Version='1.1'">
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@Version" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@RegistroPatronal" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@NumEmpleado" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@CURP" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@TipoRegimen" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@NumSeguridadSocial" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@FechaPago" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@FechaInicialPago" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@FechaFinalPago" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@NumDiasPagados" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@Departamento" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@CLABE" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@Banco" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@FechaInicioRelLaboral" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@Antiguedad" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@Puesto" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@TipoContrato" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@TipoJornada" />
        </xsl:call-template>
        <xsl:call-template name="Requerido">
          <xsl:with-param name="valor" select="./@PeriodicidadPago" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@SalarioBaseCotApor" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@RiesgoPuesto" />
        </xsl:call-template>
        <xsl:call-template name="Opcional">
          <xsl:with-param name="valor" select="./@SalarioDiarioIntegrado" />
        </xsl:call-template>
        <!--Iniciamos el tratamiento de los elementos de Nómina -->
        <xsl:if test="./nomina:Percepciones">
          <xsl:apply-templates select="./nomina:Percepciones" />
        </xsl:if>
        <xsl:if test="./nomina:Deducciones">
          <xsl:apply-templates select="./nomina:Deducciones" />
        </xsl:if>
        <xsl:for-each select="./nomina:Incapacidades">
          <xsl:apply-templates select="." />
        </xsl:for-each>
        <xsl:for-each select="./nomina:HorasExtras">
          <xsl:apply-templates select="." />
        </xsl:for-each>
      </xsl:when>
    </xsl:choose>
  </xsl:template>
  <xsl:template match="nomina:Percepciones">
    <!--Iniciamos el tratamiento de los atributos de Percepciones -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TotalGravado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TotalExento" />
    </xsl:call-template>
    <!--Iniciamos el tratamiento del los elementos de Percepciones-->
    <xsl:for-each select="./nomina:Percepcion">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="nomina:Percepcion">
    <!--Iniciamos el tratamiento de los atributos de Percepcion -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TipoPercepcion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@Clave" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@Concepto" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@ImporteGravado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@ImporteExento" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="nomina:Deducciones">
    <!--Iniciamos el tratamiento de los atributos de Deducciones -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TotalGravado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TotalExento" />
    </xsl:call-template>
    <!--Iniciamos el tratamiento del los elementos de Deducciones-->
    <xsl:for-each select="./nomina:Deduccion">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="nomina:Deduccion">
    <!--Iniciamos el tratamiento de los atributos de Deduccion -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TipoDeduccion" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@Clave" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@Concepto" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@ImporteGravado" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@ImporteExento" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="nomina:Incapacidades">
    <!--Iniciamos el tratamiento del los elementos de Incapacidades-->
    <xsl:for-each select="./nomina:Incapacidad">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="nomina:Incapacidad">
    <!--Iniciamos el tratamiento de los atributos de Incapacidad -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@DiasIncapacidad" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TipoIncapacidad" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@Descuento" />
    </xsl:call-template>
  </xsl:template>
  <xsl:template match="nomina:HorasExtras">
    <!--Iniciamos el tratamiento del los elementos de HorasExtras-->
    <xsl:for-each select="./nomina:HorasExtra">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="nomina:HorasExtra">
    <!--Iniciamos el tratamiento de los atributos de HorasExtra -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@Dias" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TipoHoras" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@HorasExtra" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@ImportePagado" />
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="implocal:ImpuestosLocales">
    <!--Iniciamos el tratamiento de los atributos de ImpuestosLocales -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@version" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TotaldeRetenciones" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@TotaldeTraslados" />
    </xsl:call-template>
    <xsl:for-each select="implocal:RetencionesLocales">
      <xsl:call-template name="Requerido">
        <xsl:with-param name="valor" select="./@ImpLocRetenido" />
      </xsl:call-template>
      <xsl:call-template name="Requerido">
        <xsl:with-param name="valor" select="./@TasadeRetencion" />
      </xsl:call-template>
      <xsl:call-template name="Requerido">
        <xsl:with-param name="valor" select="./@Importe" />
      </xsl:call-template>
    </xsl:for-each>
    <xsl:for-each select="implocal:TrasladosLocales">
      <xsl:call-template name="Requerido">
        <xsl:with-param name="valor" select="./@ImpLocTrasladado" />
      </xsl:call-template>
      <xsl:call-template name="Requerido">
        <xsl:with-param name="valor" select="./@TasadeTraslado" />
      </xsl:call-template>
      <xsl:call-template name="Requerido">
        <xsl:with-param name="valor" select="./@Importe" />
      </xsl:call-template>
    </xsl:for-each>
  </xsl:template>


  <xsl:template match="iedu:instEducativas">
    <!--Iniciamos el tratamiento de los atributos de instEducativas -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@version" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@nombreAlumno" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@CURP" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@nivelEducativo" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@autRVOE" />
    </xsl:call-template>
    <xsl:call-template name="Opcional">
      <xsl:with-param name="valor" select="./@rfcPago" />
    </xsl:call-template>
  </xsl:template>


  <xsl:template match="leyendasFisc:LeyendasFiscales">
    <!--Iniciamos el tratamiento de los atributos del complemento LeyendasFiscales -->
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@version" />
    </xsl:call-template>
    <!-- Manejo de los atributos de las leyendas Fiscales-->
    <xsl:for-each select="./leyendasFisc:Leyenda">
      <xsl:apply-templates select="." />
    </xsl:for-each>
  </xsl:template>
  <!-- Manejador de nodos tipo Información de las leyendas -->
  <xsl:template match="leyendasFisc:Leyenda">
    <!-- Manejo de los atributos de la leyenda -->
    <xsl:call-template name="Opcional">
      <xsl:with-param name="valor" select="./@disposicionFiscal" />
    </xsl:call-template>
    <xsl:call-template name="Opcional">
      <xsl:with-param name="valor" select="./@norma" />
    </xsl:call-template>
    <xsl:call-template name="Requerido">
      <xsl:with-param name="valor" select="./@textoLeyenda" />
    </xsl:call-template>
  </xsl:template>


    <!-- Aquí iniciamos el procesamiento de la cadena original con su | inicial y el terminador || -->
    <xsl:template match="/">|<xsl:apply-templates select="/cfdi:Comprobante"/>||</xsl:template>
    <!--  Aquí iniciamos el procesamiento de los datos incluidos en el comprobante -->
    <xsl:template match="cfdi:Comprobante">
        <!-- Iniciamos el tratamiento de los atributos de comprobante -->
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@version"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@fecha"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@tipoDeComprobante"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@formaDePago"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@condicionesDePago"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@subTotal"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@descuento"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@TipoCambio"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@Moneda"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@total"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@metodoDePago"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@LugarExpedicion"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@NumCtaPago"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@FolioFiscalOrig"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@SerieFolioFiscalOrig"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@FechaFolioFiscalOrig"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@MontoFolioFiscalOrig"/>
        </xsl:call-template>
        <!--
            Llamadas para procesar al los sub nodos del comprobante
        -->
        <xsl:apply-templates select="./cfdi:Emisor"/>
        <xsl:apply-templates select="./cfdi:Receptor"/>
        <xsl:apply-templates select="./cfdi:Conceptos"/>
        <xsl:apply-templates select="./cfdi:Impuestos"/>
        <xsl:apply-templates select="./cfdi:Complemento"/>
    </xsl:template>
    <!-- Manejador de nodos tipo Emisor -->
    <xsl:template match="cfdi:Emisor">
        <!-- Iniciamos el tratamiento de los atributos del Emisor -->
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@rfc"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@nombre"/>
        </xsl:call-template>
        <!--
            Llamadas para procesar al los sub nodos del comprobante
        -->
        <xsl:apply-templates select="./cfdi:DomicilioFiscal"/>
        <xsl:if test="./cfdi:ExpedidoEn">
            <xsl:call-template name="Domicilio">
                <xsl:with-param name="Nodo" select="./cfdi:ExpedidoEn"/>
            </xsl:call-template>
        </xsl:if>
        <xsl:for-each select="./cfdi:RegimenFiscal">
            <xsl:call-template name="Requerido">
                <xsl:with-param name="valor" select="./@Regimen"/>
            </xsl:call-template>
        </xsl:for-each>
    </xsl:template>
    <!-- Manejador de nodos tipo Receptor -->
    <xsl:template match="cfdi:Receptor">
        <!-- Iniciamos el tratamiento de los atributos del Receptor -->
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@rfc"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@nombre"/>
        </xsl:call-template>
        <!--
            Llamadas para procesar al los sub nodos del Receptor
        -->
        <xsl:if test="./cfdi:Domicilio">
            <xsl:call-template name="Domicilio">
                <xsl:with-param name="Nodo" select="./cfdi:Domicilio"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <!-- Manejador de nodos tipo Conceptos -->
    <xsl:template match="cfdi:Conceptos">
        <!-- Llamada para procesar los distintos nodos tipo Concepto -->
        <xsl:for-each select="./cfdi:Concepto">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
    </xsl:template>
    <!-- Manejador de nodos tipo Impuestos -->
    <xsl:template match="cfdi:Impuestos">
        <xsl:for-each select="./cfdi:Retenciones/cfdi:Retencion">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@totalImpuestosRetenidos"/>
        </xsl:call-template>
        <xsl:for-each select="./cfdi:Traslados/cfdi:Traslado">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@totalImpuestosTrasladados"/>
        </xsl:call-template>
    </xsl:template>
    <!-- Manejador de nodos tipo Retencion -->
    <xsl:template match="cfdi:Retencion">
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@impuesto"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@importe"/>
        </xsl:call-template>
    </xsl:template>
    <!-- Manejador de nodos tipo Traslado -->
    <xsl:template match="cfdi:Traslado">
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@impuesto"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@tasa"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@importe"/>
        </xsl:call-template>
    </xsl:template>
    <!-- Manejador de nodos tipo Complemento -->
    <xsl:template match="cfdi:Complemento">
        <xsl:for-each select="./*">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
    </xsl:template>
    <!--
        Manejador de nodos tipo Concepto
    -->
    <xsl:template match="cfdi:Concepto">
        <!-- Iniciamos el tratamiento de los atributos del Concepto -->
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@cantidad"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@unidad"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@noIdentificacion"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@descripcion"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@valorUnitario"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@importe"/>
        </xsl:call-template>
        <!--
            Manejo de los distintos sub nodos de información aduanera de forma indistinta
            a su grado de dependencia
        -->
        <xsl:for-each select=".//cfdi:InformacionAduanera">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
        <!-- Llamada al manejador de nodos de Cuenta Predial en caso de existir -->
        <xsl:if test="./cfdi:CuentaPredial">
            <xsl:apply-templates select="./cfdi:CuentaPredial"/>
        </xsl:if>
        <!-- Llamada al manejador de nodos de ComplementoConcepto en caso de existir -->
        <xsl:if test="./cfdi:ComplementoConcepto">
            <xsl:apply-templates select="./cfdi:ComplementoConcepto"/>
        </xsl:if>
    </xsl:template>
    <!-- Manejador de nodos tipo Información Aduanera -->
    <xsl:template match="cfdi:InformacionAduanera">
        <!-- Manejo de los atributos de la información aduanera -->
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@numero"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@fecha"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@aduana"/>
        </xsl:call-template>
    </xsl:template>
    <!-- Manejador de nodos tipo Información CuentaPredial -->
    <xsl:template match="cfdi:CuentaPredial">
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@numero"/>
        </xsl:call-template>
    </xsl:template>
    <!-- Manejador de nodos tipo ComplementoConcepto -->
    <xsl:template match="cfdi:ComplementoConcepto">
        <xsl:for-each select="./*">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
    </xsl:template>
    <!-- Manejador de nodos tipo Domicilio fiscal -->
    <xsl:template match="cfdi:DomicilioFiscal">
        <!-- Iniciamos el tratamiento de los atributos del Domicilio Fiscal -->
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@calle"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@noExterior"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@noInterior"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@colonia"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@localidad"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="./@referencia"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@municipio"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@estado"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@pais"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="./@codigoPostal"/>
        </xsl:call-template>
    </xsl:template>
    <!-- Manejador de nodos tipo Domicilio -->
    <xsl:template name="Domicilio">
        <xsl:param name="Nodo"/>
        <!-- Iniciamos el tratamiento de los atributos del Domicilio  -->
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@calle"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@noExterior"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@noInterior"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@colonia"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@localidad"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@referencia"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@municipio"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@estado"/>
        </xsl:call-template>
        <xsl:call-template name="Requerido">
            <xsl:with-param name="valor" select="$Nodo/@pais"/>
        </xsl:call-template>
        <xsl:call-template name="Opcional">
            <xsl:with-param name="valor" select="$Nodo/@codigoPostal"/>
        </xsl:call-template>
    </xsl:template>
</xsl:stylesheet>
