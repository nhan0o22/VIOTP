import requests
import json
import threading
import time
import tkinter as tk

def check_tien(api_viotp):
    url_check_tien = "https://api.viotp.com/users/balance?token=" + api_viotp
    p = requests.get(url_check_tien)
    if 'data' in p.text:
        ss = json.loads(p.text)
        sodu = ss['data']['balance']
        print("Số dư:", sodu)
        return sodu
    else:
        print("Lỗi khi lấy dữ liệu từ API:", p.status_code)
        return None

def get_services(api_viotp):
    url_check_services = f"https://api.viotp.com/service/getv2?token={api_viotp}&country=vn"
    p = requests.get(url_check_services)
    if p.status_code == 200:
        ss = json.loads(p.text)
        return ss['data'] if 'data' in ss else []
    else:
        print("Lỗi khi lấy dữ liệu từ API:", p.status_code)
        return []

def yc_dich_vu(api_viotp, service_id):
    url_yc_dich_vu = f"https://api.viotp.com/request/getv2?token={api_viotp}&serviceId={service_id}"
    p = requests.get(url_yc_dich_vu)
    if p.status_code == 200:
        ss = json.loads(p.text)
        sdt = ss['data']['re_phone_number']
        id_dv = str(ss['data']['request_id'])
        return sdt, id_dv
    else:
        print("Lỗi khi lấy dữ liệu từ API:", p.status_code)
        return None, None



def code_tra_ve(request_id, token):
    url_code_tra_ve = f"https://api.viotp.com/session/getv2?requestId={request_id}&token={token}"
    p = requests.get(url_code_tra_ve)
    if p.status_code == 200:
        ss = json.loads(p.text)
        mess = ss['data']['SmsContent']
        code = ss['data']['Code']
        return mess, code
    else:
        print("Lỗi khi lấy dữ liệu từ API:", p.status_code)
        return None, None

def auto_reload(request_id, token, code_entry, mess_entry, countdown_label):
    end_time = time.time() + 300  # 5 minutes from now
    while time.time() < end_time:
        mess, code = code_tra_ve(request_id, token)
        if mess is not None and code is not None:
            code_entry.delete(0, tk.END)
            code_entry.insert(0, code)
            mess_entry.delete(0, tk.END)
            mess_entry.insert(0, mess)
        else:
            print("Không thể tải lại mã và tin nhắn")

        remaining_time = int(end_time - time.time())
        minutes, seconds = divmod(remaining_time, 60)
        countdown_label.config(text=f"{minutes:02d}:{seconds:02d}")
        time.sleep(1)  # Wait for 1 second before the next request
