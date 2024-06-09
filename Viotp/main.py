import tkinter as tk
from tkinter import ttk
import viotp
import threading
import time
import os

TOKEN_FILE = 'token.txt'

window = tk.Tk()
window.title("TOOL GET OTP VIOTP API BY CAKKOI - 1.0.1")
window.geometry("1200x600")
# window.attributes("-topmost", True)

def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return ''

def check_xu():
    token = nhap_token.get()
    if token:
        save_token(token)
    sodu = viotp.check_tien(token)
    if sodu is not None:
        temp_value.set(sodu)
        btn_check_xu['text'] = 'Check xu thành công'
        btn_check_xu['text'] = 'Đang kiểm tra dịch vụ'
        update_services()  # Tự động cập nhật dịch vụ sau khi check xu thành công
    else:
        temp_value.set("")
        btn_check_xu['text'] = 'Sai token'
    time.sleep(2)
    btn_check_xu['text'] = 'Check xu'

def luong():
    btn_check_xu['text'] = 'Đang check xu'
    t = threading.Thread(target=check_xu)
    t.start()

def yc_dich_vu():
    selected_service = service_combobox.get()
    service_id = service_data.get(selected_service, None)
    token = nhap_token.get()
    if service_id and token:
        sdt, id_dv = viotp.yc_dich_vu(token, service_id)
        if sdt and id_dv:
            add_service_row(selected_service, id_dv, sdt)
        else:
            print("Lỗi khi lấy dữ liệu từ API")
    else:
        print("Vui lòng chọn dịch vụ và nhập token hợp lệ")

def update_services():
    token = nhap_token.get()
    services = viotp.get_services(token)
    service_names = [f"{service['name']} ({service['price']})" for service in services]
    service_combobox['values'] = service_names

    global service_data
    service_data = {f"{service['name']} ({service['price']})": service['id'] for service in services}

def filter_services(event):
    search_term = search_var.get().lower()
    filtered_services = [name for name in service_data.keys() if search_term in name.lower()]
    service_combobox['values'] = filtered_services

def add_service_row(service_name, request_id, phone_number):
    token = nhap_token.get()

    row_frame = tk.Frame(scrollable_frame)
    row_frame.pack(pady=5, padx=10, fill='x')

    id_text = tk.Label(row_frame, text="ID:", font="Times 12")
    id_text.grid(row=0, column=0, padx=5)

    id_entry = tk.Entry(row_frame, width=10, font="Times 12")
    id_entry.insert(0, request_id)
    id_entry.grid(row=0, column=1, padx=5)

    service_entry = tk.Entry(row_frame, width=10, font="Times 12")
    service_entry.insert(0, service_name)
    service_entry.grid(row=0, column=2, padx=5)

    phone_label = tk.Label(row_frame, text="SĐT:", font="Times 14")
    phone_label.grid(row=0, column=3, padx=5)
    phone_entry = tk.Entry(row_frame, width=10, font="Times 14")
    phone_entry.insert(0, phone_number)
    phone_entry.grid(row=0, column=4, padx=5)

    code_label = tk.Label(row_frame, text="Code:", font="Times 14")
    code_label.grid(row=0, column=5, padx=5)
    code_entry = tk.Entry(row_frame, width=7, font="Times 14")
    code_entry.grid(row=0, column=6, padx=5)

    mess_label = tk.Label(row_frame, text="Mess:", font="Times 14")
    mess_label.grid(row=0, column=7, padx=5)
    mess_entry = tk.Entry(row_frame, width=30, font="Times 13")
    mess_entry.grid(row=0, column=8, padx=5)

    countdown_label = tk.Label(row_frame, font="Times 15")
    countdown_label.grid(row=0, column=9, padx=5)

    delete_button = tk.Button(row_frame, text="Xóa", command=row_frame.destroy, font="Times 13")
    delete_button.grid(row=0, column=10, padx=5)

    threading.Thread(target=viotp.auto_reload, args=(request_id, token, code_entry, mess_entry, countdown_label)).start()

# Enable scrolling using the mouse wheel
def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# GUI setup
top_frame = tk.Frame(window)
top_frame.pack(pady=10, padx=10, fill='x')

token_text = tk.Label(top_frame, text="Nhập token Viotp: ", font="Times 15")
token_text.grid(row=0, column=0, padx=5)

nhap_token = tk.Entry(top_frame, width=40, font="Times 15")
nhap_token.grid(row=0, column=1, padx=5)
loaded_token = load_token()
nhap_token.insert(0, loaded_token)

btn_check_xu = tk.Button(top_frame, text="Check xu", command=luong, font="Times 10")
btn_check_xu.grid(row=0, column=4, padx=5)

so_du_text = tk.Label(top_frame, text="Số dư:", font="Times 15")
so_du_text.grid(row=0, column=2, padx=0)

temp_value = tk.StringVar()
sodu_text = tk.Label(top_frame, width=4, font="Times 15", textvariable=temp_value)
sodu_text.grid(row=0, column=3, padx=15)

second_frame = tk.Frame(window)
second_frame.pack(pady=10, padx=10, fill='x')

timkiem_text = tk.Label(second_frame, text="Tìm kiếm: ", font="Times 15")
timkiem_text.grid(row=0, column=0, padx=5)

search_var = tk.StringVar()
search_entry = tk.Entry(second_frame, textvariable=search_var, font="Times 15")
search_entry.grid(row=0, column=1, padx=67)
search_entry.bind("<KeyRelease>", filter_services)

dichvu_text = tk.Label(second_frame, text="Dịch vụ: ", font="Times 15")
dichvu_text.grid(row=0, column=2, padx=5)

service_combobox = ttk.Combobox(second_frame, font="Times 15")
service_combobox.grid(row=0, column=3, padx=5)

btn_select_service = tk.Button(second_frame, text="Thuê", command=yc_dich_vu, font="Times 10")
btn_select_service.grid(row=0, column=4, padx=5)

scrollable_frame_container = tk.Frame(window)
scrollable_frame_container.pack(pady=10, padx=10, fill='both', expand=True)

canvas = tk.Canvas(scrollable_frame_container)
scrollbar = tk.Scrollbar(scrollable_frame_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

service_data = {}

# Automatically check xu if token is loaded
if loaded_token:
    t = threading.Thread(target=check_xu)
    t.start()

window.mainloop()
