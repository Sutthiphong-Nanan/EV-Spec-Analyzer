"""
EV Simulator Version 9.5

-เปลี่ยนให้ปุ่ม "help" run โปรแกรม pdf_viewer.py จากเดิมที่เป็น exe

"""
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, font, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import subprocess
import ttkbootstrap as tkb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame
import sys
import os
import threading

set_theme = 'litera' #เลือกธีมที่ต้องการใช้

#ประกาศตัวแปร global
time_point = None
position_point = None
P_moter_mech_point = None
acc_point = None
v_t_point = None
F_tractive_point = None
F_acc_point = None
F_acc_point = None
F_rolling_point = None
F_grade_point = None 
F_air_point = None
F_acc_power_point = None
F_rolling_power_point = None
F_grade_power_point = None
F_air_power_point = None
power_PV_stop_point = None 
invert_csv_flag = None  
T_motor_point = None
N_motor_point = None
power_PV_run_point = None

# ตรวจสอบว่าโปรแกรมรันจาก PyInstaller หรือไม่
if getattr(sys, 'frozen', False): # ถ้ารันจาก PyInstaller
    # หาตำแหน่งของไฟล์ .exe ที่รันอยู่
    exe_path = sys.executable

    # เอาเฉพาะ path ของโฟลเดอร์ที่ไฟล์ .exe อยู่
    exe_folder = os.path.dirname(exe_path)

    # สร้าง path ที่ถูกต้องสำหรับไฟล์ PDF ที่ควรอยู่ในโฟลเดอร์เดียวกับ .exe
    part_pdf_viewer = os.path.join(exe_folder, "pdf_viewer.exe")
    
else:
    # ถ้ารันจาก source code, ใช้ตำแหน่งปัจจุบัน
    base_path = os.path.dirname(os.path.abspath(__file__))
    part_pdf_viewer = os.path.join(base_path, "pdf_viewer.py")

def help():
    # สร้าง thread ใหม่เพื่อเรียก subprocess
    threading.Thread(target=subprocess.run, args=(["python", part_pdf_viewer],)).start()
    
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry1.delete(0, 'end')
        entry1.insert(0, file_path)
        
def view_csv(file_path_entry1):
    try:
        data_csv = pd.read_csv(file_path_entry1)  # อ่านไฟล์
        data_csv.columns = ['Distance', 'Angle', 'Set_speed', 'Irradian_PV', 'Temp_PV']  # กำหนดชื่อ column


    except:
        messagebox.showerror(message='No CSV file found or data format is incorrect')

    else:
        # ฟังก์ชันสำหรับ plot graph csv
        def plot_graph_csv(x, y, x_name, y_name, title, label_graph):
            # กำหนดสไตล์
            plt.style.use('seaborn-v0_8-whitegrid')
            
            # สร้างกราฟเส้น
            fig, plot_csv = plt.subplots()
            fig.set_dpi(100) 
            plot_csv.plot(x, y, label=label_graph, color='b', linestyle='-', linewidth=1, markersize=2)

            # เพิ่มชื่อแกน x และ y
            plot_csv.set_xlabel(x_name)
            plot_csv.set_ylabel(y_name)
            plot_csv.set_title(title)
            plot_csv.legend()

            # แก้ค่าที่แสดงใน Toolbar ให้มีเว้นวรรคแทนคั่นหลักพัน
            plot_csv.fmt_xdata = lambda x: f"{x:,.2f}".replace(",", " ")  # แทน , ด้วยช่องว่าง
            plot_csv.fmt_ydata = lambda y: f"{y:,.2f}".replace(",", " ")  # แทน , ด้วยช่องว่าง

            # เปลี่ยนชื่อหน้าต่าง
            fig.canvas.manager.set_window_title(title)

            # สร้างหน้าต่าง tkinter
            csv_view_graph_window = tkb.Toplevel()
            csv_view_graph_window.title(title)

            # แสดงกราฟใน tkinter
            canvas = FigureCanvasTkAgg(fig, master=csv_view_graph_window)  # A tk.DrawingArea
            canvas.draw()
            canvas.get_tk_widget().pack(side=tkb.TOP, fill=tkb.BOTH, expand=1)

            # สร้าง toolbar และตั้งค่าพื้นหลัง
            toolbar = NavigationToolbar2Tk(canvas, csv_view_graph_window)
            toolbar.update()
            toolbar.pack(side=tkb.TOP, fill=tkb.X)
            
            # เปลี่ยนสีพื้นหลังของ toolbar และสีของปุ่ม
            for item in toolbar.winfo_children():
                item.config(bg='white')  # เปลี่ยนพื้นหลังของ toolbar
                if isinstance(item, tkb.Button):
                    item.config(bootstyle="primary")  # เปลี่ยนสีของปุ่มใน toolbar
                    
            # สร้างปุ่มเพิ่มเติมใน toolbar เพื่อกำหนดความละเอียดของไฟล์
            def save_high_quality():
                
                    def save_file():
                        save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf")])
                        if save_path:
                            dpi_value = entry_dpi.get()
                            if dpi_value:
                                fig.savefig(save_path, dpi=int(dpi_value.strip()))
                                dpi_window.destroy()

                    dpi_window = tkb.Toplevel()
                    dpi_window.title("Save Graph High Quality")
                    dpi_window.geometry("400x125")
                    dpi_window.resizable(0, 0)

                    tkb.Label(dpi_window, text="DPI:").pack(padx=5, pady=5)
                    entry_dpi = tkb.Entry(dpi_window)
                    entry_dpi.pack(fill='x', padx=5)

                    tkb.Button(dpi_window, text="Save", command=save_file, bootstyle='success').pack(padx=5, pady=5, fill='x')  # สร้างปุ่ม Save

                
            save_button = tkb.Button(toolbar, text="Save Graph High Quality", bootstyle='dark', command=save_high_quality)
            save_button.pack(side=tk.LEFT, padx=10, pady=5)
            
            # แสดงหน้าต่างกราฟ
            csv_view_graph_window.mainloop()
            

        show_csv = tkb.Window(themename=set_theme)  # เปลี่ยนตามธีมที่ต้องการ
        show_csv.title('View CSV')
        show_csv.geometry('450x650')

        # สร้างเฟรมสำหรับ Treeview และ Scrollbar
        frame_csv_view = tkb.Frame(show_csv)
        frame_csv_view.pack(expand=True, fill='both')

        # สร้างปุ่ม Plot Graph โดยใช้สไตล์ที่ต้องการ
        button_plot_view_csv = tk.Button(frame_csv_view, text='Plot Graph CSV', background='#FF66FF', foreground='#FFFFFF',font=('tahoma', 10, 'bold'), relief='raised'
                                        , command=lambda: plot_graph_csv(data_csv['Distance'], data_csv['Angle'],'Distance', 'Angle', 'Distance vs Angle Graph', 'Data CSV'))
        button_plot_view_csv.pack(side='top', fill='x', padx=2, pady=2)

        # สร้าง Treeview Widget
        tree = tkb.Treeview(frame_csv_view)

        # สร้าง Scrollbar สำหรับ Treeview
        vsb = tkb.Scrollbar(frame_csv_view, orient="vertical", command=tree.yview)
        hsb = tkb.Scrollbar(frame_csv_view, orient="horizontal", command=tree.xview)

        # กำหนด Scrollbar ให้กับ Treeview
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # วาง Scrollbar บนเฟรม
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(expand=True, fill='both')

        # เพิ่มคอลัมน์สำหรับหมายเลขแถว
        columns = ['Row'] + list(data_csv.columns)
        tree['columns'] = columns
        tree['show'] = 'headings'

        # ตั้งค่าหัวคอลัมน์
        for col in columns:
            tree.heading(col, text=col)

        # ตั้งค่าความกว้างของคอลัมน์
        for col in columns:
            tree.column(col, width=50, anchor='center')

        # เติมข้อมูลลงใน Treeview พร้อมหมายเลขแถว
        for index, row in data_csv.iterrows():
            tree.insert('', 'end', values=[index + 1] + list(row))

        show_csv.mainloop()
 
def input_file_calculation(part_csv, invert_csv_flag): #สลับข้อมูล      
    try:
        data_route = pd.read_csv(part_csv) #อ่านไฟล์
        data_route.columns = ['distance', 'angle', 'set_speed', 'irradian_pv', 'temp_pv'] #กำหนดชื่อ column
        test = data_route.set_speed[0] 

        if invert_csv_flag == 1:
            #สลับข้อมูล angle
            data_csv_invert = data_route.copy()
            data_csv_invert['angle'] = data_route['angle'].iloc[::-1].values
            data_csv_invert['set_speed'] = data_route['set_speed'].iloc[::-1].values
             
    except:
        messagebox.showerror(message='No CSV file found or data format is incorrect')

    else:
        if invert_csv_flag != 1: #ถ้าไม่เลือกสลับข้อมูล
            # ใช้ threading เพื่อให้คำนวณแบบไม่บล็อก UI
            thread_calculation_normal = threading.Thread(target=calculation, args=(data_route,))
            thread_calculation_normal.start()

        else: #ถ้าเลือกสลับข้อมูล
            # ใช้ threading เพื่อให้คำนวณแบบไม่บล็อก UI
            thread_calculation_invert = threading.Thread(target=calculation, args=(data_csv_invert,))
            thread_calculation_invert.start()
         


def calculation(data_route): #กดปุ่ม calculation
    
    #ประกาศตัวแปร global
    global time_point
    global position_point
    global P_moter_mech_point
    global acc_point
    global v_t_point
    global F_tractive_point
    global F_acc_point
    global F_acc_point 
    global F_rolling_point
    global F_grade_point  
    global F_air_point
    global F_acc_power_point
    global F_rolling_power_point
    global F_grade_power_point
    global F_air_power_point
    global invert_csv_flag
    global T_motor_point
    global N_motor_point
    global power_PV_stop_point 
    global power_PV_run_point   

    data_route_describe = data_route.describe()       #สร้าง DataFlame ข้อมูลสถิติ วิธีใช้ data_route_describe.distance['max']
    
    # ฟังก์ชันในการลบวิดเจ็ตทั้งหมดภายในเฟรม
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    # เรียกใช้ฟังก์ชันเพื่อลบวิดเจ็ตทั้งหมด
    clear_frame(scrollframe_tab2_info_result_scroll)

    #สร้างตัวแปรสำหรับการคำนวน
    if combo_C_d.get() in C_d_choice:
        C_d = C_d_choice_value[C_d_choice.index(combo_C_d.get())]
        if C_d == None : #ถ้าไม่เลือก แสดงError
            messagebox.showerror(message='Please select Drag Coefficient (Cd)')
            return
    else:
        if num_check(combo_C_d.get(), 'Cd') == True: #ตรวจสอบว่าเป็นตัวเลขหรือไม่
            C_d = float(combo_C_d.get())
        else:
            return

    #แทนค่า Crr   
    if combo_Crr.get() in Crr_choice:
        Crr = Crr_choice_value[Crr_choice.index(combo_Crr.get())]
        if Crr == None : #ถ้าไม่เลือก แสดงError
            messagebox.showerror(message='Please select Rolling coefficient(Crr)') 
            return  
    else:
        if num_check(combo_Crr.get(), 'Crr') == True:
            Crr = float(combo_Crr.get())
        else:
            return



    m = float(entry_m.get())          
    start_acc = float(entry_acc.get())
    brake_acc = float(entry_brake_acc.get())
    Ro = float(entry_Ro.get())
    A = float(entry_A.get())
    radius = float(entry_radius.get())
    R = float(entry_R.get())
    position_max = float(data_route_describe.distance['max'])
    dt = float(entry_dt.get())
    eff_motor = float(entry_motor_Efficiency.get())
    v_max = (5/18) * data_route['set_speed'].max() #km/hr to m/s
    station_stoptime = int(entry_station_stoptime.get()) #sec
    eff_inverter = float(entry_inverter_Efficiency.get())
    run_turn = float(entry_run_turn.get())
    #v_max = (5/18) * float(entry_V.get()) #km/hr to m/s

    #ค่าคงที่
    g = 9.81
    position = 0.00
    alpha = 0
    v_t = 0.00
    time = 0.00
    power_mech = 0.00
    time_without_progress = 0  # เวลาในช่วงที่ไม่เคลื่อนที่

    #คำนวนค่า PV
    try:
        G_pv = float(G_pv_entry.get())     
        K_v_PV = float(K_v_PV_entry.get()) / 100
        T_c_PV = float(T_c_PV_entry.get())
        P_install_PV = float(P_install_entry.get())
        G_ref = 1000
        T_ref = 25
        time_charge_pv = float(pv_time_charge_entry.get())
        f_pv = float(f_pv_entry.get()) / 100
      
           
    except ValueError:
         messagebox.showerror("Error", "must be a number. e.g. --> 1.23'")
         return

    # สร้างหน้าต่างใหม่สำหรับแสดงสถานะการคำนวณ
    status_loop = tkb.Toplevel(title="Calculation Status", size=(400, 150))
    status_loop.geometry("+400+400")
    label = tkb.Label(status_loop, text="Sim Calculating...", bootstyle="info", font=("Tohama", 16, "bold"))
    label.pack(pady=10)
    progress_bar_default = tkb.Progressbar(status_loop, orient="horizontal", length=350, mode="determinate", bootstyle="success")
    progress_bar_default.pack(padx=10, pady=10)
    percentage_label = tkb.Label(status_loop, text="Progress: 0.00%", bootstyle="dark", font=("Tohama", 14, "bold"))
    percentage_label.pack(padx=10, pady=10)

    #สร้างตัวแปรเก็บข้อมูล
    time_point = pd.Series(np.nan, dtype='float64')
    position_point = pd.Series(np.nan, dtype='float64')
    P_moter_mech_point = pd.Series(np.nan, dtype='float64')
    acc_point = pd.Series(np.nan, dtype='float64')
    v_t_point = pd.Series(np.nan, dtype='float64')
    F_tractive_point = pd.Series(np.nan, dtype='float64')
    F_acc_point = pd.Series(np.nan, dtype='float64')
    F_rolling_point = pd.Series(np.nan, dtype='float64')
    F_grade_point = pd.Series(np.nan, dtype='float64')
    F_air_point = pd.Series(np.nan, dtype='float64')
    T_motor_point = pd.Series(np.nan, dtype='float64')
    N_motor_point = pd.Series(np.nan, dtype='float64')
    power_PV_stop_point = pd.Series(np.nan, dtype='float64')
    time_pv_stop_point = pd.Series(np.nan, dtype='float64')
    power_PV_run_point = pd.Series(np.nan, dtype='float64')

    #ตัวแปร index สำหรับการเลื่อนข้อมูล
    index_number = 0
    station_stopflag = False
    integral = 0
    Kp = 0.5        #0.5
    Ki = 0.00005       #0.00005
    record_time = 999999 #ให้ทำงานในครั้งแรกก่อน
    record_time_index = 0

    #loop คำนวน power ของแต่ละช่วงเวลา
    while position <= position_max:
        
        if v_t <= 0 and index_number != 0:  # ตรวจสอบว่าความเร็วปัจจุบันเป็น 0 หรือไม่
            set_speed_now = data_route['set_speed'].max() * (5/18) #km/hr to m/s
            if station_stopflag == True: #เพื่อให้ทำครั้งเดียวตอนหยุดรถที่สถานี
                # เพิ่มเวลาหยุดรถ
                for i in range(int(station_stoptime / dt)): #เพิ่มข้อมูลเวลาหยุดรถ
                    time += dt
                    #บันทึกข้อมูล
                    time_point = pd.concat([time_point, pd.Series([time])], ignore_index=True)
                    position_point = pd.concat([position_point, pd.Series([position])], ignore_index=True) #รถหยุดนิ่ง ตำแหน่งคงเดิม
                    P_moter_mech_point = pd.concat([P_moter_mech_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ไม่มีพลังงาน
                    acc_point = pd.concat([acc_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ความเร่ง
                    v_t_point = pd.concat([v_t_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ไม่มีความเร็ว
                    F_tractive_point = pd.concat([F_tractive_point, pd.Series([m * g * np.sin(np.deg2rad(alpha))])], ignore_index=True) #แรงดึงรถให้คงที่เมื่อรถหยุดนิ่ง
                    F_acc_point = pd.concat([F_acc_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ไม่มีแรงจากการเร่ง
                    F_rolling_point = pd.concat([F_rolling_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ไม่มีแรงต้านล้อ
                    F_grade_point = pd.concat([F_grade_point, pd.Series([m * g * np.sin(np.deg2rad(alpha))])], ignore_index=True)
                    F_air_point = pd.concat([F_air_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ไม่มีแรงต้านอากาศ
                    T_motor_point = pd.concat([T_motor_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง ไม่มีแรงมอเตอร์
                    N_motor_point = pd.concat([N_motor_point, pd.Series([0])], ignore_index=True) #รถหยุดนิ่ง รอบเป็น 0
                    power_PV_run_point = pd.concat([power_PV_run_point, pd.Series([pv_power_run_charge])], ignore_index=True)
                station_stopflag = False
            
        #ส่วนการควบคุมความเร็วรถ                                  
        if pd.notna(data_route['set_speed'][index_number]) == True:  # เรียกใช้ความเร็วรถตาม data_route
            set_speed_now = data_route['set_speed'][index_number] * (5/18) #km/hr to m/s
        
        #ถ้าคำสั่ง set 0 เข้ามา ให้เปลี่ยนเป็น -0.1 เพื่อหยุดรถอย่างรวดเร็ว
        if set_speed_now == 0:
            set_speed_now = -0.1

        #PI control
        error = set_speed_now - v_t  # คำนวณ error
        integral += error*dt  # คำนวณค่าสะสม (integral)
                  
        if v_t != set_speed_now:  # ตรวจสอบว่าความเร็วปัจจุบันไม่เท่ากับความเร็วที่ตั้งไว้หรือไม่
            if v_t > set_speed_now:  
                # ถ้าความเร็วเกินกว่าที่ตั้งไว้ ให้ลดค่าการเบรกลงทีละน้อย แต่ไม่ให้ต่ำกว่า brake_acc
                acc = max((Kp*error) + (Ki*integral), brake_acc) # คำนวณค่าควบคุม (acc)

            elif v_t < set_speed_now:  
                # ถ้าความเร็วต่ำกว่าที่ตั้งไว้ ให้เพิ่มค่าการเร่งขึ้นทีละน้อย แต่ไม่ให้เกิน start_acc
                acc = min((Kp*error) + (Ki*integral), start_acc)

        #หากความเร็วใกล้เคียงกับค่าที่ตั้งไว้มาก (ต่างกันน้อยกว่า 0.01%) ให้หยุดการเร่ง/เบรก
        if abs(v_t - set_speed_now) < set_speed_now * 0.0001:  
            acc = 0  # ตั้งค่า acc เป็น 0 เพื่อหยุดการเร่งหรือเบรก
            v_t = set_speed_now  # ปรับความเร็วให้เท่ากับค่าที่ตั้งไว้

        #เรียกใช้ data_route
        if position >= data_route['distance'][index_number]: #angle แบบ Dinamic
            alpha = float(data_route['angle'][index_number])
            index_number += 1 # เลื่อนบรรทัดข้อมูล data_route

        #คำนวน PV ขณะวิ่ง
        pv_power_run_charge = ((min(G_pv, 1000) / G_ref) * P_install_PV * f_pv *(1 + K_v_PV * (T_c_PV - T_ref))) 

        #สมการคำนวน
        F_tractive = ( m * acc ) + (Crr * m * g ) + ( m * g * np.sin(np.deg2rad(alpha)) ) +  ( (1/2) * Ro * C_d * A * (v_t**2) )

        #เมื่อรถต้องการกำลังจากมอเตอร์
        if F_tractive > 0:
            T_wheel = F_tractive * radius
            W_wheel = v_t / radius #red
            N_wheel = (W_wheel * (60/(2 * np.pi))) #rad to deg
            N_motor = R * N_wheel
            T_motor = T_wheel / R
            power_mech = ((2 * np.pi * N_motor * T_motor) / 60 ) #power mechaniacl
        #เมื่อรถไม่ต้องการกำลังจากมอเตอร์
        else:
            power_mech = 0
            

        #บันทึกข้อมูล
        time_point = pd.concat([time_point, pd.Series([time])], ignore_index=True)
        position_point = pd.concat([position_point, pd.Series([position])], ignore_index=True)
        P_moter_mech_point = pd.concat([P_moter_mech_point, pd.Series([power_mech])], ignore_index=True)
        acc_point = pd.concat([acc_point, pd.Series([acc])], ignore_index=True)
        v_t_point = pd.concat([v_t_point, pd.Series([v_t])], ignore_index=True)
        F_tractive_point = pd.concat([F_tractive_point, pd.Series([F_tractive])], ignore_index=True)
        F_acc_point = pd.concat([F_acc_point, pd.Series([m * acc])], ignore_index=True)
        F_rolling_point = pd.concat([F_rolling_point, pd.Series([Crr * m * g])], ignore_index=True)
        F_grade_point = pd.concat([F_grade_point, pd.Series([ m * g * np.sin(np.deg2rad(alpha))])], ignore_index=True)
        F_air_point = pd.concat([F_air_point, pd.Series([(1/2) * Ro * C_d * A * v_t**2])], ignore_index=True)
        T_motor_point = pd.concat([T_motor_point, pd.Series([T_motor])], ignore_index=True)
        N_motor_point = pd.concat([N_motor_point, pd.Series([N_motor])], ignore_index=True)
        power_PV_run_point = pd.concat([power_PV_run_point, pd.Series([pv_power_run_charge])], ignore_index=True)


        # Update the progress bar in status_loop
        percentage = (position / position_max) * 100
        progress_bar_default['value'] = percentage
        percentage_label['text'] = f"Progress: {percentage:.2f}%"
        status_loop.update_idletasks()

        #ตรวจสอบว่าตำแหน่งไม่เปลี่ยนไป
        position_old = position
           
        #อัปเดทสำหรับ loop ถัดไป
        time += dt
        v_t += acc * dt
        position += v_t * dt
        
        # ตรวจสอบว่าตำแหน่งไม่เปลี่ยนใน 3 * station_stoptime 
        if abs(position - position_old) < (1*5/18) * dt:  # หากตำแหน่งไม่เปลี่ยนแปลงน้อยกว่า 1km/hr เป็นเวลา 3 * station_stoptime sec.
            time_without_progress += dt
        else:
            time_without_progress = 0  # รีเซ็ตหากตำแหน่งเปลี่ยนแปลง
            station_stopflag = True #รถเริ่มเคลื่อนที่ เพื่อให้+เวลาแค่เพียงครั้งเดียว
        if time_without_progress >= 3 * station_stoptime:  # ถ้าผ่านไป 3 * station_stoptime sec. แล้วยังไม่ขยับ
            messagebox.showerror(message='Error Infinite Loop: Please check the speed settings to ensure they are not set to 0, causing the vehicle to remain stationary.')
            break
        
    #ปิดหน้าต่าง status_loop หลังจากที่คำนวนเสร็จ
    status_loop.destroy()    
    


    #ลบค่า NaN ออก
    time_point = time_point.dropna()
    position_point = position_point.dropna()
    P_moter_mech_point = P_moter_mech_point.dropna()
    acc_point = acc_point.dropna()
    v_t_point = v_t_point.dropna()*3.6 #(3.6 คือการเปี่ยน m/s เป็น km/hr)
    F_tractive_point = F_tractive_point.dropna()
    F_acc_point = F_acc_point.dropna()
    F_rolling_point = F_rolling_point.dropna()
    F_grade_point = F_grade_point.dropna()
    F_air_point = F_air_point.dropna()                
    T_motor_point = T_motor_point.dropna()
    N_motor_point = N_motor_point.dropna()
    power_PV_run_point = power_PV_run_point.dropna()

    # สร้างหน้าต่างใหม่สำหรับแสดงสถานะการคำนวณ
    status_loop = tkb.Toplevel(title="Calculation Status", size=(400, 150))
    status_loop.geometry("+400+400")
    label = tkb.Label(status_loop, text="PV Calculating...", bootstyle="info", font=("Tohama", 16, "bold"))
    label.pack(pady=10)
    progress_bar_default = tkb.Progressbar(status_loop, orient="horizontal", length=350, mode="determinate", bootstyle="success")
    progress_bar_default.pack(padx=10, pady=10)
    percentage_label = tkb.Label(status_loop, text="Progress: 0.00%", bootstyle="dark", font=("Tohama", 14, "bold"))
    percentage_label.pack(padx=10, pady=10)

    #loop หาพลังงาน PV
    t = 0
    while t < time_charge_pv:
        if record_time > 1:
            irradiance_pv = min(float(data_route['irradian_pv'][record_time_index]), 1000.0) #irradiance แบบ Dinamic และไม่ให้เกิน 1000
            temp_pv = float(data_route['temp_pv'][record_time_index]) #temp แบบ Dinamic
            record_time = 0
            record_time_index += 1
        
        #การคำนวนการคำนวนพลังงานจาก PV
        pv_power_stop_charge = ((irradiance_pv / G_ref) * P_install_PV * f_pv *(1 + K_v_PV * (temp_pv - T_ref)))     #การคำนวนพลังงานจาก PV หน่วย Watt
        
        #บันทึกข้อมูล
        power_PV_stop_point = pd.concat([power_PV_stop_point, pd.Series([pv_power_stop_charge])], ignore_index=True)
        time_pv_stop_point = pd.concat([time_pv_stop_point, pd.Series([t])], ignore_index=True)

        # Update the progress bar in status_loop
        percentage = (t / time_charge_pv) * 100
        progress_bar_default['value'] = percentage
        percentage_label['text'] = f"Progress: {percentage:.2f}%"
        status_loop.update_idletasks()

        t += 0.1
        record_time += 0.1

    status_loop.destroy()
    #ลบ nan
    power_PV_stop_point = power_PV_stop_point.dropna()
    time_pv_stop_point = time_pv_stop_point.dropna()



    #คำนวนพลังงานของแต่ละแรง
    def power_calculate(F, v, radius, R ):
        v = v * (5/18) #km/hr to m/s
        T_wheel = F * radius
        T_motor = T_wheel / R
        
        W_wheel = v / radius
        N_wheel = (W_wheel * (60/(2 * np.pi)))
        N_motor = R * N_wheel
        
        power = ((2 * np.pi * N_motor * T_motor) / 60 )
        return power
        

    #คำนวนพลังงานของแต่ละแรง    
    F_acc_power_point = power_calculate(F_acc_point, v_t_point, radius, R)
    F_rolling_power_point = power_calculate(F_rolling_point, v_t_point, radius, R)
    F_grade_power_point = power_calculate(F_grade_point, v_t_point, radius, R)
    F_air_power_point = power_calculate(F_air_point, v_t_point, radius, R)
    
    plot_graph(time_point, P_moter_mech_point, 'Time(sec)', 'Power(W)', 'Power vs Time Graph', 'Power Data', None, None, None) #plot graph    

    #คำนวนพลังงานไฟฟ้า จากทางกล
    P_moter_elec_point = P_moter_mech_point * ( 1 / eff_motor) #พลังงานไฟฟ้าที่ใช้จากมอเตอร์
    P_inverter_elec_point = P_moter_elec_point * ( 1 / eff_inverter) #พลังงานไฟฟ้าที่ใช้จากอินเวอร์เตอร์

    #หาขนาดมอเตอร์ที่ต้องใช้
    P_motor_max = P_moter_mech_point.max()/1000
    
    T_motor_max = T_motor_point.max()
    N_motor_max = N_motor_point.max()

    #ขนาด inverter
    P_inverter_max = P_motor_max * ( 1 / eff_inverter) #ขนาดของอินเวอร์เตอร์ที่ต้องใช้

    #หาพลังงาน PV ขณะวิ่ง
    PV_run_charge = ((np.trapezoid(power_PV_run_point, time_point) / 3600) / 1000  ) * run_turn #trapezoidal(y, x) คำนวนพื้นที่ใต้กราฟ และแปลงเป็น kWh
    
    #หาพลังงาน PV ขณะจอด
    PV_stop_charge = (np.trapezoid(power_PV_stop_point, time_pv_stop_point) / 1000 ) #Watt*hr/1000

    #หาขนาดของแบตเตอรี่ที่ไม่มี PV
    Total_power_nonPV = (np.trapezoid(P_inverter_elec_point, time_point)) * run_turn  #trapezoidal(y, x) คำนวนพื้นที่ใต้กราฟ

    Battery_size_nonPV_full = ((Total_power_nonPV / 3600) / 1000) #หน่วยเป็น kWh
    Battery_size_nonPV_lost = Battery_size_nonPV_full * 0.1 #หน่วยเป็น kWh คือ10%ของพลังงานที่ใช้้ไช้ไม่ได้
    Battery_size_nonPV = Battery_size_nonPV_full + Battery_size_nonPV_lost #หน่วยเป็น kWh

    #หาขนาดของแบตเตอรี่ที่มี PV
    Total_power_with_PV = (np.trapezoid(P_inverter_elec_point, time_point)) * run_turn  #trapezoidal(y, x) คำนวนพื้นที่ใต้กราฟ
    Battery_size_with_PV = ((Total_power_with_PV / 3600) / 1000) - PV_run_charge  #หน่วยเป็น kWh

    #น้ำหนักแบตเตอรี่มาคำนวน pv
    Battery_weight_with_PV = max(0, (Battery_size_with_PV * 1000  / 200))  #หน่วยเป็น kg
    
    #น้ำหนักแบตเตอรี่ไม่มี pv
    Battery_weight_nonPV = max(0, (Battery_size_nonPV * 1000  / 200))  #หน่วยเป็น kg
    
    #เวลาที่ใช้ในการชาร์จแบตเตอรี่เต็ม
    Time_Full_charge = ((Battery_size_nonPV / 7) * 60) * 60 #ขนาดกำลังไฟฟ้าในการชาร์จแบตเตอรี่เต็ม 3.5 kWH
    Time_Full_charge_cc = (Time_Full_charge * 0.8) #เวลาที่ใช้ในการชาร์จแบตเตอรี่ แบบ cc 80%
    Time_Full_charge_cv = (Time_Full_charge * 0.2) * 2 #เวลาที่ใช้ในการชาร์จแบตเตอรี่ แบบ cv 20% โดยข้อยๆจ่ายไฟเข้าจะทำให้ใช้เวลา 2 เท่า
    Time_Full_charge_all = Time_Full_charge_cc + Time_Full_charge_cv #เวลาที่ใช้ในการชาร์จแบตเตอรี่ 80% + 20%
    
    #เวลาที่ใช่ชาดด้วยโซลาเซลล์
    Time_Full_charge_with_PV = (( Battery_size_nonPV / (pv_power_run_charge / 1000) ) * 60) * 60 #ขนาดกำลังไฟฟ้าในการชาร์จแบตเตอรี่เต็มด้วยโซล่าเชลล์ 
    Time_Full_charge_with_PV_cc = (Time_Full_charge_with_PV * 0.8) #เวลาที่ใช้ในการชาร์จแบตเตอรี่ แบบ cc 80%  
    Time_Full_charge_with_PV_cv = (Time_Full_charge_with_PV * 0.2) * 2 #เวลาที่ใช้ในการชาร์จแบตเตอรี่ แบบ cv 20% โดยข้อยๆจ่ายไฟเข้าจะทำให้ใช้เวลา 2 เท่า
    Time_Full_charge_with_PV_all = Time_Full_charge_with_PV_cc + Time_Full_charge_with_PV_cv #เวลาที่ใช้ในการชาร์จแบตเตอรี่ 80% + 20%
    
    pv_time_charge = (( pv_power_run_charge ) * time_charge_pv )/1000 #เวลาที่ใช้ในการชาร์จแบตเตอรี่ด้วยโซล่าเชลล์
    
    #ส่วนการแสดงข้อมูล
    #labelframe_tab2_1 สเปคขัันต่ำของรถ
    Label_P_mach_motor = tkb.Label(scrollframe_tab2_info_result_scroll, text ='Motor Size: {:,.3f} kW'.format(float(P_motor_max)))
    Label_P_mach_motor.grid(row=0, column=0, sticky="w", padx=10)

    Label_P_elec_inverter = tkb.Label(scrollframe_tab2_info_result_scroll, text ='Inverter Size: {:,.3f} kW'.format(float(P_inverter_max)))
    Label_P_elec_inverter.grid(row=1, column=0, sticky="w", padx=10)


    labelframe_T_motor_motor = tkb.Label(scrollframe_tab2_info_result_scroll, text='Motor Torque: {:,.3f} Nm'.format(float(T_motor_max)))
    labelframe_T_motor_motor.grid(row=2, column=0, sticky="w", padx=10)

    labelframe_N_motor_motor = tkb.Label(scrollframe_tab2_info_result_scroll, text='Motor Speed: {:,.3f} rpm'.format(float(N_motor_max)))
    labelframe_N_motor_motor.grid(row=3, column=0, sticky="w", padx=10)

    labelframe_power_PV = tkb.Label(scrollframe_tab2_info_result_scroll, text='PV Power: {:,.3f} kWh'.format(float(PV_run_charge)))
    labelframe_power_PV.grid(row=4, column=0, sticky="w", padx=10)

    Label_Battery_size_non = tkb.Label(scrollframe_tab2_info_result_scroll, text ='Battery Size: {:,.3f} kWh'.format(float(Battery_size_nonPV)))
    Label_Battery_size_non.grid(row=0, column=1, sticky="w", padx=10)

    Label_Battery_size = tkb.Label(scrollframe_tab2_info_result_scroll, text ='With-PV Battery Size: {:,.3f} kWh'.format(float(Battery_size_with_PV)))
    Label_Battery_size.grid(row=1, column=1, sticky="w", padx=10)

    Label_Battery_weight_nonPV = tkb.Label(scrollframe_tab2_info_result_scroll, text ='Battery Weight: {:,.3f} kg'.format(float(Battery_weight_nonPV)))
    Label_Battery_weight_nonPV.grid(row=2, column=1, sticky="w", padx=10)
    
    Label_Battery_weight_with_PV = tkb.Label(scrollframe_tab2_info_result_scroll, text ='With-PV Battery Weight: {:,.3f} kg'.format(float(Battery_weight_with_PV)))
    Label_Battery_weight_with_PV.grid(row=3, column=1, sticky="w", padx=10)
    
    Label_Time_pv_charge = tkb.Label(scrollframe_tab2_info_result_scroll, text ='PV Energy Charge: {:,.3f} kWh'.format((pv_time_charge)))
    Label_Time_pv_charge.grid(row=2, column=2, sticky="w", padx=10)
    
    min_charge = int(Time_Full_charge_all//60)
    sec_charge = int(Time_Full_charge_all % 60)   
    Label_Time_Full_charge = tkb.Label(scrollframe_tab2_info_result_scroll, text ='Time to Full Charge: {0} min {1} sec'.format(min_charge, sec_charge ))
    Label_Time_Full_charge.grid(row=0, column=2, sticky="w", padx=10)
    
    min_charge_with_PV = int(Time_Full_charge_with_PV_all//60)
    sec_charge_with_PV = int(Time_Full_charge_with_PV_all % 60)
    Label_Time_Full_charge_with_PV = tkb.Label(scrollframe_tab2_info_result_scroll, text='Time to Full Charge with PV: {0} min {1} sec'.format(min_charge_with_PV, sec_charge_with_PV))
    Label_Time_Full_charge_with_PV.grid(row=1, column=2, sticky="w", padx=10)
    
    Label_PV_stop_charge = tkb.Label(scrollframe_tab2_info_result_scroll, text='PV Energy Charge Stop run: {:,.3f} kWh'.format(float(PV_stop_charge)))
    Label_PV_stop_charge.grid(row=3, column=2, sticky="w", padx=10)

    #Tooltip
    ToolTip(Label_P_mach_motor, text="The minimum motor size is required for the vehicle to operate", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_P_elec_inverter, text="The minimum inverter size required to drive the motor", bootstyle=('dark', tkb.INVERSE))
    ToolTip(labelframe_T_motor_motor, text="The maximum torque of the motor", bootstyle=('dark', tkb.INVERSE))
    ToolTip(labelframe_N_motor_motor, text="The maximum speed of the motor", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Battery_size_non, text="The size of the battery without PV", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Battery_size, text="The size of the battery with PV: \n(Non-PV Battery Size - PV Power)", bootstyle=('dark', tkb.INVERSE))
    ToolTip(labelframe_power_PV, text="The energy generated by the PV", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Battery_weight_nonPV, text="The weight of the battery without PV", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Battery_weight_with_PV, text="The weight of the battery with PV", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Time_Full_charge, text="The time it takes to fully charge the battery", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Time_Full_charge_with_PV, text="The time it takes to fully charge the battery with PV", bootstyle=('dark', tkb.INVERSE))
    ToolTip(Label_Time_pv_charge, text="The energy value that PV generates in a given time", bootstyle=('dark', tkb.INVERSE))
    
def num_check(number, text): #ตรวจสอบว่าเป็นตัวเลขหรือไม่
    try:
        num_rt = float(number)
        return True
    except:
        messagebox.showerror(message=f'{text} must be a number. e.g. --> 1.23')
        return False

def plot_graph(x, y, x_name, y_name, title, label_graph, etc_X, etc_Y,etc_status): #plot graph
    global canvas, toolbar
    # ล้างกราฟเก่า
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
        toolbar.destroy()

    # กำหนดสไตล์และสร้างกราฟ
    plt.style.use('seaborn-v0_8-whitegrid')  # ใช้สไตล์ seaborn

    fig = Figure(figsize=(1, 2), dpi=100)  # สร้างพื้นที่กราฟขนาด 1x1 นิ้ว ความละเอียด 100 dpi
    fig.subplots_adjust(left=0.1, right=0.98, top=0.87, bottom=0.18, wspace=0.4, hspace=0.4)  # ปรับระยะขอบกราฟ
    plot1 = fig.add_subplot(1, 1, 1)  # สร้างพื้นที่ย่อยสำหรับกราฟ

    # ตั้งค่าพื้นฐานของกราฟ
    plot1.set_facecolor('#ffffff')  # กำหนดพื้นหลังสีขาว
    plot1.grid(True, linestyle='--', alpha=0.2)  # แสดงเส้นตารางแบบเส้นประ โปร่งใส 20%

    # หาค่าสูงสุด (Maximum) ของข้อมูล y และตำแหน่ง x ที่ค่าสูงสุด
    max_y = y.max()  # หาค่า y สูงสุด
    max_index = y.idxmax()  # หาตำแหน่ง index ของค่าสูงสุด
    max_x = x[max_index]  # หาค่า x ที่ตำแหน่งสูงสุด

    # วาดกราฟเส้นหลัก - ใช้สีน้ำเงินเข้มและเส้นหนากว่าเพื่อให้เด่นชัด
    plot1.plot(x, y, label=label_graph, color='#000080', linewidth=1.5)  # Navy Blue

    # กรณีที่มีข้อมูลเส้นกราฟเพิ่มเติม
    if etc_status != None:
        if etc_Y != None and etc_X == None:  # กรณีมีข้อมูล Y เพิ่มเติม
            # ใช้สีที่แตกต่างชัดเจนและมีความโปร่งใสเพื่อให้อ่านง่าย
            if etc_status[0] == True:
                plot1.plot(x, etc_Y[0], label='Acceleration', 
                        color='#FF0000', linewidth=1.5, alpha=0.7)  # สีแดง
            if etc_status[1] == True:
                plot1.plot(x, etc_Y[1], label='Rolling Resistance', 
                        color='#008000', linewidth=1.5, alpha=0.7)  # สีเขียว
            if etc_status[2] == True:
                plot1.plot(x, etc_Y[2], label='Grade Resistance', 
                        color='#FFA500', linewidth=1.5, alpha=0.7)  # สีส้ม
            if etc_status[3] == True:
                plot1.plot(x, etc_Y[3], label='Air Resistance', 
                        color='#800080', linewidth=1.5, alpha=0.7)  # สีม่วง
            if etc_status[4] == True and etc_Y[4] is not None:
                plot1.plot(x, etc_Y[4], label='PV Power', 
                        color='#A0522D', linewidth=1.5, alpha=0.7)  # สีน้ำตาล

        if etc_X != None and etc_Y == None:  # กรณีมีข้อมูล X เพิ่มเติม
            if etc_status[0] == True:
                plot1.plot(etc_X[0], y, label='Acceleration', 
                        color='#FF0000', linewidth=1.5, alpha=0.7)
            if etc_status[1] == True:
                plot1.plot(etc_X[1], y, label='Rolling Resistance', 
                        color='#008000', linewidth=1.5, alpha=0.7)
            if etc_status[2] == True:
                plot1.plot(etc_X[2], y, label='Grade Resistance', 
                        color='#FFA500', linewidth=1.5, alpha=0.7)
            if etc_status[3] == True:
                plot1.plot(etc_X[3], y, label='Air Resistance', 
                        color='#800080', linewidth=1.5, alpha=0.7)
            if etc_status[4] == True and etc_X[4] is not None:
                plot1.plot(etc_X[4], y, label='PV Power', 
                        color='#A0522D', linewidth=1.5, alpha=0.7)

    # เพิ่มจุดแสดงค่าสูงสุดและข้อความกำกับ
    plot1.scatter(max_x, max_y,              
                color='#FF0000',  # สีแดงสด
                s=25,  # ลดขนาดจุดลง (เดิม 100)
                marker='D',  # เปลี่ยนเป็นรูปข้าวหลามตัด
                edgecolor='white',  # ขอบสีขาว
                linewidth=1,  # ความหนาขอบ
                zorder=6)  # แสดงทับด้านบนสุด
    # ข้อความกำกับค่าสูงสุด
    plot1.annotate(f'Max: ({max_x:.1f}, {max_y:.1f})', 
                (max_x, max_y),  # ตำแหน่งที่ชี้
                xytext=(10, 10),  # ระยะห่างจากจุด
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5',  # กรอบมน
                        fc='white',  # พื้นหลังขาว
                        ec='#FF0000',  # ขอบสีแดง
                        alpha=0.9),  # ความทึบ 90%
                fontsize=8,  # ขนาดตัวอักษร
                zorder=6)

    # จัดการส่วนประกอบของกราฟ
    plot1.spines['top'].set_visible(False)  # ซ่อนเส้นขอบบน
    plot1.spines['right'].set_visible(False)  # ซ่อนเส้นขอบขวา
    plot1.set_xlabel(x_name, fontsize=10, labelpad=10)  # กำหนดชื่อแกน x
    plot1.set_ylabel(y_name, fontsize=10, labelpad=10)  # กำหนดชื่อแกน y
    plot1.set_title(title, fontsize=12, pad=20, fontweight='bold')  # กำหนดชื่อกราฟ
    plot1.legend(loc='best', fancybox=True, shadow=True, framealpha=1)  # แสดงคำอธิบายสัญลักษณ์ทึบแสง


    # แก้ค่าที่แสดงใน Toolbar ให้มีเว้นวรรคแทนคั่นหลักพัน
    plot1.fmt_xdata = lambda x: f"{x:,.2f}".replace(",", " ")  # แทน , ด้วยช่องว่าง
    plot1.fmt_ydata = lambda y: f"{y:,.2f}".replace(",", " ")  # แทน , ด้วยช่องว่าง

    # วางกราฟลงในหน้าต่างของ tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_tab2)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=0, pady=0, fill='both', expand=True)
    
    # เพิ่ม toolbar เพื่อให้สามารถขยายและย่อกราฟได้
    toolbar = NavigationToolbar2Tk(canvas, frame_tab2)
    toolbar.update()
    toolbar.pack(padx=5, pady=5, fill='x')
    
    # เปลี่ยนสีพื้นหลังของ toolbar และสีของปุ่ม
    for child in toolbar.winfo_children():
        child.configure(bg='#fff')  # กำหนดสีพื้นหลัง
    
    # สร้างปุ่มเพิ่มเติมใน toolbar เพื่อกำหนดความละเอียดของไฟล์
    def save_high_quality():
    
        def save_file():
            save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf")])
            if save_path:
                dpi_value = entry_dpi.get()
                if dpi_value:
                    fig.savefig(save_path, dpi=int(dpi_value.strip()))
                    dpi_window.destroy()

        dpi_window = tkb.Toplevel()
        dpi_window.title("Save Graph High Quality")
        dpi_window.geometry("400x125")
        dpi_window.resizable(0, 0)

        tkb.Label(dpi_window, text="DPI:").pack(padx=5, pady=5)
        entry_dpi = tkb.Entry(dpi_window)
        entry_dpi.pack(fill='x', padx=5)

        tkb.Button(dpi_window, text="Save", command=save_file, bootstyle='success').pack(padx=5, pady=5, fill='x')  # สร้างปุ่ม Save
    
    save_button = tkb.Button(toolbar, text="Save Graph High Quality", bootstyle='dark', command=save_high_quality)
    save_button.pack(side=tk.LEFT, padx=10, pady=5)

    # สร้างปุ่มเพิ่มเติมใน toolbar เพื่อส่งค่า simulation graph ออก csv
    def save_csv():

        # รวม Series เป็น DataFrame
        dataframe_result  = pd.DataFrame({"time_point": time_point,
                                        "position_point": position_point,
                                        "P_moter_mech_point": P_moter_mech_point,
                                        "acc_point": acc_point,
                                        "v_t_point": v_t_point,
                                        "F_tractive_point": F_tractive_point,
                                        "F_acc_point": F_acc_point,
                                        "F_rolling_point": F_rolling_point,
                                        "F_grade_point": F_grade_point,
                                        "F_air_point": F_air_point,
                                        "F_acc_power_point": F_acc_power_point,
                                        "F_rolling_power_point": F_rolling_power_point,
                                        "F_grade_power_point": F_grade_power_point,
                                        "F_air_power_point": F_air_power_point,                                 
                                        "T_motor_point": T_motor_point,
                                        "N_motor_point": N_motor_point,
                                        "power_PV_stop_point": power_PV_stop_point,
                                        "power_PV_run_point": power_PV_run_point})

        save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
        if save_path:
            # บันทึกเป็น CSV
            dataframe_result.to_csv(save_path, index=False)  # ไม่บันทึก index

    save_csv_button = tkb.Button(toolbar, text="Export Variables to CSV", bootstyle='dark', command=save_csv)
    save_csv_button.pack(side=tk.LEFT, padx=10, pady=5)      

# สร้างหน้าต่างหลัก
window = tkb.Window(themename=set_theme)
window.title('EV Spec Analyzer 1.0.0')
window.geometry('1460x768')
window.resizable(1, 1)
window.option_add('*font', 'tahoma 10')

# สร้าง Notebook widget
notebook = tkb.Notebook(window)
notebook.pack(side='top', fill='both', expand=True)

# สร้าง Frame สำหรับแท็บ
frame_tab1 = tkb.Frame(notebook)
frame_tab2 = tkb.Frame(notebook)
notebook.add(frame_tab1, text='Settings')
notebook.add(frame_tab2, text='Results')

# สร้างและกำหนดสไตล์สำหรับวิดเจ็ตทั้งหมด
style = tkb.Style()
style.configure(".", font=("tahoma", 10))  # กำหนดฟอนต์
font_Tab = font.Font(family='Arial', size='12', weight='bold')
style.configure('TNotebook.Tab', font=font_Tab)
style.configure("button_csv_view.TButton", background="#FF66FF", foreground="#FFFFFF"
                , font=("tahoma", 10, "bold"), borderwidth=0, focusthickness=0, focuscolor="none")
style.configure("button_file.TButton", background="#f39c12", foreground="#FFFFFF"
                , font=("tahoma", 10, "bold"), borderwidth=0, focusthickness=0, focuscolor="none")
style.configure("button_calc.TButton", background="#00bc8c", foreground="#FFFFFF"
                , font=("tahoma", 10, "bold"), borderwidth=0, focusthickness=0, focuscolor="none")


label_frame1 = tkb.LabelFrame(frame_tab1, text='Import Data')
label_frame1.pack(padx=5, pady=5, fill='x')
label_frame2 = tkb.LabelFrame(frame_tab1, text='Settings')
label_frame2.pack(padx=5, pady=5, side='top', fill='both', expand=True)
#Scrollbar in Label_Frame2
scrollframe_label_frame2 = ScrolledFrame(label_frame2, autohide=True)
scrollframe_label_frame2.pack(fill='both', expand=True, padx=10, pady=10)


label_frame2_F_rolling = tkb.LabelFrame(scrollframe_label_frame2, text='Rolling Resistance:', width=700, height=100)
label_frame2_F_rolling.grid_propagate(False)
label_frame2_F_rolling.grid(row=3, column=0, sticky="n", padx=5, pady=0)

label_frame2_F_PV = tkb.LabelFrame(scrollframe_label_frame2, text='PV setting', width=620, height=190)
label_frame2_F_PV.grid_propagate(False)
label_frame2_F_PV.grid(row=3, column=1, sticky="n", padx=5, pady=0)

label_frame2_F_aero = tkb.LabelFrame(scrollframe_label_frame2, text='Aerodynamic Resistance:',width=700, height=130)
label_frame2_F_aero.grid_propagate(False)
label_frame2_F_aero.grid(row=1, column=0, padx=5, pady=5)

label_frame2_general = tkb.LabelFrame(scrollframe_label_frame2, text='General variables',width=700, height=120)
label_frame2_general.grid_propagate(False)
label_frame2_general.grid(row=0, column=0, pady=5, padx=5)

label_frame2_moter = tkb.LabelFrame(scrollframe_label_frame2, text='Motor Efficiency / Inverter Efficiency / Number of Rounds',width=620, height=265)
label_frame2_moter.grid_propagate(False)
label_frame2_moter.grid(row=0, column=1, rowspan=2, sticky="n", padx=5, pady=5)

labelframe_tab2_info = tkb.LabelFrame(frame_tab2, text='Specifications of the EV', height=200)
labelframe_tab2_info.grid_propagate(False)
labelframe_tab2_info.pack(side='top', fill='x', padx=5, pady=5)

#plot LabelFrame
frame_tab2_plot = tkb.LabelFrame(labelframe_tab2_info, text='Graph Setting', width=585, height=190)
frame_tab2_plot.grid_propagate(False)
frame_tab2_plot.pack(side='left', padx=5, pady=0)
separator = tkb.Separator(frame_tab2_plot, orient='horizontal', bootstyle='dark')
separator.grid(row=2, column=0, columnspan=3, sticky='ew', padx=2, pady=1)


# สร้าง Radiobutton
#radiobutton set A
selected_option_Y = tk.StringVar(value='power')
radiobutton1_Y = tkb.Radiobutton(frame_tab2_plot, text='Power', width=10, variable=selected_option_Y, value='power', bootstyle="primary-toolbutton")
radiobutton1_Y.grid(row=0, column=0, padx=2, pady=2)
radiobutton2_Y = tkb.Radiobutton(frame_tab2_plot, text='Force', width=10, variable=selected_option_Y, value='force', bootstyle="primary-toolbutton")
radiobutton2_Y.grid(row=0, column=1, padx=2, pady=2)
radiobutton3_Y = tkb.Radiobutton(frame_tab2_plot, text='Acceleration', width=10, variable=selected_option_Y, value='acceleration', bootstyle="primary-toolbutton")
radiobutton3_Y.grid(row=0, column=2, padx=2, pady=2)
radiobutton4_Y = tkb.Radiobutton(frame_tab2_plot, text='Velocity', width=10, variable=selected_option_Y, value='velocity', bootstyle="primary-toolbutton")
radiobutton4_Y.grid(row=1, column=0, padx=2, pady=2)
radiobutton5_Y = tkb.Radiobutton(frame_tab2_plot, text='Position', width=10, variable=selected_option_Y, value='position', bootstyle="primary-toolbutton")
radiobutton5_Y.grid(row=1, column=1, padx=2, pady=2)
radiobutton6_Y = tkb.Radiobutton(frame_tab2_plot, text='Time', width=10, variable=selected_option_Y, value='time', bootstyle="primary-toolbutton")
radiobutton6_Y.grid(row=1, column=2, padx=2, pady=2)
# radiobutton set B
selected_option_X = tk.StringVar(value='time')
radiobutton1_X = tkb.Radiobutton(frame_tab2_plot, text='Power', width=10, variable=selected_option_X, value='power', bootstyle="primary-toolbutton")
radiobutton1_X.grid(row=3, column=0, padx=2, pady=2)
radiobutton2_X = tkb.Radiobutton(frame_tab2_plot, text='Force', width=10, variable=selected_option_X, value='force', bootstyle="primary-toolbutton")
radiobutton2_X.grid(row=3, column=1, padx=2, pady=2)
radiobutton3_X = tkb.Radiobutton(frame_tab2_plot, text='Acceleration', width=10, variable=selected_option_X, value='acceleration', bootstyle="primary-toolbutton")
radiobutton3_X.grid(row=3, column=2, padx=2, pady=2)
radiobutton4_X = tkb.Radiobutton(frame_tab2_plot, text='Velocity', width=10, variable=selected_option_X, value='velocity', bootstyle="primary-toolbutton")
radiobutton4_X.grid(row=4, column=0, padx=2, pady=2)
radiobutton5_X = tkb.Radiobutton(frame_tab2_plot, text='Position', width=10, variable=selected_option_X, value='position', bootstyle="primary-toolbutton")
radiobutton5_X.grid(row=4, column=1, padx=2, pady=2)
radiobutton6_X = tkb.Radiobutton(frame_tab2_plot, text='Time', width=10, variable=selected_option_X, value='time', bootstyle="primary-toolbutton")
radiobutton6_X.grid(row=4, column=2, padx=2, pady=2)

# สร้างฟังก์ชันสำหรับการอัพเดทการ plot graph ตามการเลือกของ radiobutton
def plot_config_update(*args):
    if (P_moter_mech_point is None) or (F_tractive_point is None) or (acc_point is None) or (v_t_point is None) or (position_point is None) or (time_point is None): #ตรวจสอบว่าคำนวนข้อมูลหรือยัง
        messagebox.showerror(message='No data available to display. Please calculate the data first.')
        return
    plot_config = {'power': [P_moter_mech_point,'Power(W)', [F_acc_power_point, F_rolling_power_point, F_grade_power_point, F_air_power_point, power_PV_run_point]], 'force': [F_tractive_point,'Force(N)',[F_acc_point, F_rolling_point, F_grade_point, F_air_point, None]], 'acceleration': [acc_point,'Acceleration(m/s²)', None]
                    , 'velocity': [v_t_point,'Velocity(km/hr)', None], 'position': [position_point,'Position(m)', None], 'time': [time_point,'Time(sec)', None]}
    selected_value_Y = plot_config[selected_option_Y.get()]
    selected_value_X = plot_config[selected_option_X.get()]
    title_dic = {'Power(W)': 'Power', 'Force(N)': 'Force', 'Acceleration(m/s²)': 'Acceleration', 'Velocity(km/hr)': 'Velocity', 'Position(m)': 'Position', 'Time(sec)': 'Time'}
    plot_graph(selected_value_X[0],
                selected_value_Y[0],
                selected_value_X[1],
                selected_value_Y[1],
                f'{title_dic[selected_value_Y[1]]} vs {title_dic[selected_value_X[1]]} Graph',
                f'Total {title_dic[selected_value_Y[1]]}',
                selected_value_X[2],
                selected_value_Y[2],
                [status_checkbutton1.get(), status_checkbutton2.get(), status_checkbutton3.get(), status_checkbutton4.get(), status_checkbutton6.get()])
      
# สร้างปุ่ม Plot Graph จาก radiobutton
button_plot_graph = tkb.Button(frame_tab2_plot, text='Show Selected', bootstyle="success", command=plot_config_update)
button_plot_graph.grid(row=3, column=4, rowspan=3, columnspan=3, padx=5, pady=5, ipadx=42, ipady=20, sticky='e')

# สร้างปุ่มเลือกปิดเปิดกราฟเสริม
status_checkbutton1 = tk.IntVar()
status_checkbutton2 = tk.IntVar()
status_checkbutton3 = tk.IntVar()
status_checkbutton4 = tk.IntVar()
status_checkbutton5 = tk.IntVar()
status_checkbutton6 = tk.IntVar()
invert_csv_flag = tk.IntVar()

# สร้าง Checkbutton 4 ปุ่ม พร้อมตัวแปรสถานะ
checkbutton1 = tkb.Checkbutton(frame_tab2_plot, text="Acc", bootstyle="info-round-toggle", variable=status_checkbutton1)
checkbutton1.grid(row=0, column=4)

checkbutton2 = tkb.Checkbutton(frame_tab2_plot, text="Roll", bootstyle="info-round-toggle", variable=status_checkbutton2)
checkbutton2.grid(row=0, column=5)

checkbutton3 = tkb.Checkbutton(frame_tab2_plot, text="Grad", bootstyle="info-round-toggle", variable=status_checkbutton3)
checkbutton3.grid(row=1, column=4)

checkbutton4 = tkb.Checkbutton(frame_tab2_plot, text="Air", bootstyle="info-round-toggle", variable=status_checkbutton4)
checkbutton4.grid(row=1, column=5)

checkbutton6 = tkb.Checkbutton(frame_tab2_plot, text="PV", bootstyle="info-round-toggle", variable=status_checkbutton6)
checkbutton6.grid(row=1, column=6)

# สร้าง Checkbutton ปุ่ม invert
checkbutton_invert = tkb.Checkbutton(frame_tab2_plot, text="Revert", bootstyle="info-round-toggle", variable=invert_csv_flag)
checkbutton_invert.grid(row=0, column=6)


# ผูกตัวแปรสถานะกับฟังก์ชัน plot_config_update ฟังก์ชันจะทำงานเมื่อมีการเปลี่ยนแปลงในตัวแปรสถานะ
status_checkbutton1.trace_add('write', plot_config_update)
status_checkbutton2.trace_add('write', plot_config_update)
status_checkbutton3.trace_add('write', plot_config_update)
status_checkbutton4.trace_add('write', plot_config_update)
status_checkbutton6.trace_add('write', plot_config_update)
invert_csv_flag.trace_add('write', lambda *args: input_file_calculation(entry1.get(), invert_csv_flag.get()))

#LabelFrame info_result
frame_tab2_info_result = tkb.LabelFrame(labelframe_tab2_info, text='Result', height=190)
frame_tab2_info_result.pack_propagate(False)
frame_tab2_info_result.pack(side='left', fill='x', expand=True, padx=5, pady=5)
frame_tab2_graph_show = tkb.Frame(frame_tab2)
frame_tab2_graph_show.pack(side='top', fill='both', expand=True)
#ScrollFrame in info_result
scrollframe_tab2_info_result_scroll = ScrolledFrame(frame_tab2_info_result, autohide=True)
scrollframe_tab2_info_result_scroll.pack(side='top', fill='both', expand=True)

# LabelFrame 1
button_file_select = tkb.Button(label_frame1, text='Select File', bootstyle="primary", command=select_file)
button_file_select.pack(side='left', padx=10, pady=10)

button_help = tkb.Button(label_frame1, text='Help', bootstyle="warning", command=help)
button_help.pack(side='right', padx=5, pady=5)

entry1 = tkb.Entry(label_frame1)
entry1.pack(side='left', padx=10, pady=10, fill='x', expand=True)

button2 = tkb.Button(label_frame1, text='Calculate', width=10, bootstyle="success", command=lambda: input_file_calculation(entry1.get(), invert_csv_flag.get()))
button2.pack(side='right', padx=5, pady=5)

button3 = tkb.Button(label_frame1, text='View CSV', width=10, bootstyle="info", command=lambda: view_csv(entry1.get()))
button3.pack(side='right', padx=5, pady=5)

#LabelFrame 2
#label_frame2_general
label_m = tkb.Label(label_frame2_general, text='m:')
label_m.grid(row=0, column=0, padx= 5, pady=5)
entry_m = tkb.Entry(label_frame2_general, width=5)
entry_m.insert(0, 1000)
entry_m.grid(row=0, column=1,padx=5)
label_m_unit = tkb.Label(label_frame2_general, text='kg            ')
label_m_unit.grid(row=0, column=2, padx=5, pady=5)

label_radius = tkb.Label(label_frame2_general, text='Radius:')
label_radius.grid(row=0, column=3, padx=5, pady=5)
entry_radius = tkb.Entry(label_frame2_general, width=5)
entry_radius.insert(0, 0.275)
entry_radius.grid(row=0, column=4, padx=5, pady=5)
label_radius_unit = tkb.Label(label_frame2_general, text='m            ')
label_radius_unit.grid(row=0, column=5, padx=5, pady=5)

label_acc = tkb.Label(label_frame2_general, text='Start acc:')
label_acc.grid(row=0, column=6, padx=5, pady=5)
entry_acc = tkb.Entry(label_frame2_general, width=5)
entry_acc.insert(0, 0.9)
entry_acc.grid(row=0, column=7, padx=5, pady=5)
label_acc_unit = tkb.Label(label_frame2_general, text='m/s²')
label_acc_unit.grid(row=0, column=8, padx=5, pady=5)


label_R = tkb.Label(label_frame2_general, text='R:')
label_R.grid(row=1, column=0, padx=5, pady=5)
entry_R = tkb.Entry(label_frame2_general, width=5)
entry_R.insert(0, 1)
entry_R.grid(row=1, column=1, padx=5, pady=5)
label_R_unit = tkb.Label(label_frame2_general, text='-            ')
label_R_unit.grid(row=1, column=2, padx=5)

label_dt = tkb.Label(label_frame2_general, text='dt:')
label_dt.grid(row=1, column=3, padx=5, pady=5)
entry_dt = tkb.Entry(label_frame2_general, width=5)
entry_dt.insert(0, 0.1)
entry_dt.grid(row=1, column=4, padx=5, pady=5)
label_dt_unit = tkb.Label(label_frame2_general, text='sec            ')
label_dt_unit.grid(row=1, column=5, padx=5, pady=5)

label_brake_acc = tkb.Label(label_frame2_general, text='Brake acc:')
label_brake_acc.grid(row=1, column=6, padx=5)
entry_brake_acc = tkb.Entry(label_frame2_general, width=5)
entry_brake_acc.insert(0, -1)
entry_brake_acc.grid(row=1, column=7, padx=5)
label_brake_acc_unit = tkb.Label(label_frame2_general, text='m/s²')
label_brake_acc_unit.grid(row=1, column=8, padx=5)

#label_frame2_F_PV
G_pv_label = tkb.Label(label_frame2_F_PV, text="Irradiance:")
G_pv_label.grid(column=0, row=1, padx=10, pady=10)
G_pv_entry = tkb.Entry(label_frame2_F_PV, width=8)
G_pv_entry.grid(column=1, row=1, padx=10, pady=10)
G_pv_entry.insert(0, 1017.53)
label_G_pv_unit = tkb.Label(label_frame2_F_PV, text='W/m²')
label_G_pv_unit.grid(column=2, row=1, padx=10, pady=10)
K_v_label = tkb.Label(label_frame2_F_PV, text="Kv:")
K_v_label.grid(column=0, row=2, padx=10, pady=10)
K_v_PV_entry = tkb.Entry(label_frame2_F_PV, width=8)
K_v_PV_entry.grid(column=1, row=2, padx=10, pady=10)
K_v_PV_entry.insert(0, -0.29)
label_K_v_unit = tkb.Label(label_frame2_F_PV, text='%/C°')
label_K_v_unit.grid(column=2, row=2, padx=10, pady=10)

pinstall_pv_label = tkb.Label(label_frame2_F_PV, text="P install:")
pinstall_pv_label.grid(column=3, row=2, padx=10, pady=10)
P_install_entry = tkb.Entry(label_frame2_F_PV, width=8)
P_install_entry.grid(column=4, row=2, padx=10, pady=10)
P_install_entry.insert(0, 2225)
label_pinstall_pv_unit = tkb.Label(label_frame2_F_PV, text='W')
label_pinstall_pv_unit.grid(column=5, row=2, padx=10, pady=10)

T_c_PV_label = tkb.Label(label_frame2_F_PV, text="Tc:")
T_c_PV_label.grid(column=3, row=1, padx=10, pady=10)
T_c_PV_entry = tkb.Entry(label_frame2_F_PV, width=8)
T_c_PV_entry.grid(column=4, row=1, padx=10, pady=10)
T_c_PV_entry.insert(0, 33.67)
label_T_c_PV_unit = tkb.Label(label_frame2_F_PV, text='C°')
label_T_c_PV_unit.grid(column=5, row=1, padx=10, pady=10)

pv_time_charge_label = tkb.Label(label_frame2_F_PV, text="Time Charge PV:")
pv_time_charge_label.grid(column=0, row=3, padx=10, pady=10)
pv_time_charge_entry = tkb.Entry(label_frame2_F_PV, width=8)
pv_time_charge_entry.grid(column=1, row=3, padx=10, pady=10)
pv_time_charge_entry.insert(0, 1)
label_pv_time_charge_unit = tkb.Label(label_frame2_F_PV, text='hour')
label_pv_time_charge_unit.grid(column=2, row=3, padx=10, pady=10)

f_pv_label = tkb.Label(label_frame2_F_PV, text="Derating Factor:")
f_pv_label.grid(column=3, row=3, padx=10, pady=10)
f_pv_entry = tkb.Entry(label_frame2_F_PV, width=8)
f_pv_entry.grid(column=4, row=3, padx=10, pady=10)
f_pv_entry.insert(0, 88)
f_pv_label_unit = tkb.Label(label_frame2_F_PV, text='%')
f_pv_label_unit.grid(column=5, row=3, padx=10, pady=10)


#label_frame2_F_rolling
label_Crr = tkb.Label(label_frame2_F_rolling, text='Rolling Coefficient (Crr):')
label_Crr.grid(columnspan=2, row=0, column=0, padx=5)
#กำหนดข้อมูล combobox Crr
Crr_choice = ['Select road surface type or enter a value between 0.00 - 1.00'
                , 'Good asphalt or concrete pavement(0.01 – 0.018): 0.014'
                , 'General asphalt or concrete pavement(0.018 – 0.02): 0.019'
                , 'Good gravel road(0.02 – 0.025): 0.0225'
                , 'Gravel road(0.025 – 0.030): 0.0275'
                , 'Pebble potholes pavement(0.035 – 0.050): 0.0425'
                , 'Pressed dirt road (Dry)(0.025 – 0.035): 0.03'
                , 'Pressed dirt road (Rainy)(0.050 – 0.150): 0.1'
                , 'Muddy dirt road(0.100 – 0.250): 0.175'
                , 'Dry sand(0.100 – 0.300): 0.2'
                , 'Wet sand(0.060 – 0.150): 0.105'
                , 'Icy roads(0.015 – 0.030): 0.0225'
                , 'Compacted ski track(0.030 – 0.050): 0.04'
                ]
Crr_choice_value = [None, 0.014, 0.019, 0.0225, 0.0275, 0.0425
                    , 0.03, 0.1, 0.175, 0.2, 0.105
                    , 0.0225, 0.04]  
combo_Crr = tkb.Combobox(label_frame2_F_rolling, values=Crr_choice, width=50)
combo_Crr.current(1)
combo_Crr.grid(columnspan=4, row=0, column=2, pady=10)

#label_frame2_F_aero
label_Ro = tkb.Label(label_frame2_F_aero, text='ρ:')
label_Ro.grid(row=0, column=0, padx=5, pady=5)
entry_Ro = tkb.Entry(label_frame2_F_aero, width=5)
entry_Ro.insert(0, 1.22)
entry_Ro.grid(row=0, column=1, padx=5, pady=5, sticky='w')
label_Ro_unit = tkb.Label(label_frame2_F_aero, text='kg/m²')
label_Ro_unit.grid(row=0, column=2, padx=5, pady=5, sticky='w')

label_A = tkb.Label(label_frame2_F_aero, text='    A:')
label_A.grid(row=0, column=3, padx=5, pady=5, sticky='e')
entry_A = tkb.Entry(label_frame2_F_aero, width=5)
entry_A.insert(0, 2.905)
entry_A.grid(row=0, column=4, padx=5, pady=5)
label_A_unit = tkb.Label(label_frame2_F_aero, text='m²')
label_A_unit.grid(row=0, column=5, padx=5, pady=5)


label_C_d = tkb.Label(label_frame2_F_aero, text='Drag Coefficient (Cd):')
label_C_d.grid(columnspan=3, row=1, column=0, padx=5, pady=5)                        
C_d_choice = ['Select vehicle type or enter a value between 0.00 - 1.00'
             , 'Passenger car(0.30 - 0.51): 0.405'
             , 'Van(0.40 - 0.58): 0.49'
             , 'Bus(0.50 - 0.80): 0.65'
             , 'Semi-trailer(0.65 - 0.90): 0.775'
             , 'Trailer(0.75 - 1.0): 0.875'
             , 'Circular plate: 1.17'
             , 'Sphere: 0.47'
             , 'Half-sphere: 0.42'
             , '60º-cone: 0.50'
             , 'Cube: 1.05'
              ]
C_d_choice_value = [None, 0.405, 0.49, 0.65, 0.775, 0.875, 1.17, 0.47, 0.42, 0.50, 1.05] 

#Motor Efficiency
label_motor_Efficiency = tkb.Label(label_frame2_moter, text='Motor Efficiency:')
label_motor_Efficiency.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_motor_Efficiency = tkb.Entry(label_frame2_moter, width=20)
entry_motor_Efficiency.insert(0, 0.85)
entry_motor_Efficiency.grid(row=0, column=1, padx=5, pady=5)
label_motor_Efficiency_unit = tkb.Label(label_frame2_moter, text='-')
label_motor_Efficiency_unit.grid(row=0, column=2, padx=5, pady=5)

#Inverter Efficiency
label_inverter_Efficiency = tkb.Label(label_frame2_moter, text='Inverter Efficiency:')
label_inverter_Efficiency.grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_inverter_Efficiency = tkb.Entry(label_frame2_moter, width=20)
entry_inverter_Efficiency.insert(0, 0.95)
entry_inverter_Efficiency.grid(row=1, column=1, padx=5, pady=5)
label_inverter_Efficiency_unit = tkb.Label(label_frame2_moter, text='-')
label_inverter_Efficiency_unit.grid(row=1, column=2, padx=5, pady=5)

#รอบของการวิ่งรถ run_turn
label_run_turn = tkb.Label(label_frame2_moter, text='Number of Rounds:')
label_run_turn.grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_run_turn = tkb.Entry(label_frame2_moter, width=20)
entry_run_turn.insert(0, 1)
entry_run_turn.grid(row=2, column=1, padx=5, pady=5)
label_run_turn_unit = tkb.Label(label_frame2_moter, text='round')
label_run_turn_unit.grid(row=2, column=2, padx=5, pady=5)


#การเพิ่มเวลาหยุดรถที่สถานนี station_stoptime
label_station_stoptime = tkb.Label(label_frame2_moter, text='Station Stop Time:')
label_station_stoptime.grid(row=3, column=0, padx=5, pady=5, sticky='e')
entry_station_stoptime = tkb.Entry(label_frame2_moter, width=20)
entry_station_stoptime.insert(0, 60)
entry_station_stoptime.grid(row=3, column=1, padx=5, pady=5)
label_station_stoptime_unit = tkb.Label(label_frame2_moter, text='sec')
label_station_stoptime_unit.grid(row=3, pady=5, column=2, padx=5)



#กำหนดข้อมูล combobox C_d
combo_C_d = tkb.Combobox(label_frame2_F_aero, values=C_d_choice, width=50)
combo_C_d.current(10)
combo_C_d.grid(columnspan=24, row=1, column=3, pady=5)
  
#ToolTip
ToolTip(label_m, text="Car mass", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_m, text="Car mass", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_acc, text="Car acceleration for increasing speed  \n a = v/t", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_acc, text="Car acceleration for increasing speed", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_brake_acc, text="Car acceleration for decreasing speed", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_brake_acc, text="Car acceleration for decreasing speed", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_radius, text="Wheel radius", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_radius, text="Wheel radius", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_R, text="Gear ratio: \nHigher value reduces required motor torque but increases motor rotation speed", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_R, text="Gear ratio: \nHigher value reduces required motor torque but increases motor rotation speed", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_dt, text="Calculation time interval (delta time)", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_dt, text="Calculation time interval (delta time)", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_Crr, text="Rolling resistance", bootstyle=('dark', tkb.INVERSE))
ToolTip(combo_Crr, text="Rolling resistance", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_Ro, text="Air density", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_Ro, text="Air density", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_A, text="Car frontal area affected by wind", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_A, text="Car frontal area affected by wind", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_C_d, text="Drag coefficient", bootstyle=('dark', tkb.INVERSE))
ToolTip(combo_C_d, text="Drag coefficient", bootstyle=('dark', tkb.INVERSE))
ToolTip(button_file_select, text="CSV file with 3 columns: Column 1 is distance, Column 2 is road angle, Column 3 is the speed of the vehicle and stop points where 1 indicates a stop", bootstyle=('dark', tkb.INVERSE))
ToolTip(button2, text="Calculate data", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry1, text="Enter CSV file path", bootstyle=('dark', tkb.INVERSE))
ToolTip(button3, text="View CSV data", bootstyle=('dark', tkb.INVERSE))
ToolTip(button_plot_graph, text="Show graph", bootstyle=('dark', tkb.INVERSE))
ToolTip(G_pv_entry, text="Irradiance is the amount of radiant energy that falls on a surface per unit area per unit of time, measured in watts per square meter (W/m²). ", bootstyle=('dark', tkb.INVERSE))
ToolTip(G_pv_label, text="Irradiance is the amount of radiant energy that falls on a surface per unit area per unit of time, measured in watts per square meter (W/m²). ", bootstyle=('dark', tkb.INVERSE))
ToolTip(K_v_PV_entry, text=" Temperature coefficient", bootstyle=('dark', tkb.INVERSE))
ToolTip(K_v_label, text=" Temperature coefficient", bootstyle=('dark', tkb.INVERSE))
ToolTip(T_c_PV_entry, text="Total temperature of photovoltaics refers to the operating temperature of PV panels under various conditions, which affects the energy production efficiency of the panels. Higher temperatures lead to a decrease in energy production efficiency because the increase in temperature causes a reduction in the voltage of the panels.", bootstyle=('dark', tkb.INVERSE))
ToolTip(T_c_PV_label, text="Total temperature of photovoltaics refers to the operating temperature of PV panels under various conditions, which affects the energy production efficiency of the panels. Higher temperatures lead to a decrease in energy production efficiency because the increase in temperature causes a reduction in the voltage of the panels.", bootstyle=('dark', tkb.INVERSE))
ToolTip(P_install_entry, text="The power of the installed PV panels", bootstyle=('dark', tkb.INVERSE))
ToolTip(pinstall_pv_label, text="The power of the installed PV panels", bootstyle=('dark', tkb.INVERSE))
ToolTip(combo_Crr, text="Rolling resistance", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_motor_Efficiency, text="Motor efficiency", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_motor_Efficiency, text="Motor efficiency", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_inverter_Efficiency, text="Inverter efficiency", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_inverter_Efficiency, text="Inverter efficiency", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_run_turn, text="Number of running cycles", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_run_turn, text="Number of running cycles", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_station_stoptime, text="Add station stop time", bootstyle=('dark', tkb.INVERSE))
ToolTip(entry_station_stoptime, text="Add station stop time", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton1_Y, text="Y-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton2_Y, text="Y-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton3_Y, text="Y-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton4_Y, text="Y-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton5_Y, text="Y-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton6_Y, text="Y-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton1_X, text="X-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton2_X, text="X-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton3_X, text="X-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton4_X, text="X-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton5_X, text="X-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(radiobutton6_X, text="X-axis", bootstyle=('dark', tkb.INVERSE))
ToolTip(checkbutton1, text="Acceleration", bootstyle=('dark', tkb.INVERSE))
ToolTip(checkbutton2, text="Rolling Resistance", bootstyle=('dark', tkb.INVERSE))
ToolTip(checkbutton3, text="Grade Resistance", bootstyle=('dark', tkb.INVERSE))
ToolTip(checkbutton4, text="Aerodynamic Resistance", bootstyle=('dark', tkb.INVERSE))
ToolTip(checkbutton6, text="PV Power", bootstyle=('dark', tkb.INVERSE))
ToolTip(checkbutton_invert, text="Invert Route Direction", bootstyle=('dark', tkb.INVERSE))
ToolTip(label_frame2_F_aero, text='½ × ρ × Cd × A × v²', bootstyle=('dark', tkb.INVERSE))
ToolTip(label_frame2_F_rolling, text='Crr × m × g', bootstyle=('dark', tkb.INVERSE))
ToolTip(label_frame2_F_PV, text='P = V × I × Avg_PV', bootstyle=('dark', tkb.INVERSE))
ToolTip(label_frame2_general, text='General variables', bootstyle=('dark', tkb.INVERSE))
ToolTip(pv_time_charge_entry, text='Time to charge the battery with PV energy', bootstyle=('dark', tkb.INVERSE))
ToolTip(pv_time_charge_label, text='Time to charge the battery with PV energy', bootstyle=('dark', tkb.INVERSE))
ToolTip(f_pv_entry, text='PV Derating Factor: \nA coefficient that accounts for reduced PV system performance from ideal conditions', bootstyle=('dark', tkb.INVERSE))
ToolTip(f_pv_label, text='PV Derating Factor: \nA coefficient that accounts for reduced PV system performance from ideal conditions', bootstyle=('dark', tkb.INVERSE))

window.mainloop()
