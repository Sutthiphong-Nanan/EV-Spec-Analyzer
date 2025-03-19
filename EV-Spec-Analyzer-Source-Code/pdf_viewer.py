import os
import fitz  # PyMuPDF สำหรับการจัดการไฟล์ PDF
from PIL import Image, ImageTk  # Pillow สำหรับจัดการรูปภาพ
import ttkbootstrap as tkb  # ttkbootstrap สำหรับการใช้งาน ttk widgets แบบปรับปรุง
import sys

# ตรวจสอบว่าโปรแกรมรันจาก PyInstaller หรือไม่
if getattr(sys, 'frozen', False):  # ถ้ารันจาก PyInstaller
    exe_path = sys.executable
    exe_folder = os.path.dirname(exe_path)
    path = os.path.join(exe_folder, "Manual.pdf")  # ใช้ไฟล์ PDF จากไดเรกทอรีที่มีโปรแกรม
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # ใช้ตำแหน่งของไฟล์ที่รัน
    path = os.path.join(base_path, "Manual.pdf")  # ใช้ไฟล์ PDF ในโฟลเดอร์เดียวกับสคริปต์

class PDFViewer:
    def __init__(self, master, filepath):
        # ฟังก์ชันเริ่มต้นของ PDFViewer
        self.master = master
        self.master.title('Manual')  # กำหนดชื่อหน้าต่าง
        self.master.geometry('635x800')  # ขนาดของหน้าต่าง

        self.pdf = fitz.open(filepath)  # เปิดไฟล์ PDF
        self.current_page = 0  # เริ่มต้นที่หน้าที่ 0
        self.numPages = self.pdf.page_count  # จำนวนหน้าของ PDF
        self.zoom_factor = 1.0  # ระดับการซูมเริ่มต้น
        self.is_updating = False  # ตัวแปรเช็คว่ากำลังอัปเดตหน้าหรือไม่
        self.is_dragging = False  # ตัวแปรเช็คว่ากำลังลากหน้าหรือไม่
        self.drag_start_x = 0  # ตำแหน่งเริ่มต้นในการลากในแนวนอน
        self.drag_start_y = 0  # ตำแหน่งเริ่มต้นในการลากในแนวตั้ง
        self.canvas_x_offset = 0  # การเลื่อนหน้าจอในแนวนอน
        self.canvas_y_offset = 0  # การเลื่อนหน้าจอในแนวตั้ง

        # สร้างโครงสร้างของหน้าต่าง (Frame และ Canvas)
        self.top_frame = tkb.Frame(self.master)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.grid_propagate(False)  # ไม่ให้ขนาดของ Frame ปรับตามเนื้อหาภายใน

        self.output = tkb.Canvas(self.top_frame)  # Canvas สำหรับแสดง PDF
        self.output.grid(row=0, column=0, sticky="nsew")

        # สร้าง Scrollbar แนวตั้งและแนวนอน
        self.scrolly = tkb.Scrollbar(self.top_frame, orient="vertical", command=self.output.yview)
        self.scrolly.grid(row=0, column=1, sticky=("n", "s"))
        self.scrollx = tkb.Scrollbar(self.top_frame, orient="horizontal", command=self.output.xview)
        self.scrollx.grid(row=1, column=0, sticky=("w", "e"))
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)

        # สร้างปุ่มและช่องกรอกข้อมูลที่ด้านล่าง
        self.bottom_frame = tkb.Frame(self.master)
        self.bottom_frame.grid(row=1, column=0, sticky="ew")
        self.bottom_frame.columnconfigure(9, weight=1)

        self.downbutton = tkb.Button(self.bottom_frame, text="◀", bootstyle="dark", width=3, command=self.previous_page)
        self.downbutton.grid(row=0, column=2, padx=5, pady=5)

        self.upbutton = tkb.Button(self.bottom_frame, text="▶", bootstyle="dark", width=3, command=self.next_page)
        self.upbutton.grid(row=0, column=3, pady=5)

        self.zoom_in_button = tkb.Button(self.bottom_frame, text="Z+", bootstyle="dark", width=3, command=self.zoom_in)
        self.zoom_in_button.grid(row=0, column=4, padx=5, pady=5)

        self.zoom_out_button = tkb.Button(self.bottom_frame, text="Z-", bootstyle="dark", width=3, command=self.zoom_out)
        self.zoom_out_button.grid(row=0, column=5, padx=5, pady=5)

        self.page_entry = tkb.Entry(self.bottom_frame, width=5)  # ช่องกรอกข้อมูลหมายเลขหน้า
        self.page_entry.grid(row=0, column=0, padx=5)
        self.page_entry.bind("<Return>", self.goto_page)  # ผูกเหตุการณ์ Enter กับฟังก์ชัน goto_page

        self.page_label = tkb.Label(self.bottom_frame, text='Page:')  # ป้ายแสดงหมายเลขหน้า
        self.page_label.grid(row=0, column=9, ipadx=10, sticky='e')

        # ทำให้ทุกแถวและคอลัมน์สามารถขยายได้
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.master.bind("<Configure>", self.resize)  # ฟังก์ชันสำหรับปรับขนาดเมื่อหน้าต่างขยาย
        self.display_page()  # เรียกฟังก์ชันแสดงหน้าแรก

        # เพิ่มการรองรับการลากด้วยเม้าส์
        self.output.bind("<ButtonPress-1>", self.start_drag)
        self.output.bind("<B1-Motion>", self.do_drag)
        self.output.bind("<ButtonRelease-1>", self.stop_drag)

        # เพิ่มการรองรับการเลื่อนด้วย scroll wheel
        self.output.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def get_page(self, page_num, width, height):
        # ฟังก์ชันสำหรับดึงหน้าของ PDF และแปลงเป็นรูปภาพ
        page = self.pdf.load_page(page_num)  # โหลดหน้า PDF
        mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)  # ปรับขนาดการซูม
        pix = page.get_pixmap(matrix=mat)  # แปลงหน้า PDF เป็นภาพ
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # แปลงเป็นรูปภาพ
        img_tk = ImageTk.PhotoImage(img)  # แปลงเป็นรูปแบบที่สามารถแสดงใน Tkinter
        return img_tk

    def display_page(self):
        # ฟังก์ชันสำหรับแสดงหน้าปัจจุบัน
        if self.is_updating:
            return  # ถ้ากำลังอัปเดตแล้วไม่ต้องทำอะไร

        self.is_updating = True
        window_width = self.master.winfo_width()  # ความกว้างหน้าต่าง
        window_height = self.master.winfo_height() - 50  # ความสูงหน้าต่าง
        if 0 <= self.current_page < self.numPages:
            # ดึงหน้าปัจจุบันและแสดงผล
            self.img_file = self.get_page(self.current_page, window_width, window_height)
            self.img_ref = self.img_file

            self.output.delete("all")  # ลบเนื้อหาที่เก่า
            self.output.create_image(window_width // 2 + self.canvas_x_offset, window_height // 2 + self.canvas_y_offset, anchor='center', image=self.img_ref)

            self.page_label['text'] = f'Page {self.current_page + 1} of {self.numPages}'  # แสดงหมายเลขหน้า
            self.output.configure(scrollregion=self.output.bbox("all"))  # อัปเดตพื้นที่ scroll
            self.page_entry.delete(0, "end")  # ลบข้อมูลเก่าในช่องกรอก
            self.page_entry.insert(0, str(self.current_page + 1))  # ใส่หมายเลขหน้าปัจจุบัน

        self.is_updating = False

    def next_page(self):
        # ฟังก์ชันไปยังหน้าถัดไป
        if self.current_page < self.numPages - 1:
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        # ฟังก์ชันกลับไปหน้าก่อนหน้า
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def zoom_in(self):
        # ฟังก์ชันซูมเข้าหน้า
        self.zoom_factor *= 1.2
        self.display_page()

    def zoom_out(self):
        # ฟังก์ชันซูมออกจากหน้า
        self.zoom_factor /= 1.2
        self.display_page()

    def resize(self, event):
        # ฟังก์ชันปรับขนาดหน้าต่าง
        self.display_page()
        self.output.configure(scrollregion=self.output.bbox("all"))

    def goto_page(self, event=None):
        # ฟังก์ชันไปยังหน้าที่ระบุจากช่องกรอก
        try:
            page_number = int(self.page_entry.get()) - 1  # เลขหน้าเริ่มต้นจาก 1 ดังนั้นต้องลบ 1
            if 0 <= page_number < self.numPages:
                self.current_page = page_number
                self.canvas_x_offset = 0  # รีเซ็ตค่า x offset
                self.canvas_y_offset = 0  # รีเซ็ตค่า y offset
                self.display_page()  # อัปเดตการแสดงผลของหน้า
                self.output.configure(scrollregion=self.output.bbox("all"))  # อัปเดต scroll region
        except ValueError:
            pass  # ถ้าไม่ใช่ตัวเลข จะไม่ทำอะไร

    def start_drag(self, event):
        # ฟังก์ชันเริ่มต้นการลาก
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        # ฟังก์ชันลากหน้าระหว่างการกดเม้าส์
        if self.is_dragging:
            delta_x = event.x - self.drag_start_x
            delta_y = event.y - self.drag_start_y

            self.canvas_x_offset += delta_x
            self.canvas_y_offset += delta_y

            self.drag_start_x = event.x
            self.drag_start_y = event.y

            self.output.scan_mark(event.x, event.y)
            self.output.scan_dragto(event.x + delta_x, event.y + delta_y, gain=1)
            
            self.output.update_idletasks()  # เพิ่มบรรทัดนี้เพื่ออัปเดตการแสดงผล

    def stop_drag(self, event):
        # ฟังก์ชันหยุดการลาก
        self.is_dragging = False

    def on_mouse_wheel(self, event):
        # ฟังก์ชันรองรับการเลื่อนด้วยล้อเม้าส์
        if event.delta > 0:
            self.output.yview_scroll(-1, "units")
        else:
            self.output.yview_scroll(1, "units")

        self.output.configure(scrollregion=self.output.bbox("all"))

# สร้างหน้าต่างหลักของโปรแกรม
root = tkb.Window(themename="litera")
app = PDFViewer(root, path)  # สร้างอ็อบเจ็กต์ PDFViewer
root.mainloop()  # เรียกให้โปรแกรมทำงาน
