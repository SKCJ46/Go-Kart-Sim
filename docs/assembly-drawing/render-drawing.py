"""Vector 2D dimensional study. Reuses v04.1 coordinates; no fabrication geometry inferred."""
from pathlib import Path
import json,math,re
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import fitz

R=Path(__file__).resolve().parent
D=json.loads((R.parent/'dimension-study/layout-v04.json').read_text())
pdfmetrics.registerFont(TTFont('Thai','/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Latin','/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LatinB','/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('ThaiB','/usr/share/fonts/truetype/noto/NotoSansThai-Bold.ttf'))
BLACK='#20262e';RED='#be2934';BLUE='#176385';GRAY='#7f8992';LIGHT='#e6e9ec'
PDF=R/'kart-assembly-2d-rev-b.pdf'
c=canvas.Canvas(str(PDF),pagesize=(420*mm,297*mm))
c.setTitle('Go-kart Simulator | 2D Assembly Dimension Study | Rev B | 26 Oct 2026')
c.setAuthor('Think Of Sim')

def line(x1,y1,x2,y2,color=BLACK,w=.3,dash=False):
 c.setStrokeColor(color);c.setLineWidth(w*mm);c.setDash([2*mm,1*mm] if dash else []);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
def rect(x,y,w,h,color=BLACK,lw=.3,fill=None,dash=False):
 c.setStrokeColor(color);c.setLineWidth(lw*mm);c.setDash([2*mm,1*mm] if dash else []);
 if fill:c.setFillColor(fill)
 c.rect(x*mm,y*mm,w*mm,h*mm,stroke=1,fill=bool(fill))
def poly(pts,color=BLACK,w=.4,close=False,fill=None,dash=False):
 p=c.beginPath();p.moveTo(pts[0][0]*mm,pts[0][1]*mm)
 for x,y in pts[1:]:p.lineTo(x*mm,y*mm)
 if close:p.close()
 c.setStrokeColor(color);c.setLineWidth(w*mm);c.setDash([2*mm,1*mm] if dash else [])
 if fill:c.setFillColor(fill)
 c.drawPath(p,stroke=1,fill=bool(fill))
def circle(x,y,r,color=BLACK,lw=.3,fill=None):
 c.setStrokeColor(color);c.setLineWidth(lw*mm);c.setDash([])
 if fill:c.setFillColor(fill)
 c.circle(x*mm,y*mm,r*mm,stroke=1,fill=bool(fill))
def runs(s,bold=False):
 out=[]
 for ch in s:
  family=('Thai' if '\u0e00'<=ch<='\u0e7f' else 'Latin')+('B' if bold else '')
  if out and out[-1][0]==family:out[-1]=(family,out[-1][1]+ch)
  else:out.append((family,ch))
 return out
def rich(s):
 return ''.join('<font name="'+font+'">'+escape(t).replace('\n','<br/>')+'</font>' for font,t in runs(s))
def text(x,y,s,size=9,color=BLACK,bold=False,align='left',bg=False):
 chunks=runs(s,bold);width=sum(pdfmetrics.stringWidth(t,font,size) for font,t in chunks)/mm
 dx=width/2 if align=='center' else width if align=='right' else 0
 if bg:
  c.setFillColor('white');c.rect((x-dx-.7)*mm,(y-.8)*mm,(width+1.4)*mm,(size/mm+1.2)*mm,stroke=0,fill=1)
 c.setFillColor(color);xx=x-dx
 for font,t in chunks:
  c.setFont(font,size);c.drawString(xx*mm,y*mm,t);xx+=pdfmetrics.stringWidth(t,font,size)/mm
def para(x,top,width,s,size=9,color=BLACK):
 p=Paragraph(rich(s),ParagraphStyle('p',fontName='Latin',fontSize=size,leading=size*1.45,textColor=color,wordWrap='CJK'))
 _,h=p.wrap(width*mm,300*mm);p.drawOn(c,x*mm,top*mm-h);return h/mm

def base(n,title,sub):
 rect(8,8,404,281,lw=.4);text(14,278,'GO-KART SIMULATOR',17,bold=True)
 text(14,267,title,13,bold=True);text(14,258,sub,9,color=BLUE)
 text(405,278,f'ASSEMBLY STUDY / {n:02d} OF 06',10,align='right',bold=True)
 text(405,268,'REV B  |  26 OCT 2026',9,align='right');text(405,258,'ALL DIMENSIONS mm  |  SCALE NTS',9,align='right')
 line(8,251,412,251,color=GRAY,w=.2);line(8,26,412,26,color=GRAY,w=.2)
 text(14,18,'ขนาดเสนอเพื่อวางแบบและลองประกอบ — ยังไม่ใช่แบบตัดท่อ/เจาะรูหรืออนุมัติผลิต',10,color=RED,bold=True)
 text(14,11,'READ NUMBERS ONLY. FLOOR Z=0 IS LOCAL COCKPIT DATUM, NOT ROOM GROUND. ALL HARDWARE INTERFACES TBD.',7,color=GRAY)
 text(405,18,f'KART-ASM-B-{n:02d}',9,align='right',bold=True)
def end():c.showPage()
class View:
 def __init__(self,x,y,k):self.x=x;self.y=y;self.k=k
 def p(self,x,y):return self.x+x*self.k,self.y+y*self.k
 def line(self,x1,y1,x2,y2,**kw):line(*self.p(x1,y1),*self.p(x2,y2),**kw)
 def poly(self,pts,**kw):poly([self.p(x,y) for x,y in pts],**kw)
 def rect(self,x,y,w,h,**kw):rect(*self.p(x,y),w*self.k,h*self.k,**kw)
 def circle(self,x,y,r,**kw):circle(*self.p(x,y),r*self.k,**kw)
 def label(self,x,y,s,**kw):text(*self.p(x,y),s,**kw)
 def point(self,x,y,name,dx=3,dy=3):
  px,py=self.p(x,y);line(px-1.8,py,px+1.8,py,color=BLUE,w=.45);line(px,py-1.8,px,py+1.8,color=BLUE,w=.45);text(px+dx,py+dy,name,10,color=BLUE,bold=True,bg=True)
 def hd(self,x1,x2,y,s,b1=None,b2=None,color=RED):
  a,b=self.p(x1,y),self.p(x2,y)
  for x,basey in [(x1,b1),(x2,b2)]:
   if basey is not None:self.line(x,basey,x,y+(15 if y>basey else -15),color=GRAY,w=.15)
  line(*a,*b,color=color,w=.25)
  poly([a,(a[0]+2.2,a[1]+.65),(a[0]+2.2,a[1]-.65)],color=color,w=.1,close=True,fill=color)
  poly([b,(b[0]-2.2,b[1]+.65),(b[0]-2.2,b[1]-.65)],color=color,w=.1,close=True,fill=color)
  text((a[0]+b[0])/2,a[1]+2,s,9,color=color,align='center',bg=True)
 def vd(self,x,y1,y2,s,b1=None,b2=None,color=RED):
  a,b=self.p(x,y1),self.p(x,y2)
  for yy,bx in [(y1,b1),(y2,b2)]:
   if bx is not None:self.line(bx,yy,x+(15 if x>bx else -15),yy,color=GRAY,w=.15)
  line(*a,*b,color=color,w=.25)
  poly([a,(a[0]-.65,a[1]+2.2),(a[0]+.65,a[1]+2.2)],color=color,w=.1,close=True,fill=color)
  poly([b,(b[0]-.65,b[1]-2.2),(b[0]+.65,b[1]-2.2)],color=color,w=.1,close=True,fill=color)
  c.saveState();c.translate((a[0]-2)*mm,(a[1]+b[1])/2*mm);c.rotate(90);text(0,0,s,9,color=color,align='center',bg=True);c.restoreState()

def panel(x,top,width,title,rows,fs=9):
 rect(x,top-10,width,10,fill=LIGHT,color=LIGHT);text(x+3,top-7,title,10,bold=True)
 y=top-15
 for k,v in rows:
  h=para(x+3,y,width-6,k,fs,GRAY)
  y-=h+1
  h=para(x+3,y,width-6,v,fs+1,BLACK);y-=h+4
 return y

rear=D['body']['rear_x'];front=D['body']['front_x'];hw=D['body']['half_width']
sx,sy,sz=0,0,D['seat_S']['z'];wx,wz=D['steering_W']['x'],D['steering_W']['z'];px=D['pedal_B']['x'];space=D['pedal_B']['y']-D['pedal_T']['y']
wb=D['axles']['front_x']-D['axles']['rear_x'];angle=D['seat_back_angle_deg_from_rearward_horizontal'];diam=D['steering_W']['rim_diameter']
monitor_w=D['monitors']['housing_width_example'];monitor_h=D['monitors']['housing_height_example'];ma=D['monitors']['side_angle_deg_example'];mx=D['monitors']['centre_plane_x_example'];mz=D['monitors']['bottom_z_example']
wing_x=mx-monitor_w*math.sin(math.radians(ma));wing_y=monitor_w/2+monitor_w*math.cos(math.radians(ma))

# 01 Top. Only dimension body envelope and ergonomic datums; no tube cut dimensions.
base(1,'TOP VIEW / PLAN','มุมบน • หน้ารถไปทางขวา • เส้นโครงสีเทาเป็นภาพจัดวาง ไม่ใช่แนวตัดหรือดัดท่อ')
v=View(92,141,.095)
v.rect(rear,-hw,front-rear,2*hw,color=GRAY,lw=.2,dash=True)
v.line(rear-80,0,front+110,0,color=BLUE,w=.15,dash=True)
v.poly([(-500,-450),(-350,-470),(200,-470),(800,-440),(1110,-300),(1130,300),(800,440),(200,470),(-350,470),(-500,450)],color=GRAY,w=.65,close=True)
v.label(470,-390,'FRAME ROUTING TBD',size=8,color=GRAY,align='center',bg=True)
for axle,tyre in [('rear','rear'),('front','front')]:
 xx=D['axles'][axle+'_x'];t=D['tyres'];rad=t[tyre+'_diameter']/2;ww=t[tyre+'_width'];yy=t[tyre+'_y_abs']
 v.line(xx,-hw-30,xx,hw+30,color=GRAY,w=.15,dash=True)
 for sign in [-1,1]:v.rect(xx-rad,sign*yy-ww/2,rad*2,ww,color=BLACK,lw=.4,fill=LIGHT)
v.rect(-300,-270,540,540,color=BLUE,lw=.2,dash=True)
v.poly([(-260,-250),(100,-250),(240,-200),(240,200),(100,250),(-260,250)],color=BLACK,w=.5,close=True)
v.line(wx,-diam/2,wx,diam/2,w=.8)
for yy in [180,-180]:v.rect(px-45,yy-45,90,90,color=BLACK,lw=.4,fill=LIGHT)
v.line(mx,-monitor_w/2,mx,monitor_w/2,color=GRAY,w=.5,dash=True)
for sign in [-1,1]:v.line(mx,sign*monitor_w/2,wing_x,sign*wing_y,color=GRAY,w=.5,dash=True)
v.point(0,0,'S');v.point(wx,0,'W');v.point(px,180,'B');v.point(px,-180,'T')
v.hd(rear,front,-920,'1800 BODY ENVELOPE',-hw,-hw)
v.hd(D['axles']['rear_x'],D['axles']['front_x'],-800,'1045 WHEELBASE [REF]',-hw,-hw)
v.vd(-720,-hw,hw,'1300 OVERALL WIDTH',rear,rear)
v.hd(0,wx,800,'400 S-W',0,0);v.hd(wx,px,800,'500 W-P',0,180)
v.hd(0,px,990,'900 S-P',0,180)
v.vd(1150,-180,180,'360 PEDAL CENTRES',px,px)
v.vd(-405,-270,270,'540 BAY [EXAMPLE]',-300,-300,color=BLUE)
panel(271,243,133,'DATUM / ตำแหน่งอ้างอิง',[
 ('S — Seat-surface datum','X=0, Y=0 at mid seat travel. Not anatomical H-point.'),
 ('W — Steering wheel centre','X=400, Y=0. Diameter example 310.'),
 ('B / T — Foot contact datums','B: X=900, Y=+180; T: X=900, Y=-180. Driver left = brake.'),
 ('1800 x 1300','Body envelope INCLUDING tyres / bumpers. NOT bare tube frame size.'),
 ('Axle reference','1045 wheelbase only. Axle-to-seat locations / tyre positions are illustrative.'),
 ('Dashed screens','3 x 27 in; placement / side angle illustrative. VESA and support locations TBD.'),
 ('Bare structure','Rail spacing, cross-members, tube cut lengths and bends: TBD.')],fs=8.5)
end()

# 02 Side, same X and Z datums.
base(2,'RIGHT SIDE VIEW / SEATING','มุมด้านข้าง • หน้ารถไปทางขวา • ระยะ 400 / 900 วัดจาก S เดียวกันในแนวนอน')
v=View(91,71,.1)
v.line(rear-80,0,front+100,0,color=BLUE,w=.2,dash=True);v.label(front+60,-42,'Z=0 FLOOR',size=8,color=BLUE,align='right',bg=True)
v.line(rear,-35,front,-35,color=GRAY,w=.8)
for name in ['rear','front']:
 xx=D['axles'][name+'_x'];rad=D['tyres'][name+'_diameter']/2
 v.circle(xx,60,rad,color=BLACK,lw=.4);v.circle(xx,60,rad*.52,color=GRAY,lw=.2);v.line(xx,-100,xx,280,color=GRAY,w=.15,dash=True)
back=(-200,sz+200*math.tan(math.radians(angle)))
v.poly([back,(0,sz),(235,105)],w=1.0)
v.rect(-100,35,300,35,color=GRAY,lw=.4)
v.line(20,0,20,35,color=GRAY,w=.5);v.line(150,0,150,35,color=GRAY,w=.5)
v.line(wx-70,wz-130,wx+70,wz+130,w=1.0)
v.line(wx,wz,620,260,color=GRAY,w=.7);v.line(620,260,620,0,color=GRAY,w=.7)
v.line(px-25,55,px+25,145,w=1.0)
v.rect(mx-8,mz,16,monitor_h,color=GRAY,lw=.3,dash=True);v.line(mx+35,0,mx+35,mz+100,color=GRAY,w=.4,dash=True)
v.point(0,sz,'S');v.point(wx,wz,'W');v.point(px,100,'P')
v.hd(0,wx,735,'400 S-W',sz,wz);v.hd(wx,px,735,'500 W-P',wz,100);v.hd(0,px,900,'900 S-P',sz,100)
v.hd(rear,front,-230,'1800 BODY ENVELOPE',-35,-35)
v.hd(D['axles']['rear_x'],D['axles']['front_x'],-130,'1045 WHEELBASE [REF]',-80,-68)
v.vd(-410,0,sz,'120 S/FLOOR',0,0)
v.vd(1080,sz,wz,'300 W ABOVE S',wx,wx)
v.vd(1260,0,wz,'420 W/FLOOR [DERIVED]',wx,wx)
v.line(-260,sz,0,sz,color=GRAY,w=.2,dash=True)
# angle arc with vertex S and correct rearward horizontal reference
pts=[v.p(160*math.cos(math.radians(a)),sz+160*math.sin(math.radians(a))) for a in range(120,181,3)]
poly(pts,color=RED,w=.25);v.label(-175,sz+180,'60 deg',size=9,color=RED,bg=True)
panel(275,243,129,'VERTICAL / ความสูงและมุม',[
 ('S at mid rail','Z=120 above LOCAL cockpit floor; trial range 100-160.'),
 ('W centre','Z=420 = 120+300. Trial W above S: 250-350.'),
 ('Seat back','60 deg example; trial 58-63 deg from REARWARD horizontal, not seat-to-back angle.'),
 ('Pedal height','Z=100 is drawing example only. Actual contact height / tilt TBD.'),
 ('Monitor height','Grey dashed position illustrative. Eye position, FOV, VESA and support height TBD.'),
 ('Ground / GM5','Room-ground height, GM5 installed height and stroke envelope NOT dimensioned.'),
 ('Wheel Z','Tyre centre elevations schematic. No ground clearance or rolling geometry specified.')],fs=8.5)
end()

# 03 Front projection, Y increases toward the driver's left (viewer right).
base(3,'FRONT VIEW / WIDTH & MONITOR STUDY','มุมหน้า • ด้านซ้ายผู้ขับอยู่ทางขวาของภาพ • ความสูงจอและจุดยึดยังเป็นตัวอย่าง')
v=View(144,70,.115)
v.line(-800,0,800,0,color=BLUE,w=.2,dash=True);v.line(0,-160,0,1100,color=BLUE,w=.15,dash=True)
v.line(-440,-35,440,-35,color=GRAY,w=.8)
for name in ['rear','front']:
 yy=D['tyres'][name+'_y_abs'];ww=D['tyres'][name+'_width'];dia=D['tyres'][name+'_diameter']
 for sign in [-1,1]:v.rect(sign*yy-ww/2,60-dia/2,ww,dia,color=GRAY if name=='rear' else BLACK,lw=.3,dash=name=='rear')
v.poly([(-250,sz),(-250,back[1]),(250,back[1]),(250,sz)],color=GRAY,w=.5,close=True)
v.circle(0,wz,diam/2,color=BLACK,lw=.5);v.point(0,sz,'S',dx=3,dy=-6);v.point(0,wz,'W',dx=3,dy=2)
for yy,name in [(180,'B'),(-180,'T')]:v.rect(yy-45,55,90,90,color=BLACK,lw=.3,fill=LIGHT);v.point(yy,100,name)
# Screens are orthographic projections of equal 615 x 365 housings, 50 degree side angle.
v.rect(-monitor_w/2,mz,monitor_w,monitor_h,color=GRAY,lw=.4,dash=True)
for sign in [-1,1]:
 yy=monitor_w/2 if sign>0 else -wing_y
 v.rect(yy,mz,wing_y-monitor_w/2,monitor_h,color=GRAY,lw=.4,dash=True)
v.hd(-hw,hw,-230,'1300 BODY / TYRE OUTER EDGES',-80,-80)
v.hd(-180,180,-125,'360 PEDAL CENTRES',100,100)
v.hd(-250,250,520,'500 SHELL [EXAMPLE]',back[1],back[1],color=BLUE)
v.hd(-monitor_w/2,monitor_w/2,1060,'615 CENTRE HOUSING [EXAMPLE]',mz+monitor_h,mz+monitor_h,color=GRAY)
v.vd(820,mz,mz+monitor_h,'365 HOUSING [EXAMPLE]',wing_y,wing_y,color=GRAY)
v.label(-610,270,'DRIVER RIGHT',size=8,color=GRAY,align='center');v.label(610,270,'DRIVER LEFT',size=8,color=GRAY,align='center')
panel(274,243,130,'WIDTH REGISTER / ระยะด้านกว้าง',[
 ('Body overall','1300 includes tyres / body. Steel frame width TBD.'),
 ('Seat shell / bay','500 shell example; install bay 540 example within proposed 520-560 range.'),
 ('Pedals','360 centres example; trial 320-400. Not the distance between mounting holes.'),
 ('Wheel example','310 diameter in this study. Trial 300-320; new 330 option must be checked separately.'),
 ('Monitors','3 x 27 in. Example housing 615 x 365 each; actual bezel / VESA / mass TBD.'),
 ('Side monitor angle','50 deg shown; trial 45-55 deg. Projected housing width approx 1406 at 50 deg, excluding supports / gaps.'),
 ('Reserved screen layout','1500-1700 width allowance from earlier study; NOT a fabrication dimension.')],fs=8.5)
end()

# 04 Cross sections plus travel, no fabricated member lengths.
base(4,'SECTIONS / ADJUSTMENTS / THICKNESSES','หน้าตัดวัสดุและช่วงปรับ • ตัวเลือกสำหรับตรวจแบบ ยังไม่ได้อนุมัติขนาดวัสดุหรือโหลด')
text(20,237,'A / ROUND TUBE',11,bold=True);v=View(62,192,1.4);v.circle(0,0,17,lw=.5);v.circle(0,0,14.7,lw=.35)
v.hd(-17,17,-26,'OD 34',0,0);text(62,151,'t = 2.3 / ID = 29.4 derived',9,align='center')
text(120,237,'B / BOX SECTION',11,bold=True);v=View(157,192,1.25);v.rect(-20,-20,40,40,lw=.5);v.rect(-17.7,-17.7,35.4,35.4,lw=.35)
v.hd(-20,20,-29,'40',-20,-20);v.vd(29,-20,20,'40',20,20);text(157,148,'t = 2.3 / inner 35.4 derived',9,align='center')
text(20,136,'IDEALIZED STRAIGHT SECTIONS; actual corner radii and certificates TBD.',8,color=GRAY)
# travel bars drawn in local module coordinates, without absolute end-stop positions
text(20,122,'C / TOTAL ADJUSTMENT TRAVEL',11,bold=True)
for yy,width,label_ in [(104,230,'Seat 230 example / trial 200-230'),(80,150,'Pedal set 150 proposed'),(56,100,'Steering X 100 / Z 100 proposed')]:
 v=View(38,yy,.55);v.line(0,0,width,0,color=GRAY,w=1.5);v.hd(0,width,-13,str(width),0,0,color=BLUE);text(20,yy+8,label_,9)
panel(239,243,165,'MATERIAL / THICKNESS PROPOSALS',[
 ('Main round tube','JIS G3444 STK400 / OD 34 x t2.3'),('Lower beams / screen support','JIS G3466 STKR400 / 40 x 40 x t2.3'),('FFB / pedal plates & gussets','SS400 steel t4-6, fold / brace as required'),('Motion adapter study','Steel t6-8; hole pattern / load check TBD'),('Seat cradle study','Formed steel t3-4; shape / shell support TBD'),('Floor study','Aluminium 5052-H32 t2-3; trial support spacing 200-250'),('Body / covers study','ABS or PC/ABS t3-4; process / shape TBD'),('Adjustment endpoints','Bars show TOTAL travel only. Do not infer slot length, hole pitch, lock points or absolute endpoints.')],fs=8.5)
end()

# Register helpers: wrapped tables with explicit status/source, legible at A3.
def table(x,top,width,headers,rows,colwidths,fs=9,rowmin=10):
 xx=[x]
 for z in colwidths:xx.append(xx[-1]+width*z)
 headerh=11
 rect(x,top-headerh,width,headerh,color=LIGHT,fill=LIGHT)
 for j,h in enumerate(headers):text(xx[j]+2,top-7.5,h,fs,bold=True)
 y=top-headerh
 for row in rows:
  paras=[];height=rowmin
  for j,cell in enumerate(row):
   p=Paragraph(rich(str(cell)),ParagraphStyle('cell',fontName='Latin',fontSize=fs,leading=fs*1.35,textColor=BLACK,wordWrap='CJK'))
   _,h=p.wrap((xx[j+1]-xx[j]-4)*mm,100*mm);paras.append((p,h));height=max(height,h/mm+4)
  for j,(p,h) in enumerate(paras):p.drawOn(c,(xx[j]+2)*mm,(y-2)*mm-h)
  line(x,y-height,x+width,y-height,color=LIGHT,w=.2);y-=height
 return y
base(5,'DIMENSION REGISTER / NOMINAL & TRIAL RANGES','ตารางรวมระยะที่มี • P = ข้อเสนอ / REF = อ้างอิง / D = คำนวณจากข้อเสนอ ไม่ใช่ระยะวัดจริง')
rows=[
 ('01','Body length / width','1800 x 1300','1700-1850 / 1200-1350','P; envelope incl. tyres/body, not bare steel'),
 ('02','Wheelbase','1045','Choose real kart','REF; axle positions in drawing illustrative'),
 ('03','S to W, horizontal','400','350-450','P; same S datum at mid rail'),
 ('04','S to pedals, horizontal','900','800-1000','P; foot contact not mounting holes'),
 ('05','W to pedals, horizontal','500','Derived from chosen X','D; 900-400, not 400+900'),
 ('06','S above cockpit floor','120','100-160','P; local floor, not room ground'),
 ('07','W above S','300','250-350','P; vertical difference'),
 ('08','W above cockpit floor','420','From S + W/S','D; 120+300 at example position'),
 ('09','Seat back from rear horizontal','60 deg','58-63 deg','P; not seat-to-back angle'),
 ('10','Seat slider total','230','200-230','P; lock both rails; endpoint geometry TBD'),
 ('11','Pedal slider total','150','Trial proposed','P; carrier and lock geometry TBD'),
 ('12','Steering adjustment totals','X 100 / Z 100','Trial proposed','P; slot / lock geometry TBD'),
 ('13','Pedal contact centres','360','320-400','P; verify cables and driver posture'),
 ('14','Wheel diameter','310 example','300-320 trial; 330 candidate','P; chosen model still not selected'),
 ('15','Seat install bay / shell example','540 / 500','Bay 520-560','P; measure shell + support + tools'),
 ('16','Knee clearance to hard parts','>=50 proposed','Check every tested posture','P; not a certified pinch/safety distance'),
 ('17','Monitor housings','3 x 615 x 365','3 x 27 in reference','P; selected housing/VESA still TBD'),
 ('18','Side monitor angle / layout width','50 deg example','45-55 deg / 1500-1700','P; width allowance excludes sweep/access'),
 ('19','Tyre outline rear / front','280 x 180 / 255 x 115','Drawing examples only','P; diameter x width, not selected tyres'),
]
thai_names=['ขนาดรวมตัวรถ ยาว / กว้าง','ฐานล้อ','S ถึงพวงมาลัย แนวนอน','S ถึงแป้น แนวนอน','พวงมาลัยถึงแป้น แนวนอน','S สูงจากพื้น Cockpit','พวงมาลัยสูงกว่า S','พวงมาลัยสูงจากพื้น Cockpit','มุมพนักจากแนวนอนชี้ไปท้ายรถ','ช่วงเลื่อนเบาะรวม','ช่วงเลื่อนชุดแป้นรวม','ช่วงปรับพวงมาลัยรวม','ระยะศูนย์กลางแป้นซ้าย–ขวา','เส้นผ่านศูนย์กลางวง','ช่องติดตั้งเบาะ / shell ตัวอย่าง','ช่องเข่าถึงชิ้นส่วนแข็ง','กรอบจอภาพตัวอย่าง','มุมจอข้าง / พื้นที่วางจอ','ยางหลัง / หน้า ตัวอย่างในภาพ']
rows=[(row[0],name,*row[2:]) for row,name in zip(rows,thai_names)]
table(14,243,392,['ID','Dimension / รายการ','Example / mm','Trial range / ช่วงลอง','Status / ข้อจำกัด'],rows,[.045,.25,.16,.22,.325],fs=8.6,rowmin=10.2)
text(16,30,'Source: dimension-study/layout-v04.json (v04.1) + seating-materials-assembly-th.md. No new hardware measurements.',8,color=GRAY)
end()
base(6,'FABRICATION GAPS / DATUM COORDINATES','รายการที่ยังต้องวัดก่อนสั่งตัดท่อ/เจาะรู • ไม่ใส่ตัวเลขหรือความยาวชิ้นงานที่ยังไม่มีข้อมูล')
left=[('S','0','0','120','Seat-surface datum, rail at mid'),('W','400','0','420','Wheel centre, example'),('B','900','+180','100','Driver-left brake contact; Z illustrative'),('T','900','-180','100','Driver-right throttle contact; Z illustrative')]
table(14,243,200,['Point','X','Y','Z','Meaning'],left,[.1,.13,.13,.13,.51],fs=8.5,rowmin=15)
para(17,160,192,'X forward; Y driver left; Z above local cockpit floor. S is not anatomical H-point. Moving the seat changes S-relative reaches. Pedal heights and all surface geometry are illustrative.',9,color=GRAY)
right=[('Bare frame layout','Rail spacing, cross-member XYZ, tube centre-lines, joints'),('Tube fabrication','Member cut lengths, mitres/fishmouths, bend angles/radii, developed lengths'),('GM5 interface','Actual XYZ, hole/threads, mounting thickness/torque, load cases'),('Seat / slider','Chosen shell holes/supports, rail pitch, stop/lock points, installed height'),('FFB / pedals','Selected models, hole patterns, plate shape, cables and permitted separate mounts'),('Monitor support','Selected VESA, screen depth/mass, support height, eye/FOV and arm lengths'),('Assembly controls','Tolerances, jig datums, weld symbols/map, bolt grades/torques, finish masks'),('Operating envelope','Motion installed/working heights, swept volume, access and transport clearances')]
table(224,243,182,['Still TBD','Required before fabrication'],right,[.30,.70],fs=8.7,rowmin=20)
text(17,127,'NO CUT LIST OR DRILL TEMPLATE RELEASED',11,color=RED,bold=True)
para(17,119,190,'1800 x 1300 is the complete body envelope. It must not be used as tube centre-line dimensions or as the width/length of the bare welded frame.',10,color=RED)
para(17,89,190,'Material allowance from earlier study: round tube 6-8 m + box tube 3-4 m for budget only. These are not per-member cutting lengths and do not establish quantity/strength of a build.',9)
para(17,60,190,'Next: measure actual hardware -> mock-up -> CAD frame/loads -> fabrication drawings & BOM -> review -> supplier quote -> approved release.',9,color=BLUE)
end();c.save()

# Generate scalable vector sheets and previews from the exact same PDF, no image editing.
doc=fitz.open(PDF)
for i,page in enumerate(doc):
 (R/f'{i+1:02d}-sheet.svg').write_text(page.get_svg_image(text_as_path=True))
 page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(R/f'{i+1:02d}-sheet.png')
register={
 'revision':'B','date':'2026-10-26','units':'mm','status':'proposed assembly dimension study; not fabrication release',
 'source':'../dimension-study/layout-v04.json (v04.1), ../seating-materials-assembly-th.md',
 'body_envelope':{'length':front-rear,'width':hw*2,'includes':'tyres/body; excludes monitors, sweep, access','bare_frame_size':'TBD'},
 'datum':D['datum'],'points':{k:D[k] for k in ['seat_S','steering_W','pedal_B','pedal_T']},
 'horizontal':{'S_W':wx,'S_P':px,'W_P':px-wx,'wheelbase_ref':wb},
 'vertical':{'S_floor':sz,'W_S':wz-sz,'W_floor_derived':wz},
 'pedal_contact_centres':space,'adjustment_totals':D['adjustments'],'frame_section_proposals':D['frame'],
 'register_rows':rows,'fabrication_TBD':right,
 'illustrative_only':'All drawn rail paths, shell profiles, mount supports, tyre Z, axle offsets and screen positions; do not extract part lengths from graphics',
}
(R/'dimension-register.json').write_text(json.dumps(register,ensure_ascii=False,indent=2)+'\n')
print(f'Created {len(doc)} vector A3 sheets, PDF, SVG, PNG and register')
