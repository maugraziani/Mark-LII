from __future__ import annotations

from pathlib import Path
import py_compile
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "ui.py"
BACKUP = ROOT / "ui.py.pre-mark52-ui.bak"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1 trecho, encontrado {count}. Nenhuma alteração salva.")
    return text.replace(old, new, 1)


def main() -> int:
    original = UI.read_text(encoding="utf-8")
    text = original

    # 1) Remove a moldura/título nativo do Windows.
    text = replace_once(
        text,
        '        self.setWindowTitle(f"{_display} — MARK LII")\n        self.setMinimumSize(_MIN_W, _MIN_H)\n',
        '        self.setWindowTitle("JARVIS MARK 52")\n'
        '        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)\n'
        '        self.setMinimumSize(_MIN_W, _MIN_H)\n',
        "frameless window",
    )

    # 2) O nome visual passa a ser JARVIS MARK 52 sem alterar a identidade
    # falada/configurada do assistente (self._assistant_name continua intacto).
    text = replace_once(
        text,
        '        _display = self._assistant_name.upper()\n',
        '        _display = ("JARVIS MARK 52"\n'
        '                    if self._assistant_name.upper() in ("JARVIS", "J.A.R.V.I.S")\n'
        '                    else self._assistant_name.upper())\n',
        "display name",
    )

    # 3) O subtítulo tradicional continua válido para a apresentação Mark 52.
    text = replace_once(
        text,
        '                     if _disp in ("JARVIS", "J.A.R.V.I.S")\n',
        '                     if _disp in ("JARVIS", "J.A.R.V.I.S", "JARVIS MARK 52")\n',
        "header subtitle",
    )

    # 4) Cabeçalho interno recebe minimizar/fechar; sem isso uma janela sem
    # moldura ficaria dependente de Alt+F4/voz para ser controlada.
    old_right = '''        right_col = QVBoxLayout(); right_col.setSpacing(2)\n        self._clock_lbl = QLabel("00:00:00")\n'''
    new_right = '''        window_btns = QHBoxLayout(); window_btns.setSpacing(3)\n        for txt, tip, callback in (("—", "Minimize", self.showMinimized),\n                                   ("✕", "Close", self.close)):\n            b = QPushButton(txt)\n            b.setFixedSize(24, 22)\n            b.setFont(QFont("Courier New", 9, QFont.Weight.Bold))\n            b.setCursor(Qt.CursorShape.PointingHandCursor)\n            b.setToolTip(tip)\n            b.setStyleSheet(f"""\n                QPushButton {{ background: transparent; color: {C.TEXT_DIM};\n                    border: 1px solid {C.BORDER}; border-radius: 3px; }}\n                QPushButton:hover {{ color: {C.PRI}; border-color: {C.PRI_DIM}; }}\n            """)\n            b.clicked.connect(callback)\n            window_btns.addWidget(b)\n        lay.addLayout(window_btns)\n\n        right_col = QVBoxLayout(); right_col.setSpacing(2)\n        self._clock_lbl = QLabel("00:00:00")\n'''
    text = replace_once(text, old_right, new_right, "window controls")

    # 5) Arrastar a faixa superior move a janela como uma title bar normal.
    marker = '''    def _show_camera_frame(self, img_bytes: bytes):\n'''
    drag_methods = '''    def mousePressEvent(self, event):\n        if (event.button() == Qt.MouseButton.LeftButton\n                and event.position().y() <= 54\n                and not self.isFullScreen()):\n            self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()\n            event.accept()\n            return\n        super().mousePressEvent(event)\n\n    def mouseMoveEvent(self, event):\n        if (event.buttons() & Qt.MouseButton.LeftButton\n                and hasattr(self, "_drag_offset")\n                and not self.isFullScreen()):\n            self.move(event.globalPosition().toPoint() - self._drag_offset)\n            event.accept()\n            return\n        super().mouseMoveEvent(event)\n\n    def mouseReleaseEvent(self, event):\n        if hasattr(self, "_drag_offset"):\n            del self._drag_offset\n        super().mouseReleaseEvent(event)\n\n'''
    text = replace_once(text, marker, drag_methods + marker, "window dragging")

    # Valida antes de gravar.
    tmp = UI.with_suffix(".py.mark52.tmp")
    tmp.write_text(text, encoding="utf-8")
    try:
        py_compile.compile(str(tmp), doraise=True)
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass

    if not BACKUP.exists():
        shutil.copy2(UI, BACKUP)
    UI.write_text(text, encoding="utf-8")
    py_compile.compile(str(UI), doraise=True)

    print("UI_MARK52_OK")
    print("- janela: sem moldura superior nativa")
    print("- título visual: JARVIS MARK 52")
    print("- identidade falada/configurada: preservada")
    print("- cabeçalho: minimizar e fechar adicionados")
    print("- cabeçalho: arrastar para mover a janela")
    print("- ui.py: compilação OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"UI_MARK52_FALHOU: {exc}", file=sys.stderr)
        raise SystemExit(1)
