# EV-Spec-Analyzer

EV-Spec-Analyzer เป็นโปรแกรมจำลองสำหรับวิเคราะห์และออกแบบสเปคของยานยนต์ไฟฟ้า (EV) โดยใช้ข้อมูลเส้นทางที่ป้อนเข้าไปในรูปแบบไฟล์ CSV และพารามิเตอร์ต่างๆ เพื่อคำนวณขนาดมอเตอร์ ขนาดแบตเตอรี่ และพลังงานจากแผงโซลาร์เซลล์ (PV) หากรถมีการติดตั้ง

---

## คุณสมบัติหลัก

**นำเข้าไฟล์ CSV** ที่มีข้อมูลเกี่ยวกับ:

- ระยะทางของเส้นทาง
- ความชันของถนน
- ความเร็วที่ต้องการ (รถจะพยายามรักษาความเร็วตามที่กำหนด)
- ค่าการแผ่รังสีของดวงอาทิตย์ที่กระทบ PV (ถ้ามี PV)
- อุณหภูมิอากาศ (ส่งผลต่อประสิทธิภาพของ PV)

**Simulation & Analysis**

- คำนวณพลังงานที่ต้องใช้ในแต่ละช่วงของเส้นทาง
- วิเคราะห์ขนาดมอเตอร์ที่เหมาะสม
- คำนวณความจุแบตเตอรี่ที่จำเป็น
- พิจารณาผลกระทบของพลังงานจาก PV

**แสดงผลลัพธ์**

- ส่งออกไฟล์ CSV ที่มีข้อมูลสเปคของมอเตอร์และแบตเตอรี่ที่จำเป็น
- ดูกราฟการใช้พลังงานและพารามิเตอร์ที่เกี่ยวข้อง

---

## การติดตั้ง
**วิธีที่ 1**

- 1. เข้าไปในโฟลเดอร์ " EV-Spec-Analyzer "
- 2. เปิดโปรแกรม " EV-Spec-Analyzer.exe "

**วิธีที่ 2**

**1. ติดตั้งไลบรารีที่จำเป็น**

```bash
pip install pandas numpy matplotlib ttkbootstrap
```

**2. รันโปรแกรม**

```bash
python EV_Spec_Analyzer.py
```

## วิธีใช้งานโปรแกรม

1. **เลือกไฟล์ CSV** ที่มีข้อมูลเส้นทาง
2. **กำหนดพารามิเตอร์ต่างๆ** ตามต้องการ
3. **เริ่มการจำลอง** และดูผลลัพธ์ที่ได้

---

## พารามิเตอร์ที่กำหนดค่าได้

### พารามิเตอร์เกี่ยวกับยานยนต์

| พารามิเตอร์ | หน่วย | คำอธิบาย           |
| ----------- | ----- | ------------------ |
| `m`         | kg    | มวลรวมของรถ EV     |
| `radius`    | m     | รัศมีล้อของรถ      |
| `R`         | -     | อัตราทดเกียร์      |
| `start_acc` | m/s²  | อัตราเร่งสูงสุด    |
| `brake_acc` | m/s²  | อัตราการเบรกสูงสุด |
| `dt`        | sec   | ช่วงเวลาการคำนวณในแต่ละเฟรม   |
| `run_turn`  | รอบ   | จำนวนรอบที่วิ่ง    |

### พารามิเตอร์เส้นทางและสภาพถนน

| พารามิเตอร์ | หน่วย  | คำอธิบาย            |
| ----------- | ------ | ------------------- |
| `distance`  | m      | ระยะทางของเส้นทาง   |
| `angle`     | degree | ความชันของถนน       |
| `set_speed` | km/h   | ความเร็วที่ต้องการ  |
| `Crr`       | -      | Rolling Resistance  |
| `Cd`        | -      | Drag Coefficient    |
| `A`         | m²     | พื้นที่หน้าตัดของรถ |
| `Ro`        | kg/m³  | ความหนาแน่นของอากาศ |

### พารามิเตอร์ระบบขับเคลื่อนไฟฟ้า

| พารามิเตอร์        | หน่วย | คำอธิบาย                    |
| ------------------ | ----- | --------------------------- |
| `eff_motor`        | %     | ประสิทธิภาพของมอเตอร์       |
| `eff_inverter`     | %     | ประสิทธิภาพของอินเวอร์เตอร์ |
| `station_stoptime` | sec   | เวลาหยุดจอด                 |

### พารามิเตอร์ของแผงโซลาร์เซลล์ (ถ้ารถติดตั้ง PV)

| พารามิเตอร์      | หน่วย | คำอธิบาย                  |
| ---------------- | ----- | ------------------------- |
| `irradian_pv`    | W/m²  | ค่าการแผ่รังสีของแสง      |
| `temp_pv`        | °C    | อุณหภูมิอากาศ             |
| `P_install_PV`   | W     | กำลังไฟฟ้าสูงสุดของ PV    |
| `K_v_PV`         | %/°C  | ค่าลดประสิทธิภาพ PV       |
| `G_pv`           | W/m²  | ค่าการแผ่รังสีอ้างอิง     |
| `T_c_PV`         | °C    | อุณหภูมิที่ PV ใช้งานจริง |
| `f_pv`           | %     | ค่าการลดประสิทธิภาพ       |
| `time_charge_pv` | hr    | เวลาชาร์จจาก PV           |

---

## สรุป

EV-Spec-Analyzer สามารถคำนวณการใช้พลังงานของ EV ตามเส้นทางที่กำหนด
- คำนวณสเปคของมอเตอร์ที่ต้องใช้
- วิเคราะห์ผลกระทบของ PV ต่อการลดขนาดแบตเตอรี่
- คำนวณระยะเวลาที่ต้องใช้ในการชาร์จแบตเตอรี่

---

