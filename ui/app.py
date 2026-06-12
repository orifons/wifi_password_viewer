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
                    except Exception:
                        continue

        # Fallback: si no se encontraron con las palabras claves, intentar extraer cualquier línea con ':' que
        # parezca un perfil
        if not names:
            for line in output.splitlines():
                if ':' in line and ('Profile' in line or 'Perfil' in line):
                    try:
                        names.append(line.split(':', 1)[1].strip())
                    except Exception:
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
                    except Exception:
                        continue

        # Mostrar resultado completo y, si existe, la contraseña resaltada
        self.details_text.delete("1.0", tk.END)
        display_text = f"Red seleccionada: {ssid}\n\n"
        display_text += "Detalles (salida completa del comando):\n"
        display_text += result + "\n\n"

        if password:
            display_text += f"Contraseña: {password[0]}\n"
        else:
            display_text += "Contraseña: No encontrada en la salida (verifique permisos o localización del sistema).\n"

        self.details_text.insert(tk.END, display_text)


if __name__ == "__main__":
    app = WifiPasswordViewer()
    app.mainloop()
