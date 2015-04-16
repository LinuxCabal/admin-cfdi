<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cfdi="http://www.sat.gob.mx/cfd/3" >

<xsl:output method = "text" encoding="UTF-8" />

<xsl:template match="/">-----BEGIN CERTIFICATE-----
<xsl:apply-templates select="/cfdi:Comprobante"/>
-----END CERTIFICATE-----</xsl:template>

<xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

<xsl:template match="cfdi:Comprobante">
<!--
      <xsl:value-of select="@certificado"/>
-->
      <xsl:value-of select="concat(substring(@certificado, 1, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 65, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 129, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 193, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 257, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 321, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 385, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 449, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 513, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 577, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 641, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 705, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 769, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 833, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 897, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 961, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 1025, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 1089, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 1153, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 1217, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 1281, 64), $newline)"/>
      <xsl:value-of select="concat(substring(@certificado, 1345, 64), $newline)"/>
      <xsl:value-of select="substring(@certificado, 1409, 64)"/>
      <xsl:if test="string-length(@certificado)>1473">
        <xsl:value-of select="$newline"/>
        <xsl:value-of select="substring(@certificado, 1473, 64)"/>
        <xsl:if test="string-length(@certificado)>1537">
            <xsl:value-of select="$newline"/>
            <xsl:value-of select="substring(@certificado, 1537, 64)"/>
            <xsl:if test="string-length(@certificado)>1601">
                <xsl:value-of select="$newline"/>
                <xsl:value-of select="substring(@certificado, 1601, 64)"/>
                <xsl:if test="string-length(@certificado)>1665">
                    <xsl:value-of select="$newline"/>
                    <xsl:value-of select="substring(@certificado, 1665, 64)"/>
                    <xsl:if test="string-length(@certificado)>1729">
                        <xsl:value-of select="$newline"/>
                        <xsl:value-of select="substring(@certificado, 1729, 64)"/>
                    </xsl:if>
                </xsl:if>
            </xsl:if>
        </xsl:if>
      </xsl:if>
</xsl:template>

</xsl:stylesheet>
