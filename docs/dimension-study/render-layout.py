"""Render orthographic study sheets from explicit millimetre coordinates.
Not a fabricated CAD model or a source of approved manufacturing dimensions.
Run: MPLCONFIGDIR=/tmp/mpl-dimension python docs/dimension-study/render-layout.py
"""
from pathlib import Path
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Circle,Arc,FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties, fontManager

ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'layout-v04.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
fontManager.addfont('/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf')
TH=FontProperties(family=['DejaVu Sans','Noto Sans Thai'])
BLACK='#20262e';RED='#bd262f';BLUE='#176385';GREY='#77838e';LIGHT='#e5e9ed';BG='#fafbfc'
SX,SZ=D['seat_S']['x'],D['seat_S']['z'];WX,WZ=D['steering_W']['x'],D['steering_W']['z'];PX=D['pedal_B']['x']
REAR,FRONT=D['body']['rear_x'],D['body']['front_x']

def text(ax,x,y,s,**kw):return ax.text(x,y,s,**kw)
def label(ax,x,y,s,color=BLACK,ha='center',size=10,rotation=0):
    return text(ax,x,y,s,color=color,ha=ha,va='center',fontsize=size,rotation=rotation,
                bbox=dict(facecolor=BG,edgecolor='none',alpha=.96,pad=2),zorder=15)
def hdim(ax,x1,x2,y,label_text,base1=None,base2=None,color=RED):
    for x,b in ((x1,base1),(x2,base2)):
        if b is not None:ax.plot([x,x],[b,y],color=GREY,lw=.7,ls=(0,(3,2)),zorder=8)
    ax.annotate('',(x2,y),(x1,y),arrowprops=dict(arrowstyle='<->',color=color,lw=1.2),zorder=12)
    label(ax,(x1+x2)/2,y+24,label_text,color=color)
def vdim(ax,x,y1,y2,label_text,base1=None,base2=None,color=RED):
    for y,b in ((y1,base1),(y2,base2)):
        if b is not None:ax.plot([b,x],[y,y],color=GREY,lw=.7,ls=(0,(3,2)),zorder=8)
    ax.annotate('',(x,y2),(x,y1),arrowprops=dict(arrowstyle='<->',color=color,lw=1.2),zorder=12)
    label(ax,x-23,(y1+y2)/2,label_text,color=color,rotation=90)
def point(ax,x,y,name,dx=18,dy=22):
    ax.plot(x,y,'+',ms=13,mew=2,color=BLUE,zorder=20)
    label(ax,x+dx,y+dy,name,color=BLUE,ha='left',size=11)
def arrow_note(ax,xy,xytext,note,color=GREY):
    ax.annotate(note,xy=xy,xytext=xytext,color=color,fontsize=9,ha='left',va='center',
        bbox=dict(facecolor=BG,edgecolor='none',pad=2),arrowprops=dict(arrowstyle='-',color=color,lw=.9),zorder=16)
def header(fig,title,thai):
    fig.text(.055,.952,title,fontsize=22,weight='bold',color=BLACK)
    fig.text(.055,.916,thai,fontproperties=TH,fontsize=12,color=BLUE)
    fig.text(.945,.949,'v04.1  /  21 OCT 2026',ha='right',fontsize=11,color=GREY)
    fig.text(.945,.92,'ALL NUMBERS mm  |  ORTHOGRAPHIC STUDY',ha='right',fontsize=10,color=GREY)
def footer(fig):
    fig.text(.055,.035,'ขนาดเสนอเพื่อทดลองท่านั่งและวางแบบ — ยังไม่ใช่แบบตัดท่อ/เจาะรู/อนุมัติผลิต',fontproperties=TH,fontsize=12,color=RED)
    fig.text(.055,.013,'S = seat-surface datum at mid rail; not anatomical H-point. Do not scale a print. GM5 interface / ground height: TO BE MEASURED.',fontsize=9,color=GREY)
def save(fig,name,pdf):
    fig.savefig(ROOT/f'{name}.png',dpi=180,facecolor=BG)
    fig.savefig(ROOT/f'{name}.svg',facecolor=BG)
    p=ROOT/f'{name}.svg';p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n')
    pdf.savefig(fig,facecolor=BG)
def strip(ax,center,width,y,label_text,range_text):
    ax.plot([center-width/2-50,center+width/2+50],[y,y],color=GREY,lw=5)
    ax.plot([center-width/2,center-width/2],[y-13,y+13],color=BLUE,lw=2)
    ax.plot([center+width/2,center+width/2],[y-13,y+13],color=BLUE,lw=2)
    hdim(ax,center-width/2,center+width/2,y-35,label_text,color=BLUE)
    label(ax,center,y+65,range_text,color=BLACK,size=10)

with PdfPages(ROOT/'kart-dimension-study-v04.pdf') as pdf:
    # Sheet 1: true X/Z orthographic geometry, all main dimensions share S.
    fig=plt.figure(figsize=(16.54,11.69),facecolor=BG)
    header(fig,'01  SIDE VIEW / SEATING DIMENSIONS','มุมด้านข้าง: วัดระยะจากจุด S เดียวกัน • ด้านหน้ารถไปทางขวา')
    ax=fig.add_axes([.055,.31,.89,.57],facecolor=BG)
    ax.set_xlim(-680,1580);ax.set_ylim(-260,1060);ax.set_aspect('equal');ax.axis('off')
    # The cockpit floor is a local datum, intentionally no room-ground line.
    ax.plot([REAR-40,FRONT+170],[0,0],color=BLUE,lw=1.2,ls=(0,(7,3)))
    label(ax,FRONT+100,-32,'Z = 0',color=BLUE,size=10)
    for x,rad in [(D['axles']['rear_x'],D['tyres']['rear_diameter']/2),(D['axles']['front_x'],D['tyres']['front_diameter']/2)]:
        ax.add_patch(Circle((x,60),rad,facecolor='#c7ccd1',edgecolor=BLACK,lw=2,zorder=2))
        ax.add_patch(Circle((x,60),rad*.52,facecolor=BG,edgecolor=GREY,lw=2,zorder=3))
        ax.plot([x,x],[60-rad-15,60+rad+15],color=GREY,lw=.7,ls=':')
    ax.plot([REAR,FRONT],[-35,-35],color=BLACK,lw=8,zorder=4)
    ax.add_patch(Polygon([(REAR,10),(REAR+120,70),(REAR+270,70),(REAR+270,0)],facecolor=BLACK,zorder=5))
    ax.add_patch(Polygon([(500,0),(1100,0),(1100,100),(590,110)],facecolor=BLACK,zorder=4))
    ax.add_patch(Polygon([(650,15),(1050,15),(1050,75),(810,85)],facecolor=RED,zorder=5))
    ax.add_patch(Polygon([(1130,0),(1250,0),(1250,60),(1160,85)],facecolor=RED,zorder=5))
    ax.plot([-185,0,235],[120+185*math.tan(math.radians(60)),120,105],color=BLACK,lw=9,solid_capstyle='round',zorder=7)
    ax.plot([-185,-35],[120+185*math.tan(math.radians(60)),180],color=RED,lw=3,zorder=8)
    ax.plot([-130,210],[52,52],color=GREY,lw=7,zorder=6)
    ax.plot([-100,-100,180,180],[52,12,12,52],color=BLACK,lw=2,zorder=5)
    # Steering wheel projection: full diameter represented in its inclined plane.
    half=D['steering_W']['rim_diameter']/2
    dx=half*math.cos(math.radians(60));dz=half*math.sin(math.radians(60))
    ax.plot([WX-dx,WX+dx],[WZ-dz,WZ+dz],color=BLACK,lw=8,solid_capstyle='round',zorder=8)
    ax.plot([WX,540,590],[WZ,300,0],color=BLACK,lw=5,zorder=6)
    ax.plot([WX+15,WX+65],[WZ-25,WZ-60],color=GREY,lw=13,zorder=7)
    ax.plot([860,930],[20,160],color=BLACK,lw=7,zorder=7)
    ax.plot([785,1000],[10,10],color=GREY,lw=6,zorder=6)
    # Display position is illustrative, no mounting/height dimension is implied.
    mx=D['monitors']['centre_plane_x_example'];mz=D['monitors']['bottom_z_example']
    ax.add_patch(Rectangle((mx-7,mz),14,365,fc='#d7e0e5',ec=GREY,lw=1.5,zorder=3))
    ax.plot([mx+5,mx+95,mx+95],[mz+80,mz+35,50],color=GREY,lw=3,zorder=3)
    arrow_note(ax,(mx+8,mz+200),(870,930),'Screen location / eye distance: TBD')
    ax.plot([0,0],[-10,890],color=BLUE,lw=.7,ls=':')
    point(ax,SX,SZ,'S');point(ax,WX,WZ,'W',dx=22,dy=0);point(ax,PX,100,'B / T',dx=20,dy=45)
    hdim(ax,SX,WX,705,'B1  S → W = 400',SZ,WZ)
    hdim(ax,SX,PX,820,'B2  S → PEDALS = 900',SZ,100)
    hdim(ax,WX,PX,590,'B3  W → PEDALS = 500',WZ,100,color=BLUE)
    vdim(ax,-450,0,SZ,'B4  120',base1=-350,base2=0)
    vdim(ax,1185,SZ,WZ,'B5  300',base1=SX,base2=WX)
    ax.add_patch(Arc((SX,SZ),260,260,theta1=120,theta2=180,ec=RED,lw=1.4,zorder=12))
    ax.plot([-160,0],[SZ,SZ],color=GREY,lw=.8,ls=':')
    label(ax,-245,260,'B6  60°',color=RED)
    arrow_note(ax,(mx,mz),(1000,700),'27 in screen housing\n615 W × 365 H')
    hdim(ax,REAR,FRONT,-200,'A1  BODY LENGTH = 1800',-35,-35)
    # Notes and adjustment strips occupy separate, uncluttered lower band.
    fig.text(.065,.27,'จุดอ้างอิง',fontproperties=TH,fontsize=14,color=BLUE)
    fig.text(.065,.242,'S: จุดรองก้นชิดพนัก บนแนวกึ่งกลางเบาะ เมื่อรางอยู่ตำแหน่งกลาง',fontproperties=TH,fontsize=11,color=BLACK)
    fig.text(.065,.217,'W: ศูนย์กลางวงพวงมาลัย  |  B/T: จุดสัมผัสเบรก/คันเร่ง  |  Z=0: พื้นบน cockpit ไม่ใช่พื้นห้อง',fontproperties=TH,fontsize=11,color=BLACK)
    adj=fig.add_axes([.06,.075,.88,.12],facecolor=BG);adj.set_xlim(-100,1800);adj.set_ylim(-70,120);adj.axis('off')
    strip(adj,180,230,35,'C1  230 TOTAL','SEAT: ±115 from mid rail')
    strip(adj,770,150,35,'C2  150 TOTAL','PEDALS: ±75 from mid carrier')
    strip(adj,1360,100,35,'C3  100 TOTAL','WHEEL: ±50 X / ±50 Z')
    fig.text(.065,.061,'ช่วงเลื่อนเป็นข้อเสนอของกลไก ต้องลองท่านั่งและตรวจการชนก่อนใช้ร่วมกันทุกตำแหน่ง',fontproperties=TH,fontsize=10,color=GREY)
    footer(fig);save(fig,'01-side-dimensions',pdf);plt.close(fig)

    # Sheet 2: true X/Y plan. Body / monitors / mounting scopes distinguished.
    fig=plt.figure(figsize=(16.54,11.69),facecolor=BG)
    header(fig,'02  TOP VIEW / WIDTH & CENTRELINES','มุมด้านบน: ด้านหน้ารถไปทางขวา • เส้นกึ่งกลางรถ Y=0 • เบรกซ้าย / คันเร่งขวา')
    ax=fig.add_axes([.055,.2,.89,.68],facecolor=BG)
    ax.set_xlim(-760,1580);ax.set_ylim(-940,1030);ax.set_aspect('equal');ax.axis('off')
    ax.add_patch(Rectangle((REAR,-650),FRONT-REAR,1300,fc='none',ec=GREY,lw=1,ls=(0,(4,3)),zorder=1))
    # Chassis only; exact bend radii / weld / crossmember locations deliberately not dimensioned.
    contour=[(-420,-330),(-470,-250),(-470,250),(-420,330),(1030,330),(1130,220),(1130,-220),(1030,-330),(-420,-330)]
    ax.plot(*zip(*contour),color=BLACK,lw=6,zorder=3)
    for x in (-100,300,750):ax.plot([x,x],[-330,330],color=GREY,lw=3,zorder=2)
    for side in (-1,1):
        ax.add_patch(Rectangle((260,side*440-55),660,110,fc=BLACK,ec=BLACK,zorder=2))
        ax.add_patch(Polygon([(400,side*430),(880,side*430),(880,side*470),(560,side*470)],fc=RED,zorder=3))
    # Body bumper extents at exact total-length endpoints.
    ax.add_patch(Rectangle((REAR,-350),65,700,fc=BLACK,zorder=3))
    ax.add_patch(Rectangle((FRONT-95,-410),95,820,fc=BLACK,zorder=3))
    ax.add_patch(Rectangle((FRONT-95,-410),32,820,fc=RED,zorder=4))
    for kind in ('rear','front'):
        x=D['axles'][kind+'_x'];diam=D['tyres'][kind+'_diameter'];width=D['tyres'][kind+'_width'];yc=D['tyres'][kind+'_y_abs']
        ax.plot([x,x],[-690,690],color=GREY,lw=.8,ls=(0,(5,3)),zorder=1)
        for side in (-1,1):
            y=side*yc
            ax.add_patch(Rectangle((x-diam/2,y-width/2),diam,width,fc=BLACK,ec=GREY,lw=1.5,zorder=4))
            ax.plot([x-diam*.36,x+diam*.36],[y,y],color='#58616b',lw=2,zorder=5)
    # Max shell width example =500, installation bay =540, both explicitly nominal.
    shell=[(-205,-210),(-190,-250),(185,-250),(260,-210),(240,210),(185,250),(-190,250),(-205,210)]
    ax.add_patch(Polygon(shell,fc=BLACK,ec=BLACK,lw=2,zorder=5))
    ax.plot([-190,-190],[-210,210],color=RED,lw=5,zorder=6)
    ax.add_patch(Rectangle((-180,-270),500,540,fc='none',ec=BLUE,lw=1,ls=(0,(4,3)),zorder=5))
    # Wheel plane orthographic plan: circle projects to ellipse; simple horizontal grip span shown.
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((WX,0),155,310,fc='none',ec=BLACK,lw=5,zorder=5))
    ax.plot([WX-12,WX+12],[-95,95],color=GREY,lw=3,zorder=5)
    ax.add_patch(Rectangle((WX+30,-55),130,110,fc=BLACK,zorder=4))
    for key,name in [('pedal_B','B'),('pedal_T','T')]:
        x=D[key]['x'];y=D[key]['y']
        ax.add_patch(Rectangle((x-45,y-40),90,80,fc=BLACK,ec=GREY,lw=1.5,zorder=5))
        point(ax,x,y,name,dx=55,dy=10)
    ax.add_patch(Rectangle((PX-100,-260),200,520,fc='none',ec=GREY,lw=1,zorder=3))
    # Displays are ghosted to keep dimensions legible; exact housing projection from width/angle.
    h=D['monitors']['housing_width_example'];theta=math.radians(D['monitors']['side_angle_deg_example']);mx=D['monitors']['centre_plane_x_example']
    ax.plot([mx,mx],[-h/2,h/2],color='#a2afb8',lw=7,alpha=.55,zorder=2)
    for side in (-1,1):
        ax.plot([mx,mx-h*math.sin(theta)],[side*h/2,side*(h/2+h*math.cos(theta))],color='#a2afb8',lw=7,alpha=.55,zorder=2)
    ax.plot([REAR-20,FRONT+30],[0,0],color=BLUE,lw=.8,ls=(0,(9,3)),zorder=8)
    point(ax,SX,0,'S',dx=0,dy=-55);point(ax,WX,0,'W',dx=-15,dy=-80)
    label(ax,-440,45,'Y = 0',color=BLUE,size=9)
    hdim(ax,REAR,FRONT,920,'A1  BODY LENGTH = 1800',650,650)
    vdim(ax,-660,-650,650,'A2  BODY WIDTH = 1300',base1=REAR,base2=REAR)
    hdim(ax,D['axles']['rear_x'],D['axles']['front_x'],-790,'A3  WHEELBASE = 1045',-650,-650)
    vdim(ax,1420,-180,180,'D1  PEDAL C/C = 360',base1=PX,base2=PX)
    vdim(ax,80,-270,270,'D2  BAY = 540',base1=-180,base2=-180,color=BLUE)
    arrow_note(ax,(190,703),(760,750),'Ghosted screens: 3 × 27 in\nPosition / eye distance / support: TBD')
    arrow_note(ax,(185,250),(-380,600),'Seat-shell width example: 500\nMeasure actual shell + cradle')
    # No GM5 circles with invented coordinate dimensions: list as unmeasured instead.
    arrow_note(ax,(1050,-330),(970,-680),'GM5 mounting:\nXYZ + holes TBD')
    ax.text(-450,-560,'REAR',color=GREY,fontsize=10)
    ax.text(1270,-560,'FRONT →',color=GREY,fontsize=10)
    fig.text(.065,.153,'เส้นรอบนอก A1/A2 = ตัวรถรวมล้อและกันชน ไม่รวมจอ พื้นที่กวาด Motion หรือทางเดิน',fontproperties=TH,fontsize=11,color=BLACK)
    fig.text(.065,.126,'A3 วัดระหว่างแนวศูนย์กลางล้อหน้า–หลัง  |  D1 วัดศูนย์กลางจุดสัมผัสเท้า  |  D2 เป็นช่องติดตั้งตัวอย่าง',fontproperties=TH,fontsize=11,color=BLACK)
    fig.text(.065,.095,'ยังต้องวัด: จุดยึด GM5, รูเบาะ/ราง, รูฐานพวงมาลัย/แป้น, VESA, ความสูงจากพื้นห้อง และระยะกวาดจริง',fontproperties=TH,fontsize=11,color=RED)
    footer(fig);save(fig,'02-top-dimensions',pdf);plt.close(fig)
print('Rendered 2 PNG + 2 SVG + 2-page PDF')
