from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[1]
INK='#18324a'; BLUE='#e8eff5'; GOLD='#a06b30'; PALE='#f5f1e9'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42})

def box(ax,x,y,w,h,text,face=BLUE,size=10):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.014',
        linewidth=.9,edgecolor=INK,facecolor=face))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,color=INK,linespacing=1.5)

def save(fig,name):
    fig.savefig(ROOT/'figures'/f'{name}.pdf',bbox_inches='tight',facecolor='white')
    fig.savefig(ROOT/'figures'/f'{name}.png',dpi=220,bbox_inches='tight',facecolor='white')
    plt.close(fig)

def make():
    fig,ax=plt.subplots(figsize=(8,3.35));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    labels=[('Recruitment\n1349, O1','Age, ability, livelihood;\ncraft, resources, land;\nexisting service, demand'),
            ('Departure during a term\n1349, O4','Reasonable cause\nOR licence'),
            ('Seasonal movement\n1351, S3-S5','Local service condition;\nAugust customary saving')]
    for i,(title,detail) in enumerate(labels):
        x=.02+i*.33
        box(ax,x,.60,.29,.30,title)
        box(ax,x,.18,.29,.30,detail,PALE,9)
        ax.annotate('',xy=(x+.145,.49),xytext=(x+.145,.59),arrowprops={'arrowstyle':'->','color':INK})
    ax.text(.5,.045,'An exception changes its own relation; further legal effects require further evidence.',ha='center',fontsize=9,color=INK)
    save(fig,'scope')

    fig,ax=plt.subplots(figsize=(8,3.9));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    box(ax,.02,.61,.26,.27,'Thursday\nPresentment; attachment\nfor Friday at Penryn',size=9)
    box(ax,.37,.61,.26,.27,'Friday\nFour do not appear;\narrest ordered',size=9)
    box(ax,.72,.61,.26,.27,'Saturday\nCustody; denial;\njury trial at Helston',size=9)
    for x in (.29,.64):ax.annotate('',xy=(x+.07,.745),xytext=(x,.745),arrowprops={'arrowstyle':'->','color':INK})
    box(ax,.16,.10,.39,.27,'Clegh, Karn, Trethak, Tremenhir\nAcquitted; directed to depart quit',PALE,9)
    box(ax,.62,.10,.35,.27,'Other named associates\nFound guilty; make fine',PALE,9)
    for x in (.35,.79):
        ax.annotate('',xy=(x,.38),xytext=(.85,.59),arrowprops={'arrowstyle':'->','color':INK,'connectionstyle':'arc3,rad=.1'})
    ax.text(.02,.96,'One edited proceeding, 1358; the record supplies no reason for the acquittal.',fontsize=9,color=INK)
    save(fig,'cornwall')

    fig,ax=plt.subplots(figsize=(8,3.3));ax.axis('off')
    data=[['Release on service surety\nO3 / S6','Ends','Preserved / secured','Not acquitted'],
          ['Acquittal and discharge\nC4-C5','Ends','Not established\nby this disposition','Acquitted of\npresented charge'],
          ['Official release under inquiry\nD1','Release alleged','Not established\nby this commission','No verdict supplied']]
    tab=ax.table(cellText=data,colLabels=['Event / evidence','Custody','Service commitment','Accusation'],
        cellLoc='left',colLoc='left',colWidths=[.34,.13,.27,.26],bbox=[0,.12,1,.84])
    tab.auto_set_font_size(False);tab.set_fontsize(9)
    for (r,c),cell in tab.get_celld().items():
        cell.set_edgecolor('white');cell.PAD=.12
        cell.set_facecolor(INK if r==0 else (BLUE if r%2 else PALE))
        cell.get_text().set_color('white' if r==0 else INK)
    ax.text(0,.015,'Equal changes in custody need not have equal effects on obligation or accusation.',fontsize=9,color=INK)
    save(fig,'release')

if __name__=='__main__':make()
