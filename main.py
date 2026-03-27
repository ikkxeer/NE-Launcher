"""
main.py
Punto de entrada de la aplicación.
Crea la ventana principal con la barra lateral y gestiona la navegación entre vistas.
"""

import customtkinter as ctk
from ui.checker_view import CheckerView
from ui.creator_view import CreatorView


# Configuración de apariencia global de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Node Express Launcher")
        self.geometry("860x580")
        self.minsize(760, 520)
        self.configure(fg_color="#0F172A")
        self._build_layout()
        # Mostrar la vista de verificación al arrancar
        self._show_checker()

    def _build_layout(self):
        """Construye el layout base: sidebar izquierdo + área de contenido."""

        # ── Sidebar ───────────────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#0D1B2A", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / título en el sidebar
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 32))

        ctk.CTkLabel(
            logo_frame,
            text="⬡",
            font=ctk.CTkFont(size=28),
            text_color="#6366F1"
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            logo_frame,
            text="NE Launcher",
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            text_color="#E2E8F0"
        ).pack(side="left")

        # Separador
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#1E293B").pack(fill="x", padx=16, pady=(0, 20))

        # Botones de navegación
        self.btn_checker = self._nav_button("🔍  Entorno", self._show_checker)
        self.btn_creator = self._nav_button("⚡  Nuevo proyecto", self._show_creator)

        # Sección inferior del sidebar
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#334155"
        ).pack(pady=(0, 16))

        # ── Área de contenido ─────────────────────────────────────────────
        self.content_area = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=0)
        self.content_area.pack(side="left", fill="both", expand=True, padx=40, pady=36)

        # Guardar referencias a las vistas (se crean una sola vez)
        self._checker_view = None
        self._creator_view = None

    def _nav_button(self, text: str, command) -> ctk.CTkButton:
        """Crea un botón de navegación en el sidebar."""
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#94A3B8",
            anchor="w",
            corner_radius=8,
            height=40,
        )
        btn.pack(fill="x", padx=12, pady=2)
        return btn

    def _clear_content(self):
        """Limpia el área de contenido."""
        for widget in self.content_area.winfo_children():
            widget.pack_forget()

    def _set_active_button(self, active_btn: ctk.CTkButton):
        """Resalta el botón activo en el sidebar."""
        for btn in [self.btn_checker, self.btn_creator]:
            btn.configure(fg_color="transparent", text_color="#94A3B8")
        active_btn.configure(fg_color="#1E293B", text_color="#E2E8F0")

    # ── Navegación ────────────────────────────────────────────────────────

    def _show_checker(self):
        self._set_active_button(self.btn_checker)
        self._clear_content()

        if self._checker_view is None:
            self._checker_view = CheckerView(
                self.content_area,
                on_ready_callback=self._show_creator
            )
        self._checker_view.pack(fill="both", expand=True)

    def _show_creator(self):
        self._set_active_button(self.btn_creator)
        self._clear_content()

        if self._creator_view is None:
            self._creator_view = CreatorView(self.content_area)
        self._creator_view.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
