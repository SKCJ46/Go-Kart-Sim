"""One-sheet presentation of the existing structure budget; no new price research."""
from pathlib import Path
import xlsxwriter

out=Path(__file__).with_name('structure-budget-simple.xlsx')
w=xlsxwriter.Workbook(out)
w.set_properties({'title':'งบโครงสร้าง Go-kart Simulator — ฉบับย่อ','author':'Think Of Sim','comments':'จัดทำ 24 ต.ค. 2026 จากประมาณการ 23 ต.ค. 2026 ไม่ใช่ใบเสนอราคา'})
w.set_calc_mode('auto')
s=w.add_worksheet('งบโครงสร้าง');s.hide_gridlines(2);s.set_zoom(100)
s.set_column('A:A',57);s.set_column('B:C',17);s.set_default_row(29)
def f(**kw):return w.add_format({'font_name':'Noto Sans Thai','font_size':12,'valign':'vcenter',**kw})
title=f(font_size=20,bold=True);sub=f(font_size=10,font_color='#666666')
head=f(bold=True,bg_color='#EEEEEE',bottom=1,bottom_color='#BBBBBB')
text=f(text_wrap=True,bottom=1,bottom_color='#DDDDDD');num=f(num_format='#,##0',align='right',bottom=1,bottom_color='#DDDDDD')
label=f(bold=True,bg_color='#F3F3F3');total=f(bold=True,bg_color='#F3F3F3',num_format='#,##0',align='right')
grandlabel=f(bold=True,font_color='#B52330',bg_color='#FAECEE');grand=f(bold=True,font_size=16,font_color='#B52330',bg_color='#FAECEE',num_format='#,##0',align='right')
note=f(font_size=10,font_color='#666666',text_wrap=True)
s.merge_range('A1:C1','งบโครงสร้าง Go-kart Simulator',title);s.set_row(0,39)
s.merge_range('A2:C2','ต่อ 1 เครื่อง | รวมเบาะ ล้อ และขาจอ | จัดทำ 24 ต.ค. 2026',sub)
s.set_row(2,12);s.write_row('A4',['รายการ','ต่ำ (บาท)','สูง (บาท)'],head)
rows=[('โครงเหล็ก ดัด เชื่อม จุดเสริม Motion และทำสี',30000,45000),('พื้น ตัวถัง กันชน ล้อ ยาง และดุม',18000,30000),('เบาะ รางเลื่อน และขายึด',6000,12000),('ขาจอและชุดถอดประกอบ (ไม่รวมตัวจอ)',12000,20000)]
for r,(name,lo,hi) in enumerate(rows,4):
 s.write(r,0,name,text);s.write_number(r,1,lo,num);s.write_number(r,2,hi,num);s.set_row(r,42)
for r,name in [(8,'รวมก่อนเผื่อ'),(9,'เงินเผื่อ 20%'),(10,'รวมเงินเผื่อแล้ว')]:
 s.write(r,0,name,grandlabel if r==10 else label);s.set_row(r,35)
for col,t in [('B',66000),('C',107000)]:
 s.write_formula(f'{col}9',f'=SUM({col}5:{col}8)',total,t)
 s.write_formula(f'{col}10',f'={col}9*20%',total,t*.2)
 s.write_formula(f'{col}11',f'={col}9+{col}10',grand,t*1.2)
s.set_row(11,12);s.merge_range('A13:C13','',f(bold=True,font_size=15))
s.write_formula('A13','= "ประมาณ "&TEXT(ROUND(B11,-4),"#,##0")&"–"&TEXT(ROUND(C11,-4),"#,##0")&" บาท / เครื่อง"',f(bold=True,font_size=15),'ประมาณ 80,000–130,000 บาท / เครื่อง');s.set_row(12,35)
s.set_row(13,12)
notes=[
 'ไม่รวมอุปกรณ์ Sim/Motion, PC, จอภาพ ระบบไฟ และซอฟต์แวร์',
 'ไม่รวมออกแบบ จิ๊ก ทดลอง ทดสอบ ประกอบรวมระบบขั้นสุดท้าย ชุดขนย้าย และค่าโชว์',
 'เป็นประมาณการ ยังไม่มีใบเสนอราคา; VAT/ขนส่งต้องตรวจเพิ่ม ไม่ใช่งบเครื่องพร้อมโชว์ทั้งชุด',
]
for r,n in enumerate(notes,14):s.merge_range(r,0,r,2,n,note);s.set_row(r,35)
s.freeze_panes(4,1);s.set_portrait();s.set_paper(9);s.fit_to_pages(1,1);s.print_area('A1:C17');s.set_margins(.35,.35,.4,.4)
s.set_footer('&Rหน้า &P / &N',{'margin':.2})
w.close();print(out)
