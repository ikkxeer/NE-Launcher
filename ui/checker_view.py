"""
ui/checker_view.py
Vista de verificación de dependencias (Node.js y npm).
Muestra el estado de cada herramienta y opciones si falta alguna.
"""

import customtkinter as ctk
import threading
import checker


class CheckerView(ctk.CTkFrame):

    def __init__(self, parent, on_ready_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_ready_callback = on_ready_callback
        self._build_ui()
        # Lanzar verificación automáticamente al mostrar la vista
        self.after(300, self._run_check)

    def _build_ui(self):
        # Título de sección
        title = ctk.CTkLabel(
            self,
            text="Verificación del entorno",
            font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
            text_color="#E2E8F0"
        )
        title.pack(anchor="w", pady=(0, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Comprobando que tienes todo lo necesario para trabajar.",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#94A3B8"
        )
        subtitle.pack(anchor="w", pady=(0, 28))

        # Tarjeta Node.js
        self.node_card = _DependencyCard(self, name="Node.js", description="Entorno de ejecución JavaScript")
        self.node_card.pack(fill="x", pady=(0, 12))

        # Tarjeta npm
        self.npm_card = _DependencyCard(self, name="npm", description="Gestor de paquetes de Node.js")
        self.npm_card.pack(fill="x", pady=(0, 24))

        # Área de acciones (botón instalar / continuar)
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(fill="x")

        self.status_label = ctk.CTkLabel(
            self.action_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color="#94A3B8"
        )
        self.status_label.pack(anchor="w", pady=(0, 12))

        self.install_btn = ctk.CTkButton(
            self.action_frame,
            text="Descargar Node.js",
            command=checker.open_node_download_page,
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            fg_color="#F97316",
            hover_color="#EA580C",
            corner_radius=8,
            height=42,
        )

        self.recheck_btn = ctk.CTkButton(
            self.action_frame,
            text="Volver a verificar",
            command=self._run_check,
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color="#334155",
            hover_color="#475569",
            corner_radius=8,
            height=42,
        )

        self.continue_btn = ctk.CTkButton(
            self.action_frame,
            text="Continuar →",
            command=self.on_ready_callback,
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            fg_color="#22C55E",
            hover_color="#16A34A",
            corner_radius=8,
            height=42,
        )

    def _run_check(self):
        """Lanza la verificación en un hilo para no bloquear la UI."""
        self.status_label.configure(text="🔍 Verificando...", text_color="#94A3B8")
        self.install_btn.pack_forget()
        self.recheck_btn.pack_forget()
        self.continue_btn.pack_forget()
        self.node_card.set_checking()
        self.npm_card.set_checking()

        threading.Thread(target=self._do_check, daemon=True).start()

    def _do_check(self):
        status = checker.get_status()
        # Actualizar UI desde el hilo principal
        self.after(0, lambda: self._update_ui(status))

    def _update_ui(self, status):
        node = status["node"]
        npm = status["npm"]

        self.node_card.set_result(node["installed"], node["version"])
        self.npm_card.set_result(npm["installed"], npm["version"])

        if status["ready"]:
            self.status_label.configure(
                text="✅ Todo listo. Puedes crear tu proyecto.",
                text_color="#22C55E"
            )
            self.continue_btn.pack(side="left")
        else:
            self.status_label.configure(
                text="⚠️  Instala Node.js (incluye npm) y vuelve a verificar.",
                text_color="#F97316"
            )
            self.install_btn.pack(side="left", padx=(0, 10))
            self.recheck_btn.pack(side="left")


class _DependencyCard(ctk.CTkFrame):
    """Tarjeta individual que muestra el estado de una dependencia."""

    def __init__(self, parent, name: str, description: str):
        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=10,
        )
        self.name = name

        # Indicador de estado (circulito de color)
        self.indicator = ctk.CTkLabel(
            self, text="●", width=24,
            font=ctk.CTkFont(size=18),
            text_color="#475569"
        )
        self.indicator.pack(side="left", padx=(16, 12), pady=16)

        # Info de texto
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, pady=16)

        self.name_label = ctk.CTkLabel(
            text_frame, text=name,
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            text_color="#E2E8F0", anchor="w"
        )
        self.name_label.pack(anchor="w")

        self.desc_label = ctk.CTkLabel(
            text_frame, text=description,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#64748B", anchor="w"
        )
        self.desc_label.pack(anchor="w")

        # Badge de versión / estado
        self.badge = ctk.CTkLabel(
            self, text="...",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#94A3B8",
            width=100, anchor="e"
        )
        self.badge.pack(side="right", padx=16)

    def set_checking(self):
        self.indicator.configure(text_color="#475569")
        self.badge.configure(text="verificando...", text_color="#94A3B8")

    def set_result(self, installed: bool, version: str):
        if installed:
            self.indicator.configure(text_color="#22C55E")
            self.badge.configure(text=version, text_color="#22C55E")
        else:
            self.indicator.configure(text_color="#EF4444")
            self.badge.configure(text="No instalado", text_color="#EF4444")
