import tkinter as tk
from tkinter import ttk, messagebox


class WifiPasswordViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Wi‑Fi Password Viewer")
        self.geometry("1130x650")
        self.minsize(850, 550)
        self.configure(bg="#0a0a0f")

        # ---------- Custom Fonts ----------
        self.title_font = ("Segoe UI", 14, "bold")
        self.heading_font = ("Segoe UI", 11, "bold")
        self.body_font = ("Segoe UI", 10)
        self.small_font = ("Segoe UI", 9)

        # ---------- Custom Style for ttk ----------
        style = ttk.Style(self)
        style.theme_use("clam")

        bg_dark = "#0a0a0f"
        card_bg = "#1e1e2a"
        accent = "#6366f1"
        accent_hover = "#818cf8"
        text_primary = "#f1f5f9"
        text_secondary = "#94a3b8"
        border = "#334155"

        style.configure("TFrame", background=bg_dark)
        style.configure("TLabel", background=bg_dark, foreground=text_primary, font=self.body_font)

        style.configure("Card.TLabelframe", background=card_bg, foreground=text_primary,
                        borderwidth=0, relief="flat")
        style.configure("Card.TLabelframe.Label", background=card_bg, foreground=accent,
                        font=self.heading_font, padding=(10, 5, 0, 0))

        style.configure("Accent.TButton", background=accent, foreground="white",
                        borderwidth=0, focusthickness=0, padding=(12, 6), font=self.small_font)
        style.map("Accent.TButton",
                  background=[("active", accent_hover), ("disabled", "#475569")],
                  foreground=[("disabled", "#cbd5e1")])

        style.configure("Outline.TButton", background=card_bg, foreground=text_secondary,
                        borderwidth=1, relief="solid", padding=(10, 5), font=self.small_font)
        style.map("Outline.TButton",
                  background=[("active", "#2d2d3a")],
                  foreground=[("active", text_primary)])

        style.configure("Modern.Treeview", background=card_bg, foreground=text_primary,
                        fieldbackground=card_bg, borderwidth=0, font=self.body_font,
                        rowheight=32)
        style.configure("Modern.Treeview.Heading", background="#2a2a36", foreground=accent,
                        font=self.heading_font, borderwidth=0, relief="flat")
        style.map("Modern.Treeview.Heading", background=[("active", "#2a2a36")])

        style.configure("TCheckbutton", background=bg_dark, foreground=text_secondary,
                        font=self.small_font)
        style.map("TCheckbutton", foreground=[("selected", accent)])

        style.configure("Vertical.TScrollbar", background=card_bg, troughcolor=bg_dark,
                        borderwidth=0, arrowcolor=text_secondary)

        # ---------- Main container ----------
        outer_shadow = tk.Frame(self, bg="#0a0a0f", highlightthickness=0)
        outer_shadow.pack(expand=True, fill="both", padx=20, pady=20)

        main_card = tk.Frame(outer_shadow, bg="#1e1e2a", relief="flat", bd=0)
        main_card.pack(expand=True, fill="both")

        # Header
        header = tk.Frame(main_card, bg="#1e1e2a", height=60)
        header.pack(fill="x", padx=20, pady=(15, 0))
        header.pack_propagate(False)

        title_label = tk.Label(header, text="🔐 Wi‑Fi Password Viewer", font=self.title_font,
                               fg="#f1f5f9", bg="#1e1e2a")
        title_label.pack(side="left")

        subtitle = tk.Label(header, text="Ver y copiar contraseñas de redes guardadas",
                            font=self.small_font, fg="#94a3b8", bg="#1e1e2a")
        subtitle.pack(side="left", padx=(15, 0))

        sep = tk.Frame(main_card, bg="#334155", height=1)
        sep.pack(fill="x", padx=20, pady=(10, 20))

        content = tk.Frame(main_card, bg="#1e1e2a")
        content.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        content.columnconfigure(0, weight=1, uniform="cols")
        content.columnconfigure(1, weight=2, uniform="cols")
        content.rowconfigure(0, weight=1)

        # ---------- LEFT PANEL ----------
        left_card = ttk.LabelFrame(content, text="📡 Redes disponibles", style="Card.TLabelframe", padding=10)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        refresh_btn = ttk.Button(left_card, text="⟳ Refrescar", style="Accent.TButton",
                                 command=self.load_profiles)
        refresh_btn.pack(anchor="w", pady=(0, 10))

        tree_frame = tk.Frame(left_card, bg="#1e1e2a")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("ssid",), show="headings",
                                 selectmode="browse", style="Modern.Treeview")
        self.tree.heading("ssid", text="Nombre de la red", anchor="w")
        self.tree.column("ssid", width=220, anchor="w")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=v_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        # ---------- RIGHT PANEL ----------
        right_card = ttk.LabelFrame(content, text="🔍 Información", style="Card.TLabelframe", padding=10)
        right_card.grid(row=0, column=1, sticky="nsew")

        pw_frame = tk.Frame(right_card, bg="#1e1e2a")
        pw_frame.pack(fill="x", pady=(0, 15))

        tk.Label(pw_frame, text="Contraseña:", font=self.heading_font, fg=text_primary, bg="#1e1e2a").pack(side="left",
                                                                                                           padx=(0, 10))

        self.current_password = ""
        self.pw_var = tk.StringVar(value="")
        self.show_password = tk.BooleanVar(value=False)

        # Entry con estilos forzados para modo readonly
        self.pw_entry = tk.Entry(pw_frame, textvariable=self.pw_var, font=self.body_font,
                                 state="readonly", relief="flat",
                                 disabledbackground="#2d2d3a",  # fondo cuando readonly
                                 disabledforeground=text_primary,  # texto visible
                                 highlightthickness=1, highlightcolor=accent,
                                 highlightbackground="#334155")
        self.pw_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)

        # Máscara inicial (ocultar contraseña)
        self.pw_entry.configure(show="•")

        self.copy_btn = ttk.Button(pw_frame, text="📋 Copiar", style="Outline.TButton", command=self.copy_password)
        self.copy_btn.pack(side="left", padx=(0, 8))

        self.show_chk = ttk.Checkbutton(pw_frame, text="Mostrar", variable=self.show_password,
                                        command=self.update_password_display)
        self.show_chk.pack(side="left")

        details_frame = tk.Frame(right_card, bg="#1e1e2a")
        details_frame.pack(fill="both", expand=True)

        self.details_text = tk.Text(details_frame, font=self.body_font, wrap="word",
                                    bg="#2d2d3a", fg=text_primary, relief="flat",
                                    padx=10, pady=10, insertbackground=accent,
                                    highlightthickness=1, highlightbackground="#334155",
                                    highlightcolor=accent)
        text_scroll = ttk.Scrollbar(details_frame, orient="vertical", command=self.details_text.yview,
                                    style="Vertical.TScrollbar")
        self.details_text.configure(yscrollcommand=text_scroll.set)

        self.details_text.pack(side="left", fill="both", expand=True)
        text_scroll.pack(side="right", fill="y")

        self.details_text.insert("1.0", "✨ Selecciona una red Wi‑Fi para ver sus detalles.")

        # ---------- Import utilities ----------
        try:
            from utils.commands import SHOW_WIFI_PROFILES, SHOW_WIFI_PROFILE
            from utils.execute import exec_command
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las utilidades: {e}")
            self.SHOW_WIFI_PROFILES = None
            self.SHOW_WIFI_PROFILE = None
            self.exec_command = None
            return

        self.SHOW_WIFI_PROFILES = SHOW_WIFI_PROFILES
        self.SHOW_WIFI_PROFILE = SHOW_WIFI_PROFILE
        self.exec_command = exec_command
        self.profiles = []

        self.load_profiles()

    # ---------- Methods ----------
    def update_password_display(self):
        """Alterna la máscara del campo contraseña según el Checkbutton."""
        if self.show_password.get():
            self.pw_entry.configure(show="")
        else:
            self.pw_entry.configure(show="•")
        # Forzamos la actualización del texto (aunque la máscara ya lo maneja)
        self.pw_var.set(self.current_password)

    def copy_password(self):
        if not self.current_password:
            messagebox.showinfo("Copiar", "No hay contraseña para copiar.")
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(self.current_password)
            messagebox.showinfo("Copiar", "Contraseña copiada al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar: {e}")

    def load_profiles(self):
        if not self.exec_command or not self.SHOW_WIFI_PROFILES:
            return
        try:
            output = self.exec_command(command_line=self.SHOW_WIFI_PROFILES, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo listar redes: {e}")
            return

        names = []
        for line in output.splitlines():
            if any(phrase in line for phrase in ('All User Profile', 'Perfil de todos los usuarios',
                                                 'Perfil de usuario', 'Todos los perfiles de usuario')):
                if ':' in line:
                    try:
                        names.append(line.split(':', 1)[1].strip())
                    except Exception:
                        continue
        if not names:
            for line in output.splitlines():
                if ':' in line and ('Profile' in line or 'Perfil' in line):
                    try:
                        names.append(line.split(':', 1)[1].strip())
                    except Exception:
                        continue

        self.profiles = names
        for item in self.tree.get_children():
            self.tree.delete(item)
        for name in self.profiles:
            self.tree.insert("", tk.END, values=(name,), iid=name)

        if not self.profiles:
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, "⚠️ No se encontraron redes guardadas.")
            self.current_password = ""
            self.pw_var.set("")
            self.copy_btn.state(["disabled"])

    def show_details(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        ssid = selection[0]

        if not self.exec_command or not self.SHOW_WIFI_PROFILE:
            messagebox.showerror("Error", "Funcionalidad no disponible.")
            return

        try:
            result = self.exec_command(command_line=self.SHOW_WIFI_PROFILE, arg=ssid, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener detalles: {e}")
            return

        password = ""
        for line in result.splitlines():
            if any(phrase in line for phrase in ('Key Content', 'Contenido de la clave', 'Contenido de la contraseña')):
                if ':' in line:
                    try:
                        password = line.split(':', 1)[1].strip()
                        break
                    except Exception:
                        continue

        # Actualizar contraseña
        if password:
            self.current_password = password
            self.copy_btn.state(["!disabled"])
        else:
            self.current_password = ""
            self.copy_btn.state(["disabled"])

        # Aplicar máscara según el estado actual del checkbox
        self.update_password_display()

        # Mostrar detalles en el área de texto
        self.details_text.delete("1.0", tk.END)
        display_text = f"📶 Red: {ssid}\n\n"
        display_text += "─────────────────────────────\n"
        display_text += "📄 Salida completa:\n"
        display_text += result + "\n\n"
        if not password:
            display_text += "🔑 Contraseña no encontrada (permisos o idioma del sistema)."
        self.details_text.insert(tk.END, display_text)
