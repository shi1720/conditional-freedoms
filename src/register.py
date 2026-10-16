"""Build the hand-curated source register and verify every transcription anchor.

Anchors are whitespace-normalized OCR strings, not diplomatic transcriptions.
Dates and page references refer to the printed editions, not file line numbers.
"""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROWS=[
('O1',1349,'White and Notestein 1915, p. 141','recruitment','free or bond','Status does not exempt a person from this recruitment clause.'),
('O2',1349,'White and Notestein 1915, p. 142','priority','retain no more than be necessary for them','Preference for lords is expressly limited; necessity is not numerically defined.'),
('O3',1349,'White and Notestein 1915, p. 142','custody','surety to serve','The stated custodial endpoint requires a service commitment.'),
('O4',1349,'White and Notestein 1915, p. 142','departure','without reasonable cause or license','Cause and licence qualify early departure; their adjudication is not specified here.'),
('O5',1349,'White and Notestein 1915, p. 142','receiving','presume to receive or to retain','The receiving employer is also exposed to a penalty.'),
('O6',1349,'White and Notestein 1915, pp. 142-143','wages','nor that any in other manner shall demand or receive the same','Recruitment, departure and wage limits have different objects.'),
('O7',1349,'White and Notestein 1915, pp. 143-144','craft','all other artificers and workmen','The craft exclusion in recruitment is not a blanket exclusion from wage regulation.'),
('O8',1349,'White and Notestein 1915, p. 145','subsistence','under the color of pity or alms','Almsgivers are addressed as a way of compelling labour.'),
('O9',1349,'White and Notestein 1915, p. 146','ecclesiastical','under the pain of suspension and interdict','The episcopal letter uses ecclesiastical sanctions for stipendiary chaplains.'),
('S1',1351,'White and Notestein 1915, p. 148','terms','a whole year, or by other usual terms','The edition preserves a qualification to annual service.'),
('S2',1351,'White and Notestein 1915, p. 149','oath','sworn two times in the year','Compliance is renewed by an oath before local officers.'),
('S3',1351,'White and Notestein 1915, p. 149','mobility','if he may serve in the same town','The summer mobility restriction contains a local-service condition.'),
('S4',1351,'White and Notestein 1915, p. 149','custom','and other places','The named origins do not constitute an explicitly closed list.'),
('S5',1351,'White and Notestein 1915, p. 149','return','and safely re-','The saving explicitly addresses a return leg as well as outward labour.'),
('S6',1351,'White and Notestein 1915, p. 151','custody','till they have found surety','Custody can secure future compliance; it is not a manumission formula.'),
('D1',1356,'White and Notestein 1915, p. 153; Putnam 1908, Appendix, p. 25','official_release','by their own authority, freed them','The commission singles out self-authorized release for privately appropriated receipts without statutory observance.'),
('D2',1356,'White and Notestein 1915, p. 154; Putnam 1908, Appendix, p. 25','royal_revenue','the amercements and other','The commission expressly reserves receipts due to the crown.'),
('C1',1358,'White and Notestein 1915, p. 156; Putnam 1908, Appendix, p. 152','presentment','took excessive wages, prices, and profits','A presentment accuses; it is not yet a verdict.'),
('C2',1358,'White and Notestein 1915, p. 156; Putnam 1908, Appendix, p. 153','appearance','did not come','Four named defendants do not appear on Friday; an arrest is ordered.'),
('C3',1358,'White and Notestein 1915, p. 157; Putnam 1908, Appendix, p. 154','custody','had been arrested and were in custody','Saturday custody is reported before the trial disposition.'),
('C4',1358,'White and Notestein 1915, p. 157; Putnam 1908, Appendix, p. 154','verdict','acquitted the said John Clegh','The jury acquits the four named defendants of the presented excesses and trespasses.'),
('C5',1358,'White and Notestein 1915, p. 157; Putnam 1908, Appendix, p. 154','discharge','Therefore let them go quit','Discharge follows this acquittal; a general employment exemption is not recorded.'),
]

def normalize(s): return re.sub(r'\s+',' ',s).strip()

def build():
    text=normalize((ROOT/'data'/'white_notestein_1915_ocr.txt').read_text())
    out=[]
    for ident,year,locator,action,anchor,interpretation in ROWS:
        # OCR can break words across lines, but do not silently repair a missing anchor.
        assert normalize(anchor) in text, (ident,anchor)
        out.append(dict(id=ident,year=year,locator=locator,action=action,
            anchor=anchor,interpretation=interpretation,edition='White and Notestein 1915',
            evidence_kind='edited normative text' if ident[0] in 'OSD' else 'edited proceeding',
            source_url='https://archive.org/details/sourceproblemsin00whit'))
    (ROOT/'data'/'source_units.json').write_text(json.dumps(out,indent=2)+'\n')
    sources=[]
    for file,url in [
      ('white_notestein_1915_ocr.txt','https://archive.org/download/sourceproblemsin00whit/sourceproblemsin00whit_djvu.txt'),
      ('putnam_1908_ocr.txt','https://archive.org/download/enforcementofsta00putnrich/enforcementofsta00putnrich_djvu.txt')]:
        b=(ROOT/'data'/file).read_bytes()
        sources.append(dict(file=file,url=url,access_date='2026-10-16',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),
            note='Historical edition in the public domain in the United States; OCR is not a facsimile.'))
    scans={
       'putnam_appendix_25.png':('https://archive.org/download/enforcementofsta00putnrich/enforcementofsta00putnrich.pdf',269,'Appendix, p. 25'),
       'putnam_appendix_154.png':('https://archive.org/download/enforcementofsta00putnrich/enforcementofsta00putnrich.pdf',398,'Appendix, p. 154'),
       'white_notestein_142.png':('https://archive.org/download/sourceproblemsin00whit/sourceproblemsin00whit.pdf',166,'p. 142'),
       'white_notestein_149.png':('https://archive.org/download/sourceproblemsin00whit/sourceproblemsin00whit.pdf',173,'p. 149')}
    for file,(url,page,locator) in scans.items():
        b=(ROOT/'data'/'scans'/file).read_bytes()
        sources.append(dict(file='scans/'+file,url=url,access_date='2026-10-16',sha256=hashlib.sha256(b).hexdigest(),
            bytes=len(b),pdf_page=page,printed_locator=locator,note='Single scan page rendered with pdftoppm, scale-to 1800; visually checked.'))
    (ROOT/'data'/'manifest.json').write_text(json.dumps(sources,indent=2)+'\n')
    print(f'{len(out)} anchors verified against the pinned edition OCR')

if __name__=='__main__':build()
