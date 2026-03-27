"""
ui/creator_view.py
Vista principal de creación del proyecto Node.js + Express.
Permite elegir nombre, carpeta destino y ver el progreso de instalación.
"""

import customtkinter as ctk
import tkinter.filedialog as fd
import threading
import os
import subprocess
from pathlib import Path
import project_gen


class CreatorView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._project_path = None   # Se rellena tras crear el proyecto con éxito
        self._build_ui()

    def _build_ui(self):
        # Título
        title = ctk.CTkLabel(
            self,
            text="Nuevo proyecto",
            font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
            text_color="#E2E8F0"
        )
        title.pack(anchor="w", pady=(0, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Rellena los datos y crea tu proyecto listo para programar.",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#94A3B8"
        )
        subtitle.pack(anchor="w", pady=(0, 28))

        # ── Campo: nombre del proyecto ─────────────────────────────────────
        ctk.CTkLabel(
            self, text="Nombre del proyecto",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color="#CBD5E1", anchor="w"
        ).pack(fill="x", pady=(0, 6))

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="mi-api",
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#E2E8F0",
            height=42,
            corner_radius=8
        )
        self.name_entry.pack(fill="x", pady=(0, 20))

        # ── Campo: carpeta destino ─────────────────────────────────────────
        ctk.CTkLabel(
            self, text="Carpeta destino",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color="#CBD5E1", anchor="w"
        ).pack(fill="x", pady=(0, 6))

        path_row = ctk.CTkFrame(self, fg_color="transparent")
        path_row.pack(fill="x", pady=(0, 20))

        self.path_entry = ctk.CTkEntry(
            path_row,
            placeholder_text="C:\\Users\\tu_usuario\\proyectos",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#E2E8F0",
            height=42,
            corner_radius=8
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            path_row,
            text="Explorar",
            command=self._browse_folder,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=8,
            height=42,
            width=90
        )
        browse_btn.pack(side="left")

        # ── Botón crear ────────────────────────────────────────────────────
        self.create_btn = ctk.CTkButton(
            self,
            text="Crear proyecto",
            command=self._start_creation,
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8,
            height=48
        )
        self.create_btn.pack(fill="x", pady=(0, 24))

        # ── Log de progreso ────────────────────────────────────────────────
        self.log_frame = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=10)
        self.log_frame.pack(fill="both", expand=True)

        log_header = ctk.CTkLabel(
            self.log_frame, text="Terminal",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#475569"
        )
        log_header.pack(anchor="w", padx=14, pady=(10, 2))

        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            text_color="#94A3B8",
            wrap="word",
            state="disabled",
            corner_radius=0
        )
        self.log_text.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        # Botón "Abrir en explorador" (se muestra al final)
        self.open_btn = ctk.CTkButton(
            self,
            text="📂  Abrir carpeta del proyecto",
            command=self._open_in_explorer,
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color="#0F172A",
            hover_color="#1E293B",
            border_width=1,
            border_color="#334155",
            text_color="#94A3B8",
            corner_radius=8,
            height=40
        )
        # Se muestra solo al terminar con éxito (ver _on_success)

    # ── Acciones ──────────────────────────────────────────────────────────

    def _browse_folder(self):
        folder = fd.askdirectory(title="Selecciona la carpeta destino")
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def _start_creation(self):
        name = self.name_entry.get().strip()
        path = self.path_entry.get().strip()

        if not name:
            self._log("⚠️  Ponle un nombre al proyecto.", color="#F97316")
            return
        if not path:
            self._log("⚠️  Selecciona una carpeta destino.", color="#F97316")
            return
        if not Path(path).exists():
            self._log("⚠️  La carpeta destino no existe.", color="#F97316")
            return

        self.create_btn.configure(state="disabled", text="Creando...")
        self.open_btn.pack_forget()
        self._clear_log()

        threading.Thread(
            target=self._do_create,
            args=(name, path),
            daemon=True
        ).start()

    def _do_create(self, name, path):
        ok, result = project_gen.create_project(
            project_name=name,
            destination_path=path,
            on_log=lambda msg: self.after(0, lambda m=msg: self._log(m))
        )

        if ok:
            self._project_path = result
            self.after(0, self._on_success)
        else:
            self.after(0, lambda: self._on_error(result))

    def _on_success(self):
        self.create_btn.configure(state="normal", text="Crear proyecto")
        self.open_btn.pack(fill="x", pady=(12, 0))

    def _on_error(self, msg):
        self._log(f"\n❌ Error:\n{msg}", color="#EF4444")
        self.create_btn.configure(state="normal", text="Crear proyecto")

    def _open_in_explorer(self):
        if self._project_path and Path(self._project_path).exists():
            subprocess.Popen(f'explorer "{self._project_path}"')

    # ── Helpers de log ────────────────────────────────────────────────────

    def _log(self, message: str, color: str = "#94A3B8"):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
