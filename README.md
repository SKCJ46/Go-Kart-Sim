# Go-Kart-Sim

โครงการพัฒนา Go-kart Simulator แบบ Modular เพื่อผลิตขาย เริ่มจากศึกษาความเป็นไปได้และพัฒนาต้นแบบ

## เริ่มอ่านที่นี่

- [บริบทและข้อกำหนดโครงการ](Gokart_IDEA/PROJECT_CONTEXT.md) — แหล่งอ้างอิงหลัก ไม่สร้าง Context ซ้ำอีกชุด
- [ข้อเสนอผู้บริหาร](docs/management-proposal-th.md) / [Word](docs/management-proposal-th.docx) — ร่างเพื่อหารือ งบและเวลาเป็นประมาณการ ยังไม่ใช่อนุมัติผลิต
- [งบและเกณฑ์เครื่องพร้อมโชว์](docs/show-ready-plan-th.md) — ประมาณการสองทางเลือกและร่างเกณฑ์ตรวจรับ 16 ด้าน
- [ท่านั่ง วัสดุ และวิธีประกอบ](docs/seating-materials-assembly-th.md) / [Word](docs/seating-materials-assembly-th.docx) — งานศึกษาสำหรับ Mark พร้อมภาพและตาราง mock-up ยังไม่ใช่แบบผลิต
- [วิธีทำงานร่วมกัน](docs/team-workflow.md)
- [งานที่ต้องทำ](docs/tasks.md)
- [บันทึกการตัดสินใจ](docs/decisions.md)
- [ภาพแนวคิด v03 ไอโซเมทริกดำ–แดงพร้อมขนาด](Gokart_IDEA/Concepts/kart-concept-v03-isometric.png) — มิติเป้าหมายจากงานศึกษา ไม่ใช่แบบผลิต
- [ภาพแนวคิด v02](Gokart_IDEA/Concepts/kart-concept-v02.png)
- [ภาพและคลิปอ้างอิง](Gokart_IDEA/References/)

ข้อเสนอผู้บริหารถูกจัดทำก่อนดึงภาพ/คลิปครบจาก GitHub ข้อความเรื่องไฟล์ที่ได้รับในข้อเสนอนั้นเป็นสถานะ ณ ตอนจัดทำ ปัจจุบันไฟล์อ้างอิงอยู่ใน Gokart_IDEA แล้ว ยังไม่มีการตรวจวิศวกรรมหรือทดสอบฮาร์ดแวร์จริง

## สถานะเครื่องมือ

Repository นี้ยังไม่มีแอป dependency manifest หรือชุดทดสอบ ไม่ต้องติดตั้ง runtime เพียงเพื่ออ่าน/แก้เอกสาร การทดสอบเกม FFB และ GM5 ต้องใช้ PC และฮาร์ดแวร์จริงตามข้อกำหนดผู้ผลิต

ใช้ GitHub เก็บไฟล์และประวัติร่วมกัน แชทแต่ละคนไม่ได้แชร์ประวัติอัตโนมัติ และ Save & Publish ของ Codex ไม่ได้ push ไฟล์ขึ้น GitHub
