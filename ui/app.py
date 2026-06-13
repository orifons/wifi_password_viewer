import tkinter as tk
from tkinter import messagebox


class WifiPasswordViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Wi-Fi Password Viewer")
        self.geometry("800x500")
        self.minsize(700, 450)

        # Contenedor principal con borde
        main = tk.Frame(self, bg="white", relief="solid", bd=0)
        main.pack(expand=True, padx=20, pady=20)

        # Cuerpo con dos columnas
        body = tk.Frame(main, bg="white")
        body.pack(fill="none", expand=True)

        body.grid_columnconfigure(0, weight=1, uniform="cols")
        body.grid_columnconfigure(1, weight=2, uniform="cols")
        body.grid_rowconfigure(0, weight=1)

        # Panel izquierdo
        left_panel = tk.Frame(body, bg="white", bd=1, relief="solid")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        left_header = tk.Label(
            left_panel,
            text="Redes Wi-Fi",
            bg="white",
            fg="black",
            font=("Arial", 11, "bold"),
            bd=2,
            relief="solid"
        )
        left_header.pack(fill="x")

        # Controles encima de la lista (refresh)
        controls = tk.Frame(left_panel, bg="white")
        controls.pack(fill="x", padx=8, pady=(6, 0))

        refresh_btn = tk.Button(controls, text="Refrescar", command=lambda: self.load_profiles())
        refresh_btn.pack(side="left")

        list_container = tk.Frame(left_panel, bg="white")
        list_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Convertir listbox en atributo para usarlo desde otros métodos
        self.listbox = tk.Listbox(
            list_container,
            font=("Arial", 11),
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(fill="both", expand=True)

        # Panel derecho
        right_panel = tk.Frame(body, bg="white", bd=3, relief="solid")
        right_panel.grid(row=0, column=1, sticky="nsew")

        right_header = tk.Label(
            right_panel,
            text="Detalles",
            bg="white",
            fg="black",
            font=("Arial", 11, "bold"),
            bd=2,
            relief="solid"
        )
        right_header.pack(fill="x")

        # -- Nuevo: fila de controles para contraseña (mostrar/ocultar y copiar)
        pw_controls = tk.Frame(right_panel, bg="white")
        pw_controls.pack(fill="x", padx=10, pady=(8, 4))

        pw_label = tk.Label(pw_controls, text="Contraseña:", bg="white", font=("Arial", 10, "bold"))
        pw_label.pack(side="left")

        # Variable para la contraseña actual y flag de visibilidad
        self.current_password = ""
        self.pw_var = tk.StringVar(value="")
        self.show_password = tk.BooleanVar(value=False)

        # Entry para mostrar la contraseña (readonly)
        # Inicialmente ocultada (mostrar='*') y readonly
        self.pw_entry = tk.Entry(pw_controls, textvariable=self.pw_var, font=("Arial", 11), bd=1, show='*')
        self.pw_entry.configure(state='readonly')
        self.pw_entry.pack(side="left", padx=(8, 6), fill="x", expand=True)

        # Botón copiar contraseña
        self.copy_btn = tk.Button(pw_controls, text="Copiar contraseña", command=self.copy_password, state='disabled')
        self.copy_btn.pack(side="left", padx=(6, 0))

        # Toggle mostrar/ocultar (Checkbutton)
        self.show_chk = tk.Checkbutton(
            pw_controls,
            text="Mostrar",
            variable=self.show_password,
            command=self.update_password_display,
            bg="white"
        )
        self.show_chk.pack(side="left", padx=(6, 0))

        # Contenedor para detalles (salida completa)
        details_container = tk.Frame(right_panel, bg="white")
        details_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.details_text = tk.Text(
            details_container,
            font=("Arial", 11),
            bd=0,
            highlightthickness=0,
            wrap="word"
        )
        self.details_text.pack(fill="both", expand=True)

        self.details_text.insert(
            "1.0",
            "Selecciona una red Wi‑Fi para mostrar aquí los detalles.\n"
        )

        # Bind en el listbox al método de mostrar detalles
        self.listbox.bind("<<ListboxSelect>>", self.show_details)

        # Importar utilidades aquí para que el módulo pueda cargarse incluso si las utils fallan
        try:
            from utils.commands import SHOW_WIFI_PROFILES, SHOW_WIFI_PROFILE
            from utils.execute import exec_command
        except Exception as e:
            # Si no se pueden importar las utilidades, informar al usuario y deshabilitar la funcionalidad
            messagebox.showerror("Error", f"No se pudieron cargar las utilidades necesarias: {e}")
            self.SHOW_WIFI_PROFILES = None
            self.SHOW_WIFI_PROFILE = None
            self.exec_command = None
            return

        self.SHOW_WIFI_PROFILES = SHOW_WIFI_PROFILES
        self.SHOW_WIFI_PROFILE = SHOW_WIFI_PROFILE
        self.exec_command = exec_command

        # Lista de perfiles cargados (SSID strings)
        self.profiles = []

        # Cargar perfiles al iniciar
        self.load_profiles()

    def update_password_display(self):
        """Actualiza la visualización del campo de contraseña según el toggle."""
        # Cambia la máscara del entry según show_password
        if self.show_password.get():
            # Mostrar texto claro
            self.pw_entry.configure(show='')
        else:
            # Ocultar con asteriscos
            self.pw_entry.configure(show='*')

        # Actualizar el valor (aunque el StringVar ya tiene el valor)
        self.pw_var.set(self.current_password if self.show_password.get() else self.current_password)

    def copy_password(self):
        """Copia la contraseña actual al portapapeles (si existe)."""
        if not self.current_password:
            messagebox.showinfo("Copiar", "No hay ninguna contraseña para copiar.")
            return

        try:
            # Usar clipboard del root
            self.clipboard_clear()
            self.clipboard_append(self.current_password)
            messagebox.showinfo("Copiar", "Contraseña copiada al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar la contraseña: {e}")

    def load_profiles(self):
        """Ejecuta el comando para listar perfiles y rellena el listbox."""
        if not self.exec_command or not self.SHOW_WIFI_PROFILES:
            return

        try:
            output = self.exec_command(command_line=self.SHOW_WIFI_PROFILES, shell=True)
        except Exception as e:
            messagebox.showerror("Error al listar redes", f"No se pudo obtener la lista de redes: {e}")
            return

        # Parseo sencillo: buscar líneas que contengan 'All User Profile' y extraer la parte después de ':',
        # soportando inglés y español
        names = []
        for line in output.splitlines():
            if ('All User Profile' in line or 'Perfil de todos los usuarios' in line or 'Perfil de usuario' in line or
                    'Todos los perfiles de usuario' in line):
                if ':' in line:
                    try:
                        names.append(line.split(':', 1)[1].strip())
                    except SystemError:
                        continue

        # Fallback: si no se encontraron con las palabras claves, intentar extraer cualquier línea con ':' que
        # parezca un perfil
        if not names:
            for line in output.splitlines():
                if ':' in line and ('Profile' in line or 'Perfil' in line):
                    try:
                        names.append(line.split(':', 1)[1].strip())
                    except SystemError:
                        continue

        # Actualizar listbox
        self.profiles = names
        self.listbox.delete(0, tk.END)
        for name in self.profiles:
            self.listbox.insert(tk.END, name)

        if not self.profiles:
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, "No se encontraron perfiles de Wi‑Fi en este sistema.")

    def show_details(self, event):
        """Muestra los detalles de la red seleccionada (ejecuta netsh para ese perfil)."""
        # event puede ser un evento de Tkinter o un string (no usado aquí)
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return

        ssid = widget.get(selection[0])

        if not self.exec_command or not self.SHOW_WIFI_PROFILE:
            messagebox.showerror("Error", "Funcionalidad no disponible.")
            return

        try:
            result = self.exec_command(command_line=self.SHOW_WIFI_PROFILE, arg=ssid, shell=True)
        except Exception as e:
            messagebox.showerror("Error al obtener detalles", f"No se pudieron obtener detalles para {ssid}: {e}")
            return

        # Buscar contraseña en la salida (soportar inglés y español)
        password = []
        for line in result.splitlines():
            if 'Key Content' in line or 'Contenido de la clave' in line or 'Contenido de la contraseña' in line:
                if ':' in line:
                    try:
                        password.append(line.split(':', 1)[1].strip())
                    except SystemError:
                        continue

        # Actualizar campo de contraseña (se muestra en el entry dedicado)
        if password:
            self.current_password = password[0]
            self.pw_var.set(self.current_password if self.show_password.get() else self.current_password)
            self.copy_btn.configure(state='normal')
        else:
            self.current_password = ""
            self.pw_var.set("")
            self.copy_btn.configure(state='disabled')

        # Mostrar resultado completo en el Text (sin repetir la línea de contraseña)
        self.details_text.delete("1.0", tk.END)
        display_text = f"Red seleccionada: {ssid}\n\n"
        display_text += "Detalles (salida completa del comando):\n"
        display_text += result + "\n\n"

        if not password:
            display_text += "Contraseña: No encontrada en la salida (verifique permisos o localización del sistema).\n"

        self.details_text.insert(tk.END, display_text)


if __name__ == "__main__":
    app = WifiPasswordViewer()
    app.mainloop()
