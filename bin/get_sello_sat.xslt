<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:cfdi="http://www.sat.gob.mx/cfd/3" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" version="1.0">

    <xsl:output method="text" version="1.0" encoding="UTF-8" indent="no"/>

    <xsl:template match="/"><xsl:apply-templates select="./cfdi:Comprobante"/></xsl:template>
    <xsl:template match="cfdi:Comprobante"><xsl:apply-templates select="./cfdi:Complemento"/></xsl:template>
    <xsl:template match="cfdi:Complemento"><xsl:apply-templates select="./tfd:TimbreFiscalDigital"/></xsl:template>
    <xsl:template match="tfd:TimbreFiscalDigital">
        <xsl:value-of select="@selloSAT"/>
    </xsl:template>

</xsl:stylesheet>