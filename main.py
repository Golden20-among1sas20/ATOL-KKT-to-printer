import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import webbrowser
from libfptr10 import IFptr
import os
import re

class KKTPrinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Печать на ККТ АТОЛ")
        self.root.geometry("650x800")
        self.root.minsize(650, 800)
        
        # Настройки по умолчанию
        self.ip_address = ""
        self.ip_port = ""
        
        self.fptr = None
        
        # Сначала создаем все виджеты
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для настроек подключения
        settings_frame = ttk.LabelFrame(self.root, text="Настройки подключения", padding=10)
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Поле для IP-адреса
        ttk.Label(settings_frame, text="IP-адрес ККТ:").grid(row=0, column=0, sticky=tk.W)
        self.ip_address_entry = ttk.Entry(settings_frame)
        self.ip_address_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Поле для порта
        ttk.Label(settings_frame, text="Порт ККТ:").grid(row=1, column=0, sticky=tk.W)
        self.ip_port_entry = ttk.Entry(settings_frame)
        self.ip_port_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # Кнопка подключения
        ttk.Button(
            settings_frame,
            text="Подключиться",
            command=self.connect_to_kkt
        ).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Фрейм статуса подключения
        connection_frame = ttk.LabelFrame(self.root, text="Статус подключения", padding=10)
        connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.connection_status = ttk.Label(
            connection_frame, 
            text="Введите IP и порт ККТ", 
            foreground="blue"
        )
        self.connection_status.pack(anchor=tk.W)
        
        # Информация о ККТ
        info_frame = ttk.LabelFrame(self.root, text="Информация о ККТ", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.kkt_info_text = scrolledtext.ScrolledText(
            info_frame, 
            height=5, 
            wrap=tk.WORD,
            state='disabled'
        )
        self.kkt_info_text.pack(fill=tk.X)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка текста
        text_tab = ttk.Frame(notebook)
        notebook.add(text_tab, text="Текст")
        self.create_text_tab(text_tab)
        
        # Вкладка QR-кода
        qr_tab = ttk.Frame(notebook)
        notebook.add(qr_tab, text="QR-код")
        self.create_qr_tab(qr_tab)
        
        # Вкладка изображения
        image_tab = ttk.Frame(notebook)
        notebook.add(image_tab, text="Изображение")
        self.create_image_tab(image_tab)
        
        # Вкладка комбинированной печати
        combined_tab = ttk.Frame(notebook)
        notebook.add(combined_tab, text="Текст + QR")
        self.create_combined_tab(combined_tab)

    def validate_ip_port(self):
        """Проверка корректности IP и порта"""
        ip = self.ip_address_entry.get().strip()
        port = self.ip_port_entry.get().strip()
        
        # Проверка IP
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            messagebox.showerror("Ошибка", "Неверный формат IP-адреса")
            return False
        
        # Проверка порта
        try:
            port_num = int(port)
            if not 1 <= port_num <= 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Порт должен быть числом от 1 до 65535")
            return False
        
        self.ip_address = ip
        self.ip_port = port
        return True
    
    def create_text_tab(self, parent):
        """Создает вкладку для печати текста"""
        text_frame = ttk.LabelFrame(parent, text="Текст для печати", padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_entry = scrolledtext.ScrolledText(
            text_frame, 
            height=10, 
            wrap=tk.WORD
        )
        self.text_entry.pack(fill=tk.BOTH, expand=True)
        
        # Настройки печати текста
        settings_frame = ttk.Frame(text_frame)
        settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(settings_frame, text="Выравнивание:").grid(row=0, column=0, sticky=tk.W)
        self.alignment_var = tk.StringVar(value="center")
        ttk.Radiobutton(
            settings_frame, 
            text="По левому краю", 
            variable=self.alignment_var, 
            value="left"
        ).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(
            settings_frame, 
            text="По центру", 
            variable=self.alignment_var, 
            value="center"
        ).grid(row=0, column=2, sticky=tk.W)
        ttk.Radiobutton(
            settings_frame, 
            text="По правому краю", 
            variable=self.alignment_var, 
            value="right"
        ).grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(settings_frame, text="Перенос текста:").grid(row=1, column=0, sticky=tk.W)
        self.wrap_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame, 
            text="Включить перенос слов", 
            variable=self.wrap_var
        ).grid(row=1, column=1, columnspan=3, sticky=tk.W)
        
        ttk.Button(
            text_frame, 
            text="Печатать текст", 
            command=self.print_text
        ).pack(pady=5)
    
    def create_qr_tab(self, parent):
        """Создает вкладку для печати QR-кода"""
        qr_frame = ttk.LabelFrame(parent, text="QR-код для печати", padding=10)
        qr_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(qr_frame, text="Текст/URL для QR-кода:").pack(anchor=tk.W)
        self.qr_text_entry = ttk.Entry(qr_frame)
        self.qr_text_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(qr_frame, text="Размер QR-кода:").pack(anchor=tk.W)
        self.qr_size_var = tk.IntVar(value=5)
        ttk.Spinbox(
            qr_frame, 
            from_=1, 
            to=10, 
            textvariable=self.qr_size_var
        ).pack(fill=tk.X, pady=5)
        
        ttk.Label(qr_frame, text="Выравнивание:").pack(anchor=tk.W)
        self.qr_alignment_var = tk.StringVar(value="center")
        ttk.Radiobutton(
            qr_frame, 
            text="По левому краю", 
            variable=self.qr_alignment_var, 
            value="left"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            qr_frame, 
            text="По центру", 
            variable=self.qr_alignment_var, 
            value="center"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            qr_frame, 
            text="По правому краю", 
            variable=self.qr_alignment_var, 
            value="right"
        ).pack(anchor=tk.W)
        
        ttk.Button(
            qr_frame, 
            text="Печатать QR-код", 
            command=self.print_qr
        ).pack(pady=5)
    
    def create_image_tab(self, parent):
        """Создает вкладку для печати изображения"""
        image_frame = ttk.LabelFrame(parent, text="Изображение для печати", padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_path_var = tk.StringVar()
        ttk.Label(image_frame, text="Путь к изображению:").pack(anchor=tk.W)
        ttk.Label(image_frame, text="!!! Изображение должно быть черно-белым !!!", foreground="#FF0000").pack(anchor=tk.W)
        tk.Label(image_frame, text="Программу для преобразования фото в ЧБ можно найти в релизах на GitHub", foreground="#C4C4C4").pack(anchor=tk.W)
        githuburl = tk.Label(image_frame, text="GitHub", foreground="blue")
        githuburl.pack(anchor=tk.W)
        githuburl.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Golden20-among1sas20/ATOL-KKT-to-printer/releases"))
        
        path_frame = ttk.Frame(image_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(path_frame, textvariable=self.image_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            path_frame, 
            text="Обзор...", 
            command=self.browse_image
        ).pack(side=tk.RIGHT)
        
        ttk.Label(image_frame, text="Выравнивание:").pack(anchor=tk.W)
        self.image_alignment_var = tk.StringVar(value="center")
        ttk.Radiobutton(
            image_frame, 
            text="По левому краю", 
            variable=self.image_alignment_var, 
            value="left"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            image_frame, 
            text="По центру", 
            variable=self.image_alignment_var, 
            value="center"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            image_frame, 
            text="По правому краю", 
            variable=self.image_alignment_var, 
            value="right"
        ).pack(anchor=tk.W)
        
        self.image_scale_var = tk.IntVar(value=100)
        ttk.Label(image_frame, text=f"Масштаб: ").pack(anchor=tk.W)
        ttk.Spinbox(
            image_frame, 
            from_=50, 
            to=250, 
            textvariable=self.image_scale_var,
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            image_frame, 
            text="Печатать изображение", 
            command=self.print_image
        ).pack(pady=5)
    
    def create_combined_tab(self, parent):
        """Создает вкладку для комбинированной печати текста и QR-кода"""
        combined_frame = ttk.LabelFrame(parent, text="Текст + QR-код", padding=10)
        combined_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(combined_frame, text="Текст для печати:").pack(anchor=tk.W)
        self.combined_text_entry = scrolledtext.ScrolledText(
            combined_frame, 
            height=5, 
            wrap=tk.WORD
        )
        self.combined_text_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(combined_frame, text="Текст для QR-кода:").pack(anchor=tk.W)
        self.combined_qr_entry = ttk.Entry(combined_frame)
        self.combined_qr_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(combined_frame, text="Расположение QR-кода:").pack(anchor=tk.W)
        self.qr_position_var = tk.StringVar(value="below")
        ttk.Radiobutton(
            combined_frame, 
            text="Под текстом", 
            variable=self.qr_position_var, 
            value="below"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            combined_frame, 
            text="Рядом с текстом", 
            variable=self.qr_position_var, 
            value="right"
        ).pack(anchor=tk.W)
        
        ttk.Label(combined_frame, text="Размер QR-кода:").pack(anchor=tk.W)
        self.combined_qr_size_var = tk.IntVar(value=5)
        ttk.Spinbox(
            combined_frame, 
            from_=1, 
            to=10, 
            textvariable=self.combined_qr_size_var
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            combined_frame, 
            text="Печатать текст и QR-код", 
            command=self.print_combined
        ).pack(pady=5)
    
    def browse_image(self):
        """Выбор файла изображения"""
        filepath = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=(("Изображения", "*.png *.jpg *.bmp"), ("Все файлы", "*.*")))
        if filepath:
            self.image_path_var.set(filepath)
    
    def connect_to_kkt(self):
        """Подключение к ККТ с проверкой введенных данных"""
        if not self.validate_ip_port():
            return
            
        try:
            if self.fptr and self.fptr.isOpened():
                self.fptr.close()
            
            self.fptr = IFptr(r"C:\Program Files\ATOL\Drivers10\KKT\bin\fptr10.dll")
            
            settings = {
                IFptr.LIBFPTR_PARAM_PRINT_FOOTER: False,
                IFptr.LIBFPTR_SETTING_MODEL: IFptr.LIBFPTR_MODEL_ATOL_AUTO,
                IFptr.LIBFPTR_SETTING_PORT: IFptr.LIBFPTR_PORT_TCPIP,
                IFptr.LIBFPTR_SETTING_IPADDRESS: self.ip_address,
                IFptr.LIBFPTR_SETTING_IPPORT: self.ip_port
            }
            self.fptr.setSettings(settings)
            self.fptr.open()
            
            # Обновляем информацию о ККТ
            self.update_kkt_info()
            self.connection_status.config(text="Подключено", foreground="green")
            
        except Exception as e:
            error_msg = f"Ошибка подключения: {str(e)}"
            self.connection_status.config(text=error_msg, foreground="red")
            self.update_kkt_info(error_msg)
            messagebox.showerror("Ошибка подключения", error_msg)

    def update_kkt_info(self, text=None):
        """Обновление информации о ККТ"""
        if text is None:
            try:
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_STATUS)
                self.fptr.queryData()
                
                kkt_name = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_MODEL_NAME)
                serial_number = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_SERIAL_NUMBER)
                
                text = (
                    f"Модель: {kkt_name}\n"
                    f"Серийный номер: {serial_number}\n"
                    f"IP: {self.ip_address}:{self.ip_port}\n"
                    f"Статус: Подключено"
                )
            except Exception as e:
                text = f"Ошибка получения информации: {str(e)}"
        
        self.kkt_info_text.config(state='normal')
        self.kkt_info_text.delete(1.0, tk.END)
        self.kkt_info_text.insert(tk.END, text)
        self.kkt_info_text.config(state='disabled')
    
    def print_text(self):
        """Печать текста на ККТ"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror("Ошибка", "Нет подключения к ККТ")
            return
        
        text_to_print = self.text_entry.get("1.0", tk.END).strip()
        if not text_to_print:
            messagebox.showwarning("Предупреждение", "Введите текст для печати")
            return
        
        try:
            self.fptr.beginNonfiscalDocument()
            # Устанавливаем параметры печати
            alignment = {
                "left": IFptr.LIBFPTR_ALIGNMENT_LEFT,
                "center": IFptr.LIBFPTR_ALIGNMENT_CENTER,
                "right": IFptr.LIBFPTR_ALIGNMENT_RIGHT
            }[self.alignment_var.get()]
            
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT, text_to_print)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, alignment)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT_WRAP, 
                              IFptr.LIBFPTR_TW_WORDS if self.wrap_var.get() else IFptr.LIBFPTR_TW_NONE)
            
            # Печатаем текст
            result = self.fptr.printText()
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
            self.fptr.endNonfiscalDocument()
            if result == 0:
                messagebox.showinfo("Успех", "Текст успешно отправлен на печать")
            else:
                messagebox.showerror("Ошибка", f"Ошибка печати. Код ошибки: {result}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при печати текста: {str(e)}")
    
    def print_qr(self):
        """Печать QR-кода"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror("Ошибка", "Нет подключения к ККТ")
            return
        
        qr_text = self.qr_text_entry.get().strip()
        if not qr_text:
            messagebox.showwarning("Предупреждение", "Введите текст для QR-кода")
            return
        
        try:
            self.fptr.beginNonfiscalDocument()
            # Устанавливаем параметры печати QR-кода
            alignment = {
                "left": IFptr.LIBFPTR_ALIGNMENT_LEFT,
                "center": IFptr.LIBFPTR_ALIGNMENT_CENTER,
                "right": IFptr.LIBFPTR_ALIGNMENT_RIGHT
            }[self.qr_alignment_var.get()]
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_BARCODE_TYPE, IFptr.LIBFPTR_BT_QR)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_BARCODE, qr_text)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, alignment)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_SCALE, self.qr_size_var.get())
            
            # Печатаем QR-код
            result = self.fptr.printBarcode()
            if result == 0:
                messagebox.showinfo("Успех", "QR-код успешно отправлен на печать")
            else:
                messagebox.showerror("Ошибка", f"Ошибка печати QR-кода. Код ошибки: {result}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при печати QR-кода: {str(e)}")

        self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
        self.fptr.endNonfiscalDocument()
    
    def print_image(self):
        """Печать изображения"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror("Ошибка", "Нет подключения к ККТ")
            return
        
        image_path = self.image_path_var.get()
        if not image_path or not os.path.exists(image_path):
            messagebox.showwarning("Предупреждение", "Выберите существующий файл изображения")
            return
        
        try:
            # Устанавливаем параметры печати изображения
            self.fptr.beginNonfiscalDocument()
            alignment = {
                "left": IFptr.LIBFPTR_ALIGNMENT_LEFT,
                "center": IFptr.LIBFPTR_ALIGNMENT_CENTER,
                "right": IFptr.LIBFPTR_ALIGNMENT_RIGHT
            }[self.image_alignment_var.get()]
            
            scale = self.image_scale_var.get() / 100.0
            
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, alignment)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_SCALE, scale)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_FILENAME, image_path)
            
            # Печатаем изображение
            result = self.fptr.printPicture()
            if result == 0:
                messagebox.showinfo("Успех", "Изображение успешно отправлено на печать")
            else:
                messagebox.showerror("Ошибка", f"Ошибка печати изображения. Код ошибки: {result}")
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
            self.fptr.endNonfiscalDocument()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при печати изображения: {str(e)}")
    
    def print_combined(self):
        """Печать текста и QR-кода вместе"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror("Ошибка", "Нет подключения к ККТ")
            return
        
        text_to_print = self.combined_text_entry.get("1.0", tk.END).strip()
        qr_text = self.combined_qr_entry.get().strip()
        
        if not text_to_print and not qr_text:
            messagebox.showwarning("Предупреждение", "Введите текст и/или текст для QR-кода")
            return
        
        try:
            self.fptr.beginNonfiscalDocument()
            # Печатаем текст (если есть)
            if text_to_print:
                if self.qr_position_var.get() == "right":
                    self.fptr.setParam(IFptr.LIBFPTR_PARAM_DEFER, IFptr.LIBFPTR_DEFER_OVERLAY)
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT, text_to_print)
                
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, IFptr.LIBFPTR_ALIGNMENT_LEFT)
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT_WRAP, IFptr.LIBFPTR_TW_WORDS)
                self.fptr.printText()
            
            # Печатаем QR-код (если есть)
            if qr_text:
                # Устанавливаем положение QR-кода
                if self.qr_position_var.get() == "right":
                    self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, IFptr.LIBFPTR_ALIGNMENT_RIGHT)
                else:
                    self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, IFptr.LIBFPTR_ALIGNMENT_CENTER)
                
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_BARCODE, qr_text)
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_BARCODE_TYPE, IFptr.LIBFPTR_BT_QR)
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_SCALE, self.combined_qr_size_var.get())
                self.fptr.printBarcode()
            
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
            self.fptr.endNonfiscalDocument()
            
            messagebox.showinfo("Успех", "Текст и QR-код успешно отправлены на печать")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при печати: {str(e)}")
    
    def on_closing(self):
        """Действия при закрытии окна"""
        if self.fptr and self.fptr.isOpened():
            self.fptr.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KKTPrinterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
