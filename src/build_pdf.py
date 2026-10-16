"""Produce the paper from editable text, verified result files and figure images."""
import json,re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,KeepTogether,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
ROOT=Path(__file__).resolve().parents[1]

def build():
    f=Path(matplotlib.get_data_path())/'fonts'/'ttf'
    for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),
                      ('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(f/file)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='PaperBody',fontName='Body',fontSize=10.3,leading=15.2,spaceAfter=8.2,
        alignment=TA_LEFT,splitLongWords=False,allowWidows=0,allowOrphans=0))
    styles.add(ParagraphStyle(name='PaperAbstract',parent=styles['PaperBody'],fontSize=9.4,leading=13.6,leftIndent=16,rightIndent=16))
    styles.add(ParagraphStyle(name='PaperTitle',fontName='BodyBold',fontSize=23,leading=28,spaceAfter=9))
    styles.add(ParagraphStyle(name='PaperSub',fontName='Body',fontSize=14.2,leading=19,spaceAfter=17))
    styles.add(ParagraphStyle(name='PaperHead',fontName='SansBold',fontSize=11.8,leading=16,spaceBefore=14,spaceAfter=9,keepWithNext=True))
    styles.add(ParagraphStyle(name='Caption',fontName='Sans',fontSize=8.3,leading=11.8,spaceAfter=11))
    styles.add(ParagraphStyle(name='Cell',fontName='Sans',fontSize=8.0,leading=11))
    styles.add(ParagraphStyle(name='Ref',fontName='Body',fontSize=9.1,leading=13.2,spaceAfter=9,leftIndent=13,firstLineIndent=-13,splitLongWords=True))
    story=[]
    def para(s,style='PaperBody'):
        s=escape(s)
        # Clickable bibliography links and data availability, with URL breaks.
        s=re.sub(r'(https://[^\s]+?)([.,]?(?:\s|$))',lambda m:'<link href="'+m[1].rstrip('.')+'" color="#235c80">'+m[1].rstrip('.')+'</link>'+m[2],s)
        return Paragraph(s,styles[style])
    def table(headers,rows,widths):
        t=Table([[para(str(x),'Cell') for x in headers]]+[[para(str(x),'Cell') for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e4ebf0')),
           ('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#27435b')),
           ('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#ccd2d8')),('TOPPADDING',(0,0),(-1,-1),7),
           ('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))
        return t
    text=(ROOT/'paper'/'manuscript.txt').read_text()
    text=re.sub(r'(?m)^(ABSTRACT|[1-9]\. [^\n]+|DATA AND CODE|REFERENCES|APPENDIX [AB]\. [^\n]+)\n(?!\n)',r'\1\n\n',text)
    blocks=text.strip().split('\n\n')
    front=blocks.pop(0).splitlines()
    story += [para(front[0].split(': ',1)[1],'PaperTitle'),para(front[1].split(': ',1)[1],'PaperSub'),
        para('Shivam Gupta | Independent Researcher','Caption'),para('shivam1720406@gmail.com | 16 October 2026','Caption'),Spacer(1,7)]
    abstract=False;refs=False
    for b in blocks:
        if b=='ABSTRACT':story.append(para('Abstract','PaperHead'));abstract=True;continue
        if b.startswith('KEYWORDS:'):
            abstract=False;story.append(para(b.replace('KEYWORDS:','Keywords:'),'Caption'));continue
        if b.startswith('[FIGURE'):
            num=int(b[7]); names={1:'scope',2:'cornwall',3:'release'}
            cap={1:'Figure 1. Three distinct objects of qualification. Sources: White and Notestein (1915), pp. 141-142, 149. Arrows connect a rule to its own qualifications, not stages of a universal career.',
                 2:'Figure 2. The Cornwall sequence, 1358. Source: Putnam (1908), Appendix, pp. 152-154; White and Notestein (1915), pp. 156-157. The branches are outcomes within one proceeding, not a population sample.',
                 3:'Figure 3. Release has a limited object. Normative rules, a commission directive, and a reported disposition are compared; their evidential status differs. Unknown service relations are not filled by inference.'}[num]
            im=Image(str(ROOT/'figures'/f'{names[num]}.png'));iw,ih=im.imageWidth,im.imageHeight;im.drawWidth=470;im.drawHeight=470*ih/iw
            story.append(KeepTogether([im,Spacer(1,7),para(cap,'Caption')]));continue
        if b=='[TABLE1]':
            rows=[['O1-O3, 1349','Recruitment and priority','Trade, craft, resources, land, existing service; bounded lordly preference','No blanket exclusion from other provisions'],
             ['O4-O5, 1349','Departure / receiving','Reasonable cause OR licence; agreed term','No automatic right to any new wage'],
             ['S3-S5, 1351','Seasonal movement','Local service at prescribed terms; customary August movement and return','No express general cancellation of an existing term'],
             ['O3 / S6','Custodial endpoint','Surety for service / compliance','Service obligation remains'],
             ['D1-D2, 1356','Official release','Authority, statutory observance, destination of receipts','An inquiry directive, not proof of conviction'],
             ['C1-C5, 1358','Presented accusation','Jury acquittal and discharge','No recorded general employment exemption']]
            story += [para('Table 1. Documentary distinctions retained in the reconstruction. Unit IDs refer to Appendix A.','Caption'),table(['Units','Object','Qualification or act','Boundary'],rows,[66,91,161,152]),Spacer(1,9)];continue
        if b=='[TABLE2]':
            results=json.loads((ROOT/'results'/'summary.json').read_text())
            names={'licence_only':'Omit reasonable cause','both_required':'Require cause AND licence','no_exception':'Omit both departure qualifications',
                'blanket_geographical_ban':'Replace mobility rule with blanket ban','omit_customary_saving':'Omit customary August saving'}
            story += [para('Table 2. Constructed reading mutations: disagreements with the declared reconstruction. Every domain contains eight equally enumerated logical assignments; none is a historical sample.','Caption'),
              table(['Mutation','Disagreements','Domain'],[[names[r['reading']],r['disagreements'],r['domain']] for r in results['mutations']],[310,90,70]),Spacer(1,9)];continue
        if b=='[REGISTER]':
            rows=json.loads((ROOT/'data'/'source_units.json').read_text())
            story += [table(['ID / date','Printed-edition locator','Interpretation retained'],[[r['id']+' / '+str(r['year']),r['locator'],r['interpretation']] for r in rows],[58,175,237]),Spacer(1,10)];continue
        if re.match(r'^\d+\. ',b) or b in ['DATA AND CODE','REFERENCES'] or b.startswith('APPENDIX '):
            abstract=False
            if b=='REFERENCES':refs=True;story.append(PageBreak())
            if b.startswith('APPENDIX A'):refs=False;story.append(PageBreak())
            story.append(para(b.title() if b in ['DATA AND CODE','REFERENCES'] else b,'PaperHead'));continue
        story.append(para(b,'Ref' if refs else ('PaperAbstract' if abstract else 'PaperBody')))
    out=ROOT/'paper'/'What_Did_Release_Release_Shivam_Gupta.pdf'
    doc=SimpleDocTemplate(str(out),pagesize=(595.276,841.89),leftMargin=62.5,rightMargin=62.5,
        topMargin=55,bottomMargin=57,title='What Did Release Release? Service, Surety, and Conditional Freedoms in England, 1349-1358',author='Shivam Gupta')
    def page(c,d):
        c.setStrokeColor(colors.HexColor('#c3cbd1'));c.setLineWidth(.35);c.line(62.5,44,532.7,44)
        c.setFont('Sans',7.2);c.setFillColor(colors.HexColor('#566672'))
        c.drawString(62.5,31,'GUPTA | WHAT DID RELEASE RELEASE?');c.drawRightString(532.7,31,str(d.page))
    doc.build(story,onFirstPage=page,onLaterPages=page)
    print(out)

if __name__=='__main__':build()
