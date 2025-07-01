import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import webbrowser
from libfptr10 import IFptr
import os
import re
import json
from pathlib import Path

class KKTPrinterApp:
    def __init__(self, root):
        self.root = root
        self.config_file = Path("atol_printer_config.json")
        self.translations_file = Path("translations.json")
        self.load_config()
        self.load_translations()
        
        self.current_lang = self.config.get("language", "ru")
        self.root.title(self.tr("title"))
        self.root.geometry("650x800")
        self.root.minsize(650, 800)
        
        # Default settings
        self.ip_address = self.config.get("ip_address", "")
        self.ip_port = self.config.get("ip_port", "")
        
        self.fptr = None
        
        # Create menu
        self.create_menu()
        # Create widgets
        self.create_widgets()
    
    def load_translations(self):
        """Load translations from JSON file"""
        default_translations = {
            "ru": {
                "title": "Печать на ККТ АТОЛ",
                "connection_settings": "Настройки подключения",
                "ip_label": "IP-адрес ККТ:",
                "port_label": "Порт ККТ:",
                "connect_btn": "Подключиться",
                "connection_status": "Статус подключения",
                "not_connected": "Введите IP и порт ККТ",
                "connected": "Подключено",
                "connection_error": "Ошибка подключения",
                "kkt_info": "Информация о ККТ",
                "model": "Модель",
                "serial": "Серийный номер",
                "status": "Статус",
                "text_tab": "Текст",
                "text_to_print": "Текст для печати",
                "alignment": "Выравнивание:",
                "left": "По левому краю",
                "center": "По центру",
                "right": "По правому краю",
                "word_wrap": "Перенос текста:",
                "enable_word_wrap": "Включить перенос слов",
                "print_text": "Печатать текст",
                "qr_tab": "QR-код",
                "qr_text": "Текст/URL для QR-кода:",
                "qr_size": "Размер QR-кода:",
                "print_qr": "Печатать QR-код",
                "image_tab": "Изображение",
                "image_path": "Путь к изображению:",
                "bw_warning": "!!! Изображение должно быть черно-белым !!!",
                "github_tool": "Программу для преобразования фото в ЧБ можно найти в релизах на GitHub",
                "browse": "Обзор...",
                "scale": "Масштаб:",
                "print_image": "Печатать изображение",
                "combined_tab": "Текст + QR",
                "text_for_print": "Текст для печати:",
                "qr_position": "Расположение QR-кода:",
                "below": "Под текстом",
                "side": "Рядом с текстом",
                "print_combined": "Печатать текст и QR-код",
                "error": "Ошибка",
                "warning": "Предупреждение",
                "success": "Успех",
                "invalid_ip": "Неверный формат IP-адреса",
                "invalid_port": "Порт должен быть числом от 1 до 65535",
                "enter_ip_port": "Введите IP-адрес и порт",
                "settings_saved": "Настройки сохранены",
                "enter_text": "Введите текст для печати",
                "text_printed": "Текст успешно отправлен на печать",
                "print_error": "Ошибка печати. Код ошибки:",
                "enter_qr": "Введите текст для QR-кода",
                "qr_printed": "QR-код успешно отправлен на печать",
                "select_image": "Выберите существующий файл изображения",
                "image_printed": "Изображение успешно отправлено на печать",
                "enter_text_or_qr": "Введите текст и/или текст для QR-кода",
                "combined_printed": "Текст и QR-код успешно отправлены на печать",
                "language": "Язык",
                "russian": "Русский",
                "english": "English",
                "get_info_error": "Ошибка получения информации:"
            },
            "en": {
                "title": "ATOL KKT Printing",
                "connection_settings": "Connection Settings",
                "ip_label": "KKT IP Address:",
                "port_label": "KKT Port:",
                "connect_btn": "Connect",
                "connection_status": "Connection Status",
                "not_connected": "Enter KKT IP and port",
                "connected": "Connected",
                "connection_error": "Connection error",
                "kkt_info": "KKT Information",
                "model": "Model",
                "serial": "Serial number",
                "status": "Status",
                "text_tab": "Text",
                "text_to_print": "Text to print",
                "alignment": "Alignment:",
                "left": "Left",
                "center": "Center",
                "right": "Right",
                "word_wrap": "Word wrap:",
                "enable_word_wrap": "Enable word wrap",
                "print_text": "Print text",
                "qr_tab": "QR Code",
                "qr_text": "QR Code Text/URL:",
                "qr_size": "QR Code Size:",
                "print_qr": "Print QR Code",
                "image_tab": "Image",
                "image_path": "Image path:",
                "bw_warning": "!!! Image must be black and white !!!",
                "github_tool": "You can find image converter tool in GitHub releases",
                "browse": "Browse...",
                "scale": "Scale:",
                "print_image": "Print image",
                "combined_tab": "Text + QR",
                "text_for_print": "Text to print:",
                "qr_position": "QR Code position:",
                "below": "Below text",
                "side": "Side by side",
                "print_combined": "Print text and QR code",
                "error": "Error",
                "warning": "Warning",
                "success": "Success",
                "invalid_ip": "Invalid IP address format",
                "invalid_port": "Port must be a number between 1 and 65535",
                "enter_ip_port": "Enter IP address and port",
                "settings_saved": "Settings saved",
                "enter_text": "Enter text to print",
                "text_printed": "Text sent to printer successfully",
                "print_error": "Print error. Error code:",
                "enter_qr": "Enter text for QR code",
                "qr_printed": "QR code sent to printer successfully",
                "select_image": "Select existing image file",
                "image_printed": "Image sent to printer successfully",
                "enter_text_or_qr": "Enter text and/or QR code text",
                "combined_printed": "Text and QR code sent to printer successfully",
                "language": "Language",
                "russian": "Russian",
                "english": "English",
                "get_info_error": "Error getting information:"
            }
        }
        
        try:
            if self.translations_file.exists():
                with open(self.translations_file, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
            else:
                self.translations = default_translations
                with open(self.translations_file, "w", encoding="utf-8") as f:
                    json.dump(default_translations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error loading translations: {e}")
            self.translations = default_translations
    
    def tr(self, key):
        """Get translation for current language"""
        try:
            return self.translations[self.current_lang].get(key, key)
        except:
            return key
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            else:
                self.config = {}
        except Exception:
            self.config = {}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def create_menu(self):
        """Create language selection menu"""
        menubar = tk.Menu(self.root)
        
        # Language menu
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label=self.tr("russian"), command=lambda: self.set_language("ru"))
        lang_menu.add_command(label=self.tr("english"), command=lambda: self.set_language("en"))
        
        menubar.add_cascade(label=self.tr("language"), menu=lang_menu)
        self.root.config(menu=menubar)
    
    def set_language(self, lang):
        """Set interface language"""
        if lang in self.translations:
            self.current_lang = lang
            self.config["language"] = lang
            self.save_config()
            self.update_ui_language()
    
    def update_ui_language(self):
        """Update interface text when language changes"""
        self.root.title(self.tr("title"))
        
        # Update all widgets that store references
        if hasattr(self, 'settings_frame'):
            self.settings_frame.config(text=self.tr("connection_settings"))
        if hasattr(self, 'connection_frame'):
            self.connection_frame.config(text=self.tr("connection_status"))
        if hasattr(self, 'info_frame'):
            self.info_frame.config(text=self.tr("kkt_info"))
        
        # Update notebook tabs
        if hasattr(self, 'notebook'):
            for tab_id in range(self.notebook.index("end")):
                tab_text = self.notebook.tab(tab_id, "text")
                # Find translation key for this tab text
                for key, translations in self.translations.items():
                    for lang, text in translations.items():
                        if text == tab_text:
                            self.notebook.tab(tab_id, text=self.tr(key))
                            break
        
        # Update other widgets as needed...
        # This would need to be expanded to update all UI elements
    
    def create_widgets(self):
        # Connection settings frame
        self.settings_frame = ttk.LabelFrame(self.root, text=self.tr("connection_settings"), padding=10)
        self.settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # IP address field
        ttk.Label(self.settings_frame, text=self.tr("ip_label")).grid(row=0, column=0, sticky=tk.W)
        self.ip_address_entry = ttk.Entry(self.settings_frame)
        self.ip_address_entry.insert(0, self.ip_address)
        self.ip_address_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Port field
        ttk.Label(self.settings_frame, text=self.tr("port_label")).grid(row=1, column=0, sticky=tk.W)
        self.ip_port_entry = ttk.Entry(self.settings_frame)
        self.ip_port_entry.insert(0, self.ip_port)
        self.ip_port_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # Connect button
        ttk.Button(
            self.settings_frame,
            text=self.tr("connect_btn"),
            command=self.connect_to_kkt
        ).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Connection status frame
        self.connection_frame = ttk.LabelFrame(self.root, text=self.tr("connection_status"), padding=10)
        self.connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.connection_status = ttk.Label(
            self.connection_frame, 
            text=self.tr("not_connected"), 
            foreground="blue"
        )
        self.connection_status.pack(anchor=tk.W)
        
        # KKT info frame
        self.info_frame = ttk.LabelFrame(self.root, text=self.tr("kkt_info"), padding=10)
        self.info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.kkt_info_text = scrolledtext.ScrolledText(
            self.info_frame, 
            height=5, 
            wrap=tk.WORD,
            state='disabled'
        )
        self.kkt_info_text.pack(fill=tk.X)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text tab
        text_tab = ttk.Frame(self.notebook)
        self.notebook.add(text_tab, text=self.tr("text_tab"))
        self.create_text_tab(text_tab)
        
        # QR tab
        qr_tab = ttk.Frame(self.notebook)
        self.notebook.add(qr_tab, text=self.tr("qr_tab"))
        self.create_qr_tab(qr_tab)
        
        # Image tab
        image_tab = ttk.Frame(self.notebook)
        self.notebook.add(image_tab, text=self.tr("image_tab"))
        self.create_image_tab(image_tab)
        
        # Combined tab
        combined_tab = ttk.Frame(self.notebook)
        self.notebook.add(combined_tab, text=self.tr("combined_tab"))
        self.create_combined_tab(combined_tab)

    def validate_ip_port(self):
        """Validate IP and port"""
        ip = self.ip_address_entry.get().strip()
        port = self.ip_port_entry.get().strip()
        
        # IP validation
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            messagebox.showerror(self.tr("error"), self.tr("invalid_ip"))
            return False
        
        # Port validation
        try:
            port_num = int(port)
            if not 1 <= port_num <= 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.tr("error"), self.tr("invalid_port"))
            return False
        
        self.ip_address = ip
        self.ip_port = port
        return True
    
    def create_text_tab(self, parent):
        """Create text printing tab"""
        text_frame = ttk.LabelFrame(parent, text=self.tr("text_to_print"), padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_entry = scrolledtext.ScrolledText(
            text_frame, 
            height=10, 
            wrap=tk.WORD
        )
        self.text_entry.pack(fill=tk.BOTH, expand=True)
        
        # Text printing settings
        settings_frame = ttk.Frame(text_frame)
        settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(settings_frame, text=self.tr("alignment")).grid(row=0, column=0, sticky=tk.W)
        self.alignment_var = tk.StringVar(value="center")
        ttk.Radiobutton(
            settings_frame, 
            text=self.tr("left"), 
            variable=self.alignment_var, 
            value="left"
        ).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(
            settings_frame, 
            text=self.tr("center"), 
            variable=self.alignment_var, 
            value="center"
        ).grid(row=0, column=2, sticky=tk.W)
        ttk.Radiobutton(
            settings_frame, 
            text=self.tr("right"), 
            variable=self.alignment_var, 
            value="right"
        ).grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(settings_frame, text=self.tr("word_wrap")).grid(row=1, column=0, sticky=tk.W)
        self.wrap_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame, 
            text=self.tr("enable_word_wrap"), 
            variable=self.wrap_var
        ).grid(row=1, column=1, columnspan=3, sticky=tk.W)
        
        ttk.Button(
            text_frame, 
            text=self.tr("print_text"), 
            command=self.print_text
        ).pack(pady=5)
    
    def create_qr_tab(self, parent):
        """Create QR code printing tab"""
        qr_frame = ttk.LabelFrame(parent, text=self.tr("qr_tab"), padding=10)
        qr_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(qr_frame, text=self.tr("qr_text")).pack(anchor=tk.W)
        self.qr_text_entry = ttk.Entry(qr_frame)
        self.qr_text_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(qr_frame, text=self.tr("qr_size")).pack(anchor=tk.W)
        self.qr_size_var = tk.IntVar(value=5)
        ttk.Spinbox(
            qr_frame, 
            from_=1, 
            to=10, 
            textvariable=self.qr_size_var
        ).pack(fill=tk.X, pady=5)
        
        ttk.Label(qr_frame, text=self.tr("alignment")).pack(anchor=tk.W)
        self.qr_alignment_var = tk.StringVar(value="center")
        ttk.Radiobutton(
            qr_frame, 
            text=self.tr("left"), 
            variable=self.qr_alignment_var, 
            value="left"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            qr_frame, 
            text=self.tr("center"), 
            variable=self.qr_alignment_var, 
            value="center"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            qr_frame, 
            text=self.tr("right"), 
            variable=self.qr_alignment_var, 
            value="right"
        ).pack(anchor=tk.W)
        
        ttk.Button(
            qr_frame, 
            text=self.tr("print_qr"), 
            command=self.print_qr
        ).pack(pady=5)
    
    def create_image_tab(self, parent):
        """Create image printing tab"""
        image_frame = ttk.LabelFrame(parent, text=self.tr("image_tab"), padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_path_var = tk.StringVar()
        ttk.Label(image_frame, text=self.tr("image_path")).pack(anchor=tk.W)
        ttk.Label(image_frame, text=self.tr("bw_warning"), foreground="#FF0000").pack(anchor=tk.W)
        tk.Label(image_frame, text=self.tr("github_tool"), foreground="#C4C4C4").pack(anchor=tk.W)
        githuburl = tk.Label(image_frame, text="GitHub", foreground="blue")
        githuburl.pack(anchor=tk.W)
        githuburl.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Golden20-among1sas20/ATOL-KKT-to-printer/releases"))
        
        path_frame = ttk.Frame(image_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(path_frame, textvariable=self.image_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            path_frame, 
            text=self.tr("browse"), 
            command=self.browse_image
        ).pack(side=tk.RIGHT)
        
        ttk.Label(image_frame, text=self.tr("alignment")).pack(anchor=tk.W)
        self.image_alignment_var = tk.StringVar(value="center")
        ttk.Radiobutton(
            image_frame, 
            text=self.tr("left"), 
            variable=self.image_alignment_var, 
            value="left"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            image_frame, 
            text=self.tr("center"), 
            variable=self.image_alignment_var, 
            value="center"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            image_frame, 
            text=self.tr("right"), 
            variable=self.image_alignment_var, 
            value="right"
        ).pack(anchor=tk.W)
        
        self.image_scale_var = tk.IntVar(value=100)
        ttk.Label(image_frame, text=self.tr("scale")).pack(anchor=tk.W)
        ttk.Spinbox(
            image_frame, 
            from_=50, 
            to=250, 
            textvariable=self.image_scale_var,
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            image_frame, 
            text=self.tr("print_image"), 
            command=self.print_image
        ).pack(pady=5)
    
    def create_combined_tab(self, parent):
        """Create combined text+QR printing tab"""
        combined_frame = ttk.LabelFrame(parent, text=self.tr("combined_tab"), padding=10)
        combined_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(combined_frame, text=self.tr("text_for_print")).pack(anchor=tk.W)
        self.combined_text_entry = scrolledtext.ScrolledText(
            combined_frame, 
            height=5, 
            wrap=tk.WORD
        )
        self.combined_text_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(combined_frame, text=self.tr("qr_text")).pack(anchor=tk.W)
        self.combined_qr_entry = ttk.Entry(combined_frame)
        self.combined_qr_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(combined_frame, text=self.tr("qr_position")).pack(anchor=tk.W)
        self.qr_position_var = tk.StringVar(value="below")
        ttk.Radiobutton(
            combined_frame, 
            text=self.tr("below"), 
            variable=self.qr_position_var, 
            value="below"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            combined_frame, 
            text=self.tr("side"), 
            variable=self.qr_position_var, 
            value="right"
        ).pack(anchor=tk.W)
        
        ttk.Label(combined_frame, text=self.tr("qr_size")).pack(anchor=tk.W)
        self.combined_qr_size_var = tk.IntVar(value=5)
        ttk.Spinbox(
            combined_frame, 
            from_=1, 
            to=10, 
            textvariable=self.combined_qr_size_var
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            combined_frame, 
            text=self.tr("print_combined"), 
            command=self.print_combined
        ).pack(pady=5)
    
    def browse_image(self):
        """Browse for image file"""
        filepath = filedialog.askopenfilename(
            title=self.tr("select_image"),
            filetypes=(("Images", "*.png *.jpg *.bmp"), ("All files", "*.*")))
        if filepath:
            self.image_path_var.set(filepath)
    
    def connect_to_kkt(self):
        """Connect to KKT with validation"""
        if not self.validate_ip_port():
            return
            
        try:
            # Save settings
            self.config["ip_address"] = self.ip_address
            self.config["ip_port"] = self.ip_port
            self.save_config()
            
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
            
            self.update_kkt_info()
            self.connection_status.config(text=self.tr("connected"), foreground="green")
            
        except Exception as e:
            error_msg = f"{self.tr('connection_error')}: {str(e)}"
            self.connection_status.config(text=error_msg, foreground="red")
            self.update_kkt_info(error_msg)
            messagebox.showerror(self.tr("error"), error_msg)

    def update_kkt_info(self, text=None):
        """Update KKT information display"""
        if text is None:
            try:
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_STATUS)
                self.fptr.queryData()
                
                kkt_name = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_MODEL_NAME)
                serial_number = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_SERIAL_NUMBER)
                
                text = (
                    f"{self.tr('model')}: {kkt_name}\n"
                    f"{self.tr('serial')}: {serial_number}\n"
                    f"IP: {self.ip_address}:{self.ip_port}\n"
                    f"{self.tr('status')}: {self.tr('connected')}"
                )
            except Exception as e:
                text = f"{self.tr('get_info_error')} {str(e)}"
        
        self.kkt_info_text.config(state='normal')
        self.kkt_info_text.delete(1.0, tk.END)
        self.kkt_info_text.insert(tk.END, text)
        self.kkt_info_text.config(state='disabled')
    
    def print_text(self):
        """Print text on KKT"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror(self.tr("error"), self.tr("not_connected"))
            return
        
        text_to_print = self.text_entry.get("1.0", tk.END).strip()
        if not text_to_print:
            messagebox.showwarning(self.tr("warning"), self.tr("enter_text"))
            return
        
        try:
            self.fptr.beginNonfiscalDocument()
            # Set print parameters
            alignment = {
                "left": IFptr.LIBFPTR_ALIGNMENT_LEFT,
                "center": IFptr.LIBFPTR_ALIGNMENT_CENTER,
                "right": IFptr.LIBFPTR_ALIGNMENT_RIGHT
            }[self.alignment_var.get()]
            
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT, text_to_print)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, alignment)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT_WRAP, 
                              IFptr.LIBFPTR_TW_WORDS if self.wrap_var.get() else IFptr.LIBFPTR_TW_NONE)
            
            # Print text
            result = self.fptr.printText()
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
            self.fptr.endNonfiscalDocument()
            if result == 0:
                messagebox.showinfo(self.tr("success"), self.tr("text_printed"))
            else:
                messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {result}")
                
        except Exception as e:
            messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {str(e)}")
    
    def print_qr(self):
        """Print QR code"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror(self.tr("error"), self.tr("not_connected"))
            return
        
        qr_text = self.qr_text_entry.get().strip()
        if not qr_text:
            messagebox.showwarning(self.tr("warning"), self.tr("enter_qr"))
            return
        
        try:
            self.fptr.beginNonfiscalDocument()
            # Set QR print parameters
            alignment = {
                "left": IFptr.LIBFPTR_ALIGNMENT_LEFT,
                "center": IFptr.LIBFPTR_ALIGNMENT_CENTER,
                "right": IFptr.LIBFPTR_ALIGNMENT_RIGHT
            }[self.qr_alignment_var.get()]
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_BARCODE_TYPE, IFptr.LIBFPTR_BT_QR)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_BARCODE, qr_text)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, alignment)
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_SCALE, self.qr_size_var.get())
            
            # Print QR code
            result = self.fptr.printBarcode()
            if result == 0:
                messagebox.showinfo(self.tr("success"), self.tr("qr_printed"))
            else:
                messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {result}")
                
        except Exception as e:
            messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {str(e)}")

        self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
        self.fptr.endNonfiscalDocument()
    
    def print_image(self):
        """Print image"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror(self.tr("error"), self.tr("not_connected"))
            return
        
        image_path = self.image_path_var.get()
        if not image_path or not os.path.exists(image_path):
            messagebox.showwarning(self.tr("warning"), self.tr("select_image"))
            return
        
        try:
            # Set image print parameters
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
            
            # Print image
            result = self.fptr.printPicture()
            if result == 0:
                messagebox.showinfo(self.tr("success"), self.tr("image_printed"))
            else:
                messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {result}")
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_PRINT_FOOTER, False)
            self.fptr.endNonfiscalDocument()
        except Exception as e:
            messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {str(e)}")
    
    def print_combined(self):
        """Print text and QR code together"""
        if not self.fptr or not self.fptr.isOpened():
            messagebox.showerror(self.tr("error"), self.tr("not_connected"))
            return
        
        text_to_print = self.combined_text_entry.get("1.0", tk.END).strip()
        qr_text = self.combined_qr_entry.get().strip()
        
        if not text_to_print and not qr_text:
            messagebox.showwarning(self.tr("warning"), self.tr("enter_text_or_qr"))
            return
        
        try:
            self.fptr.beginNonfiscalDocument()
            # Print text (if any)
            if text_to_print:
                if self.qr_position_var.get() == "right":
                    self.fptr.setParam(IFptr.LIBFPTR_PARAM_DEFER, IFptr.LIBFPTR_DEFER_OVERLAY)
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT, text_to_print)
                
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_ALIGNMENT, IFptr.LIBFPTR_ALIGNMENT_LEFT)
                self.fptr.setParam(IFptr.LIBFPTR_PARAM_TEXT_WRAP, IFptr.LIBFPTR_TW_WORDS)
                self.fptr.printText()
            
            # Print QR code (if any)
            if qr_text:
                # Set QR position
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
            
            messagebox.showinfo(self.tr("success"), self.tr("combined_printed"))
                
        except Exception as e:
            messagebox.showerror(self.tr("error"), f"{self.tr('print_error')} {str(e)}")
    
    def on_closing(self):
        """Actions when closing window"""
        if self.fptr and self.fptr.isOpened():
            self.fptr.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KKTPrinterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()