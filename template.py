import datetime
import os
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        #~ kwargs['bottomup'] = 0
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(20.59 * cm, 1 * cm,
            'Página {} de {}'.format(self._pageNumber, page_count))


class ReportTemplate(BaseDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        # letter 21.6 x 27.9
        kwargs['pagesize'] = letter
        kwargs['rightMargin'] = 1 * cm
        kwargs['leftMargin'] = 1 * cm
        kwargs['topMargin'] = 4 * cm
        kwargs['bottomMargin'] = 2 * cm
        BaseDocTemplate.__init__(self, *args, **kwargs)
        self.styles = getSampleStyleSheet()
        self.header = {}
        self.data = []

    def afterPage(self):
        """Called after each page has been processed"""
        self.canv.saveState()
        date = datetime.datetime.today().strftime('%A, %d de %B del %Y')
        self.canv.setStrokeColorRGB(0, 0, 0.5)
        self.canv.setFont("Helvetica", 8)
        self.canv.drawRightString(20.59 * cm, 26.9 * cm, date)
        self.canv.line(1 * cm, 26.4 * cm, 20.6 * cm, 26.4 * cm)

        path_cur = os.path.dirname(os.path.realpath(__file__))
        path_img = os.path.join(path_cur, 'logo.png')
        try:
            self.canv.drawImage(path_img, 1.5 * cm, 24.2 * cm, 2.5 * cm, 2 * cm)
        except:
            pass

        self.canv.roundRect(
            5 * cm, 25.4 * cm, 15.5 * cm, 0.6 * cm, 0.15 * cm,
            stroke=True, fill=False)
        self.canv.setFont('Helvetica-BoldOblique', 10)
        self.canv.drawCentredString(12.75 * cm, 25.6 * cm, self.header['emisor'])

        self.canv.roundRect(
            5 * cm, 24.4 * cm, 15.5 * cm, 0.6 * cm, 0.15 * cm,
            stroke=True, fill=False)
        self.canv.setFont('Helvetica-BoldOblique', 9)
        self.canv.drawCentredString(12.75 * cm, 24.6 * cm, self.header['title'])

        self.canv.line(1 * cm, 1.5 * cm, 20.6 * cm, 1.5 * cm)
        self.canv.restoreState()
        return

    def set_data(self, data):
        self.header['emisor'] = data['emisor']
        self.header['title'] = data['title']
        cols = len(data['rows'][0])
        widths = []
        for w in data['widths']:
            widths.append(float(w) * cm)
        t_styles = [
            ('GRID', (0, 0), (-1, -1), 0.25, colors.darkblue),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOX', (0, 0), (-1, 0), 1, colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ]
        if cols == 6:
            t_styles += [
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('ALIGN', (3, 1), (3, -1), 'CENTER'),
                ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ]
        elif cols == 3:
            t_styles += [
                ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (-2, 0), (-2, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ]
        elif cols == 2:
            t_styles += [
                ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ]
        rows = []
        for i, r in enumerate(data['rows']):
            n = i + 1
            rows.append(('{}.-'.format(n),) + r)
            if cols == 6:
                if r[4] == 'Cancelado':
                    t_styles += [
                        ('GRID', (0, n), (-1, n), 0.25, colors.red),
                        ('TEXTCOLOR', (0, n), (-1, n), colors.red),
                    ]
        rows.insert(0, data['titles'])
        t = Table(rows, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle(t_styles))

        text = 'Total este reporte = $ {}'.format(data['total'])
        ps = ParagraphStyle(
            name='Total',
            fontSize=12,
            fontName='Helvetica-BoldOblique',
            textColor=colors.darkblue,
            spaceBefore=0.5 * cm,
            spaceAfter=0.5 * cm)
        p1 = Paragraph(text, ps)
        text = 'Nota: esta suma no incluye documentos cancelados'
        ps = ParagraphStyle(
            name='Note',
            fontSize=7,
            fontName='Helvetica-BoldOblique')
        p2 = Paragraph(text, ps)
        self.data = [t, p1, p2]
        return

    def make_pdf(self):
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id='normal')
        template = PageTemplate(id='report', frames=frame)
        self.addPageTemplates([template])
        self.build(self.data, canvasmaker=NumberedCanvas)
        return


if __name__ == "__main__":
    doc = ReportTemplate('filename.pdf')
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    data = []
    for i in range(100):
        data.append(Paragraph("This is line %d." % i, styleN))
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='report', frames=frame)
    doc.addPageTemplates([template])
    # Build your doc with your elements and go grab a beer
    doc.build(data, canvasmaker=NumberedCanvas)

