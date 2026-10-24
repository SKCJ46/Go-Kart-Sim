"""Build the editable structure-only estimate; amounts are project allowances, not quotes."""
from pathlib import Path
import xlsxwriter

OUT = Path(__file__).with_name('structure-budget-th.xlsx')
wb = xlsxwriter.Workbook(OUT)
wb.set_properties({'title': 'Go-kart Simulator — งบโครงสร้าง Cockpit', 'subject': 'ประมาณการรวมเบาะ ล้อ และขาจอ ต่อหนึ่งเครื่อง', 'author': 'Think Of Sim', 'comments': 'จัดทำ 24 ตุลาคม 2026; ฐานประมาณการ 23 ตุลาคม 2026; ไม่ใช่ใบเสนอราคาหรืออนุมัติซื้อ'})
wb.set_calc_mode('auto')
INK, RED, GRAY, LINE, BLUE = '#24262D', '#C82935', '#667078', '#E2E4E8', '#165DB5'
def fmt(**kwargs):
    return wb.add_format({'font_name': 'Noto Sans Thai', 'font_size': 11, 'font_color': INK, 'valign': 'vcenter', **kwargs})
F = {
 'title':fmt(font_size=23,bold=True,font_color='white',bg_color=INK),
 'sub':fmt(font_size=10,font_color=GRAY,text_wrap=True),
 'band':fmt(bold=True,font_color=RED,bg_color='#FBEDEE',text_wrap=True),
 'head':fmt(bold=True,font_color='white',bg_color=INK,text_wrap=True),
 'text':fmt(text_wrap=True,bottom=1,bottom_color=LINE),
 'num':fmt(num_format='#,##0',align='right',bottom=1,bottom_color=LINE),
 'input':fmt(font_color=BLUE,bg_color='#EDF4FF',num_format='#,##0',align='right',border=1,border_color='#C6D8F3'),
 'pct':fmt(font_color=BLUE,bg_color='#EDF4FF',num_format='0%',align='center',border=1,border_color='#C6D8F3'),
 'sumlabel':fmt(bold=True,bg_color='#EFEDE9'),
 'sum':fmt(bold=True,bg_color='#EFEDE9',num_format='#,##0',align='right'),
 'grandlabel':fmt(bold=True,bg_color=RED,font_color='white',font_size=13),
 'grand':fmt(bold=True,bg_color=RED,font_color='white',font_size=17,num_format='#,##0',align='right'),
 'biglabel':fmt(bold=True,font_color=RED,bg_color='#FBEDEE'),
 'big':fmt(bold=True,font_color=RED,bg_color='#FBEDEE',font_size=18,num_format='#,##0',align='right'),
 'note':fmt(text_wrap=True,font_size=10,font_color=GRAY,bg_color='#F4F5F7'),
 'link':fmt(font_color=BLUE,underline=1,font_size=10),
 'warn':fmt(bg_color='#FFD6D9',font_color='#A11B28'),
}
summary = wb.add_worksheet('สรุปเสนอผู้บริหาร')
detail = wb.add_worksheet('รายละเอียดงบ')
notes = wb.add_worksheet('สมมติฐานและไม่รวม')
for ws in (summary,detail,notes):
    ws.hide_gridlines(2);ws.set_zoom(90);ws.set_tab_color(RED);ws.set_paper(9);ws.set_landscape()
    ws.set_margins(0.3,0.3,0.4,0.4);ws.fit_to_pages(1,1);ws.center_horizontally()
    ws.set_header('&LThink Of Sim | Go-kart Simulator&Rประมาณการ / ยังไม่ใช่ราคาจัดซื้อ',{'margin':0.15})
    ws.set_footer('&L24 ต.ค. 2026 | THB ต่อเครื่อง&Rหน้า &P / &N',{'margin':0.2})
    ws.set_default_row(26)

# Detail sheet: editable range and reserve, with formula caches for all viewers.
detail.set_column('A:A',7);detail.set_column('B:B',29);detail.set_column('C:C',65)
detail.set_column('D:E',18);detail.set_column('F:F',23)
detail.merge_range('A1:F2','รายละเอียดงบโครงสร้าง',F['title'])
detail.merge_range('A3:F3','ตัวเลขสีน้ำเงินแก้ไขได้ | ฐานประมาณการ 23 ต.ค. 2026 | ทุกหมวดต่อหนึ่งเครื่อง ไม่ใช่ราคาต่อชิ้น',F['sub'])
detail.write('A5','เผื่อ',F['sumlabel']);detail.write_number('B5',0.2,F['pct'])
detail.merge_range('C5:F5','อัตราเงินเผื่อคิดจากยอดโครงสร้างก่อนเผื่อเพียงครั้งเดียว ไม่ครอบคลุมรายการที่แยกออก',F['sub'])
detail.write_row('A7',['รหัส','หมวด','รายละเอียดที่รวม','ต่ำ / บาท','สูง / บาท','สถานะ'],F['head']);detail.set_row(6,30)
items=[
 ('S01','โครงท่อหลัก','ท่อเหล็ก คานรอง จุดเสริมรับ Motion วัสดุ ตัด ดัด เชื่อม และทำสี',30000,45000),
 ('S02','พื้นและตัวรถ','พื้น ตัวถัง กันชน ล้อ 4 ล้อ ยาง และดุม ไม่มีเครื่องยนต์หรือระบบขับรถจริง',18000,30000),
 ('S03','ชุดเบาะ','เบาะโกคาร์ท รางเลื่อน และชุดรอง/ขายึด ต้องยืนยันขนาดและจุดยึด',6000,12000),
 ('S04','ชุดขาจอ','โครงรองรับสามจอ ขายึด และชุดถอดประกอบ ไม่รวมตัวจอ',12000,20000),
]
for row,(code,name,scope,low,high) in enumerate(items,7):
    detail.set_row(row,58)
    for col,value in [(0,code),(1,name),(2,scope)]:detail.write(row,col,value,F['text'])
    detail.write_number(row,3,low,F['input']);detail.write_number(row,4,high,F['input'])
    detail.write(row,5,'ประมาณการโครงการ\nยังไม่มีใบเสนอราคา',F['text'])
    for col in (3,4):detail.write_comment(row,col,'แก้เป็นประมาณการที่ปรับแล้วได้ เมื่อมีใบเสนอราคาให้ตรวจรายการรวม/ไม่รวม VAT และขนส่งก่อนใช้ ห้ามรวมอุปกรณ์ Sim หรือจอเข้าหมวดนี้')
low=sum(x[3] for x in items);high=sum(x[4] for x in items)
for row,label in [(12,'รวมก่อนเงินเผื่อ'),(13,'เงินเผื่อ'),(14,'รวมเงินเผื่อแล้ว')]:
    detail.merge_range(row,0,row,2,label,F['grandlabel'] if row==14 else F['sumlabel'])
    detail.write_blank(row,5,None,F['grandlabel'] if row==14 else F['sumlabel']);detail.set_row(row,34)
for col,total in [('D',low),('E',high)]:
    detail.write_formula(f'{col}13',f'=SUM({col}8:{col}11)',F['sum'],total)
    detail.write_formula(f'{col}14',f'={col}13*$B$5',F['sum'],total*0.2)
    detail.write_formula(f'{col}15',f'={col}13+{col}14',F['grand'],total*1.2)
detail.merge_range('A17:F18','ราคาย่อย เช่น ค่าเหล็ก ค่าเชื่อม ค่าล้อ หรือค่าแรง ยังไม่ได้แยกจากผู้ผลิต จึงไม่สร้างราคาย่อยสมมติขึ้นมาแทนใบเสนอราคา',F['note'])
detail.merge_range('A20:F21','งานผลิตแต่ละชุดอยู่ในหมวดนั้นแล้ว ส่วนออกแบบ จิ๊ก ทดลอง ทดสอบ ประกอบรวมระบบขั้นสุดท้าย และชุดขนย้ายแยกงบ ตรวจขอบเขตอะแดปเตอร์เฉพาะรุ่นและ interface GM5 ก่อนยืนยันราคา',F['note'])
detail.merge_range('A23:F24','ที่มา: docs/structure-budget-th.md (23 ต.ค. 2026) ซึ่งคัดสี่หมวดจาก docs/show-ready-plan-th.md (21 ต.ค. 2026) ไม่มีการขอราคาใหม่ในรอบจัดทำ Excel',F['sub'])
detail.autofilter('A7:F11');detail.freeze_panes(7,3);detail.print_area('A1:F24');detail.repeat_rows(6,6)
detail.data_validation('B5',{'validate':'decimal','criteria':'between','minimum':0,'maximum':1,'input_title':'อัตราเงินเผื่อ','input_message':'ป้อน 20% หรือ 0.20','error_title':'อัตราไม่ถูกต้อง','error_message':'ป้อนระหว่าง 0%–100%'})
detail.data_validation('D8:D11',{'validate':'decimal','criteria':'>=','value':0,'error_message':'ราคาต้องไม่ติดลบ'})
detail.data_validation('E8:E11',{'validate':'custom','value':'=AND(ISNUMBER(E8),E8>=D8,E8>=0)','error_message':'ราคาสูงต้องเป็นตัวเลขและไม่น้อยกว่าราคาต่ำ'})
detail.conditional_format('D8:E11',{'type':'formula','criteria':'=OR($D8<0,$E8<$D8)','format':F['warn']})

# Executive summary, designed to print on one landscape A4 page.
summary.set_column('A:B',23);summary.set_column('C:F',17)
summary.merge_range('A1:F2','งบโครงสร้าง Go-kart Simulator',F['title'])
summary.merge_range('A3:F3','เสนอพิจารณา | จัดทำ 24 ต.ค. 2026 | ฐานประมาณการ 23 ต.ค. 2026 | บาทต่อหนึ่งเครื่อง',F['sub'])
summary.merge_range('A5:F5','รวมโครง + พื้น/ตัวถัง/กันชน + เบาะ + ล้อ/ยาง/ดุม + ขาจอ',F['band'])
summary.merge_range('A6:F6','ไม่รวมอุปกรณ์ Sim/Motion, PC และตัวจอ | ขอบเขตยืนยันแล้ว ราคายังเป็นประมาณการ',F['sub'])
summary.merge_range('A8:B8','รายการ',F['head']);summary.merge_range('C8:D8','ประมาณการต่ำ / บาท',F['head']);summary.merge_range('E8:F8','ประมาณการสูง / บาท',F['head'])
for row,item in enumerate(items,8):
    summary.set_row(row,33);summary.merge_range(row,0,row,1,item[1],F['text'])
    for col,dc,val in [(2,'D',item[3]),(4,'E',item[4])]:
        summary.merge_range(row,col,row,col+1,'',F['num']);summary.write_formula(row,col,f"='รายละเอียดงบ'!{dc}{row}",F['num'],val)
for row,label,ref,vals in [(12,'รวมก่อนเงินเผื่อ',13,(low,high)),(13,'เงินเผื่อ',14,(low*.2,high*.2)),(14,'รวมเงินเผื่อแล้ว',15,(low*1.2,high*1.2))]:
    lf=F['grandlabel'] if row==14 else F['sumlabel'];nf=F['grand'] if row==14 else F['sum'];summary.set_row(row,35)
    summary.merge_range(row,0,row,1,label,lf)
    if row==13:summary.write_formula(row,0,'="เงินเผื่อ "&TEXT(\'รายละเอียดงบ\'!B5,"0%")',lf,'เงินเผื่อ 20%')
    for col,dc,val in [(2,'D',vals[0]),(4,'E',vals[1])]:
        summary.merge_range(row,col,row,col+1,'',nf);summary.write_formula(row,col,f"='รายละเอียดงบ'!{dc}{ref}",nf,val)
summary.set_row(16,38);summary.merge_range('A17:B17','ช่วงปัดสำหรับคุยทีม',F['biglabel'])
summary.merge_range('C17:D17','',F['big']);summary.write_formula('C17','=ROUND(C15,-4)',F['big'],80000)
summary.merge_range('E17:F17','',F['big']);summary.write_formula('E17','=ROUND(E15,-4)',F['big'],130000)
summary.merge_range('A18:D18','ค่ากลางปัดเพื่อเริ่มคุย — ไม่ใช่เพดานอนุมัติ',F['sub'])
summary.merge_range('E18:F18','',F['sum']);summary.write_formula('E18','=ROUND(AVERAGE(C15,E15),-4)',F['sum'],100000)
summary.merge_range('A20:F21','แยกงบเพิ่มเติม: อุปกรณ์ Sim/Motion, PC, จอ, ระบบไฟ/ซอฟต์แวร์, ออกแบบ/จิ๊ก/ทดลอง/ทดสอบ, ประกอบรวมระบบขั้นสุดท้าย, ชุดขนย้าย และค่าโชว์; VAT/ขนส่งต้องตรวจจากใบเสนอราคาจริง',F['note'])
summary.merge_range('A23:F24','สถานะ: ยังไม่มีใบเสนอราคาและยังไม่อนุมัติงบ/จัดซื้อ งบนี้เป็นเพียงส่วนโครงสร้าง ไม่ใช่งบเครื่องพร้อมโชว์ทั้งระบบ และห้ามบวกซ้ำกับหมวดเดียวกันในงบรวมเดิม',F['note'])
summary.merge_range('A26:D26','ปรับตัวเลขสีน้ำเงินในชีต “รายละเอียดงบ” ยอดสรุปคำนวณอัตโนมัติ',F['sub'])
summary.merge_range('E26:F26','',F['link']);summary.write_url('E26',"internal:'รายละเอียดงบ'!A1",F['link'],'ไปปรับรายละเอียด →')
summary.freeze_panes(8,2);summary.print_area('A1:F26');summary.set_first_sheet();summary.activate()

# Assumptions and exclusions: readable notes with no fabricated amounts.
notes.set_column('A:A',24);notes.set_column('B:B',71);notes.set_column('C:C',32)
notes.merge_range('A1:C2','สมมติฐาน / ขอบเขต / รายการรอราคา',F['title'])
notes.merge_range('A3:C3','ไม่มีรายการรอราคาใดถูกนับเป็นศูนย์ในงบโครงสร้าง ต้องแยกประเมินก่อนรวมงบทั้งเครื่อง',F['sub'])
notes.write_row('A5',['หัวข้อ','รายละเอียด','สถานะ'],F['head'])
rows=[
 ('ฐานผลิต','ประเมินต้นแบบหนึ่งเครื่อง ตัวรถตั้งต้น 1,800 × 1,300 มม. ไม่รวมพื้นที่จอยื่นและการเคลื่อน Motion','สมมติฐาน ยังไม่ใช่แบบผลิต'),
 ('วิธีผลิต','โครงเหล็กเชื่อม โมดูลถอดด้วยน็อต งานสีสำหรับโชว์ วัสดุและจุดยึดต้องตรวจโหลด/แบบจริง','ข้อเสนอวิธีผลิต'),
 ('เบาะและล้อ','รวมเบาะ ราง ขายึด ล้อ ยาง และดุม รุ่น/ขนาด/คุณภาพยังต้องเลือก','ยืนยันขอบเขต ยังไม่เลือกรุ่น'),
 ('ขาจอ','รวมโครงรองรับสามจอและชุดถอด ต้องตรวจน้ำหนักและแรงจาก Motion','ยืนยันขอบเขต รอตรวจแบบ'),
 ('รายการที่ราคาผันแปร','รูปทรงตัวถัง งานผิว ขาจอ จุดรับ Motion และจำนวนรอบแก้แบบ','ต้องดูแบบก่อนตีราคาจริง'),
 ('อุปกรณ์ Sim / Motion','ฐาน FFB พวงมาลัย แป้น เบรก Active ชุด Motion/controller และอุปกรณ์เสริม','ไม่รวม / รอเลือกรุ่นและราคา'),
 ('PC และจอภาพ','PC จอ และอุปกรณ์คอมพิวเตอร์ ไม่รวมตัวจอแม้ขาจออยู่ในงบ','ไม่รวม / แยกงบ'),
 ('ระบบไฟ / ซอฟต์แวร์','สาย อุปกรณ์เชื่อมต่อ ระบบหยุด เกม ซอฟต์แวร์ควบคุม และไลเซนส์','ไม่รวม / รอผัง รุ่น และสิทธิ์'),
 ('พัฒนา / จิ๊ก / ทดสอบ','ออกแบบ จิ๊ก mock-up ชิ้นส่วนทดลอง การทดสอบและตรวจรับ','ไม่รวม / ประเมินขอบเขตก่อน'),
 ('ประกอบรวมระบบ','ติดตั้ง/รวมระบบและตั้งค่าขั้นสุดท้าย แยกจากค่าผลิตแต่ละชุดที่อยู่ในงบแล้ว','ไม่รวม / ป้องกันคิดแรงงานซ้ำ'),
 ('ขนย้ายและงานโชว์','ชุดขนย้าย แพ็กกิ้ง ค่ารถ บูธ เดินทาง และเจ้าหน้าที่','ไม่รวม / รอรูปแบบและสถานที่'),
 ('VAT / ขนส่ง','ตรวจว่าราคาแต่ละบรรทัดรวมภาษี/ส่งแล้วหรือไม่ บวกเฉพาะส่วนที่ยังขาด ไม่บวก VAT ซ้ำ','ยังไม่ยืนยัน / ไม่ถือว่ารวมแล้ว'),
 ('อะแดปเตอร์เฉพาะรุ่น','จุดยึดฐาน FFB แป้นและ interface GM5 ต้องกำหนดแบบก่อนระบุว่ารวมอยู่ในหมวดใด','รอยืนยันขอบเขตและราคา'),
 ('ราคาย่อย','ยังไม่มีราคาวัสดุ ค่าเชื่อม ค่าแรงและชิ้นส่วนแยกย่อย จึงคงไว้เป็นสี่หมวด ไม่แจกแจงตัวเลขขึ้นใหม่','รอใบเสนอราคาผู้ผลิต'),
 ('ก่อนสั่งผลิต','ทำ CAD/BOM เลือกเบาะ/ล้อ/ขาจอ ตรวจโหลดและให้ผู้มีอำนาจอนุมัติแบบ/งบก่อนสั่ง','งานถัดไป ยังไม่ได้สั่ง'),
 ('ขอราคาจริง','ขอแยกวัสดุ แรงงาน สี จิ๊ก VAT ขนส่ง และเงื่อนไขแก้แบบ พร้อมคิวผลิต','งานถัดไป ยังไม่ได้ติดต่อผู้ขาย'),
 ('แหล่งข้อมูล','docs/structure-budget-th.md (23 ต.ค. 2026) และกรอบงบใน docs/show-ready-plan-th.md (21 ต.ค. 2026)','ข้อมูลประมาณการโครงการ'),
]
for row,values in enumerate(rows,5):
    notes.set_row(row,38 if row not in (5,13,17,19,20) else 44)
    for col,value in enumerate(values):notes.write(row,col,value,F['text'])
notes.freeze_panes(5,1);notes.autofilter(4,0,4+len(rows),2);notes.print_area(0,0,4+len(rows),2);notes.repeat_rows(4,4)
wb.close()
print(OUT)
