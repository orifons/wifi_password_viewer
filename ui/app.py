import tkinter as tk


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

        list_container = tk.Frame(left_panel, bg="white")
        list_container.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = tk.Listbox(
            list_container,
            font=("Arial", 11),
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        listbox.pack(fill="both", expand=True)

        redes = [
            "Red Wi-Fi 1",
            "Red Wi-Fi 2",
            "Red Wi-Fi 3",
            "Red Wi-Fi 4",
        ]

        for red in redes:
            listbox.insert(tk.END, red)

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

        listbox.bind("<<ListboxSelect>>", self.show_details)

    def show_details(self, event):
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return

        red = widget.get(selection[0])

        self.details_text.delete("1.0", tk.END)
        self.details_text.insert(
            tk.END,
            f"Red seleccionada: {red}\n\n"
            "Aquí puedes mostrar:\n"
            "- SSID\n"
            "- Contraseña\n"
            "- Seguridad\n"
            "- Señal\n"
        )


if __name__ == "__main__":
    app = WifiPasswordViewer()
    app.mainloop()
