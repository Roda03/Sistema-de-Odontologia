import sys
import platform
import ctypes

from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QDesktopWidget, QMessageBox,
    QGraphicsDropShadowEffect, QAction, QScrollArea, QFrame
)

from views.base_window import BaseWindow  # tu clase base

class VentanaLogin(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setObjectName("VentanaLogin")
        self.setWindowTitle("Login de Odontología")
        self.resize(480, 520)

        self._apply_global_style()
        self._build_ui()
        self._center()
        self.input_usuario.setFocus()

    # ---------- Estilo ----------
    def _apply_global_style(self):
        f = QFont("Segoe UI", 10)
        self.setFont(f)
        self.setStyleSheet("""
            QWidget#VentanaLogin {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #eef5ff, stop:1 #f9fbff);
            }

            QFrame#Card {
                background: #ffffff;
                border: 1px solid #dbe3f0;
                border-radius: 14px;
            }

            QLabel.Title {
                font-size: 22px;
                font-weight: 800;
                color: #1f2d3d;
            }
            QLabel.Subtitle {
                color: #5f6b7a;
            }

            QLineEdit {
                border: 1.5px solid #cfd8e3;
                border-radius: 8px;
                padding: 8px 10px;
                background: #fff;
            }
            QLineEdit:focus {
                border: 1.5px solid #3b82f6;
            }

            QPushButton {
                border-radius: 8px;
                padding: 10px 14px;
                font-weight: 600;
            }
            QPushButton#btnLogin {
                background: #3b82f6;
                color: white;
                border: none;
            }
            QPushButton#btnLogin:hover { background: #2563eb; }
            QPushButton#btnLogin:pressed { background: #1d4ed8; }

            /* Feedback de error */
            QLineEdit[error="true"] {
                border: 2px solid #ef4444;
                background: #fff8f8;
            }
        """)

    # ---------- UI ----------
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        root.addWidget(scroll)

        wrapper = QWidget()
        scroll.setWidget(wrapper)

        v = QVBoxLayout(wrapper)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(12)

        v.addStretch(2)

        title = QLabel("🔐 Sistema Odontológico")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("class", "Title")
        v.addWidget(title)

        subtitle = QLabel("Ingresá tus credenciales para continuar")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setProperty("class", "Subtitle")
        v.addWidget(subtitle)

        v.addSpacing(6)

        # Card contenedor con tamaño fijo
        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card.setFixedSize(380, 300)  # <-- tamaño fijo aquí
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 12)
        shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(shadow)

        # Usuario
        lbl_usuario = QLabel("Usuario")
        lbl_usuario.setStyleSheet("font-weight:600; color:#2c3e50;")
        card_layout.addWidget(lbl_usuario)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("usuario")
        self.input_usuario.setClearButtonEnabled(True)
        self.input_usuario.setMinimumHeight(38)
        card_layout.addWidget(self.input_usuario)

        # Contraseña
        lbl_clave = QLabel("Contraseña")
        lbl_clave.setStyleSheet("font-weight:600; color:#2c3e50;")
        card_layout.addWidget(lbl_clave)

        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("contraseña")
        self.input_clave.setEchoMode(QLineEdit.Password)
        self.input_clave.setClearButtonEnabled(True)
        self.input_clave.setMinimumHeight(38)
        card_layout.addWidget(self.input_clave)

        # Toggle mostrar/ocultar
        self._add_password_toggle()

        # Hint Caps Lock
        self._caps_tip = QLabel("")
        self._caps_tip.setStyleSheet("color:#e67e22; font-size:12px; padding-top:4px;")
        card_layout.addWidget(self._caps_tip)
        self._inject_caps_handler()

        # Botón login
        self.btn_login = QPushButton("Ingresar")
        self.btn_login.setObjectName("btnLogin")
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setDefault(True)
        card_layout.addWidget(self.btn_login)

        v.addWidget(self.card, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        v.addStretch(3)

        # Tab order
        self.setTabOrder(self.input_usuario, self.input_clave)
        self.setTabOrder(self.input_clave, self.btn_login)

    def _center(self):
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    # ---------- Helpers ----------
    def _add_password_toggle(self):
        self.toggle_pwd_action = QAction(QIcon.fromTheme("view-hidden"), "Mostrar/ocultar", self)
        self.toggle_pwd_action.setCheckable(True)
        self.toggle_pwd_action.toggled.connect(self._toggle_pwd)
        self.input_clave.addAction(self.toggle_pwd_action, QLineEdit.TrailingPosition)

    def _toggle_pwd(self, checked):
        if checked:
            self.input_clave.setEchoMode(QLineEdit.Normal)
            self.toggle_pwd_action.setIcon(QIcon.fromTheme("view-visible"))
        else:
            self.input_clave.setEchoMode(QLineEdit.Password)
            self.toggle_pwd_action.setIcon(QIcon.fromTheme("view-hidden"))

    def _mark_error(self, widget, msg):
        widget.setProperty("error", True)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.setToolTip(msg)

    def _clear_error(self, widget):
        widget.setProperty("error", False)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.setToolTip("")

    def _shake(self, widget):
        anim = QPropertyAnimation(widget, b"pos", self)
        start = widget.pos()
        seq = [QPoint(start.x() + dx, start.y()) for dx in (0, 14, -14, 10, -10, 6, -6, 3, -3, 0)]
        anim.setDuration(220)
        anim.setKeyValueAt(0.0, seq[0])
        for i, p in enumerate(seq[1:], start=1):
            anim.setKeyValueAt(i / (len(seq) - 1), p)
        anim.start(QPropertyAnimation.DeleteWhenStopped)

    # Caps Lock (Windows)
    def _inject_caps_handler(self):
        orig_keypress = self.input_clave.keyPressEvent

        def handler(e):
            self._update_caps_tip()
            return orig_keypress(e)

        self.input_clave.keyPressEvent = handler

        orig_focus = self.input_clave.focusInEvent
        def focus_handler(e):
            self._update_caps_tip()
            return orig_focus(e)
        self.input_clave.focusInEvent = focus_handler

    def _capslock_on_windows(self):
        try:
            return bool(ctypes.windll.user32.GetKeyState(0x14) & 1)
        except Exception:
            return False

    def _update_caps_tip(self):
        caps_on = platform.system() == "Windows" and self._capslock_on_windows()
        self._caps_tip.setText("Bloq Mayús activado" if caps_on else "")

    # ---------- Lógica ----------
    def login(self):
        usuario = self.input_usuario.text().strip()
        clave = self.input_clave.text().strip()

        self._clear_error(self.input_usuario)
        self._clear_error(self.input_clave)

        if not usuario:
            self._mark_error(self.input_usuario, "Ingrese su usuario")
        if not clave:
            self._mark_error(self.input_clave, "Ingrese su contraseña")
        if not usuario or not clave:
            self._shake(self.card)
            return

        QApplication.setOverrideCursor(Qt.BusyCursor)
        try:
            ok = self.db.validar_usuario(usuario, clave)
        finally:
            QApplication.restoreOverrideCursor()

        if ok:
            if hasattr(self.parent, "mostrar_inicio"):
                self.parent.mostrar_inicio()
            self.close()
        else:
            self._mark_error(self.input_clave, "Credenciales inválidas")
            self.input_clave.clear()
            self.input_clave.setFocus()
            self._shake(self.card)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.login()
        else:
            super().keyPressEvent(event)