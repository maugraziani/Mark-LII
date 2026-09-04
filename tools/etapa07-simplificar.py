"""Etapa 07 — aplica a simplificação da superfície ativa do Jarvis v0.1.

Uso (na raiz do projeto):
    .\.venv\Scripts\python.exe tools\etapa07-simplificar.py

O script é deliberadamente conservador: só altera main.py quando encontra
exatamente os trechos esperados. dev_agent.py e game_updater.py NÃO são apagados.
"""
from __future__ import annotations

from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.py"
DESKTOP = ROOT / "actions" / "desktop.py"


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1 trecho; encontrado(s) {count}. Nada foi salvo.")
    return text.replace(old, new, 1)


def remove_tool_block(text: str, tool_name: str) -> str:
    marker = f'        "name": "{tool_name}",'
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError(f"tool {tool_name}: declaração não encontrada")

    start = text.rfind("    {", 0, pos)
    if start < 0:
        raise RuntimeError(f"tool {tool_name}: início do bloco não encontrado")

    # A declaração é um dict top-level dentro de TOOL_DECLARATIONS. Fazemos
    # contagem de chaves ignorando conteúdo entre strings para achar seu fim.
    depth = 0
    in_str = False
    quote = ""
    escaped = False
    end = None
    i = start
    while i < len(text):
        ch = text[i]
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                in_str = False
        else:
            if ch in ('"', "'"):
                in_str = True
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1

    if end is None:
        raise RuntimeError(f"tool {tool_name}: fim do bloco não encontrado")

    # Consumir vírgula e quebra de linha seguintes.
    if text[end:end + 1] == ",":
        end += 1
    if text[end:end + 2] == "\r\n":
        end += 2
    elif text[end:end + 1] == "\n":
        end += 1

    return text[:start] + text[end:]


def main() -> int:
    original = MAIN.read_text(encoding="utf-8")
    text = original

    text = replace_exact(
        text,
        "from actions.dev_agent         import dev_agent\n",
        "",
        "import dev_agent",
    )
    text = replace_exact(
        text,
        "from actions.game_updater      import game_updater\n",
        "",
        "import game_updater",
    )

    text = remove_tool_block(text, "dev_agent")
    text = remove_tool_block(text, "game_updater")

    text = replace_exact(
        text,
        '                "action": {"type": "STRING", "description": "wallpaper | wallpaper_url | organize | clean | list | stats | task"},\n',
        '                "action": {"type": "STRING", "description": "wallpaper | wallpaper_url | current_wallpaper | organize | clean | list | stats"},\n',
        "schema desktop action",
    )
    text = replace_exact(
        text,
        '                "task":   {"type": "STRING", "description": "Natural language desktop task"},\n',
        "",
        "schema desktop task",
    )

    text = replace_exact(
        text,
        '            elif name == "dev_agent":\n                r = await loop.run_in_executor(None, lambda: dev_agent(parameters=args, player=self.ui, speak=self.speak))\n                result = r or "Done."\n\n',
        "",
        "dispatch dev_agent",
    )
    text = replace_exact(
        text,
        '            elif name == "game_updater":\n                r = await loop.run_in_executor(None, lambda: game_updater(parameters=args, player=self.ui, speak=self.speak))\n                result = r or "Done."\n\n',
        "",
        "dispatch game_updater",
    )

    # Garantias antes de salvar.
    forbidden = (
        "from actions.dev_agent         import dev_agent",
        "from actions.game_updater      import game_updater",
        '"name": "dev_agent"',
        '"name": "game_updater"',
        'elif name == "dev_agent"',
        'elif name == "game_updater"',
        '"Natural language desktop task"',
    )
    remaining = [item for item in forbidden if item in text]
    if remaining:
        raise RuntimeError(f"referências ativas ainda presentes: {remaining}")

    if text == original:
        print("Nenhuma alteração necessária.")
        return 0

    # Backup local simples, fora do fluxo normal do app. Não sobrescreve um
    # backup anterior desta etapa.
    backup = MAIN.with_suffix(".py.etapa07.bak")
    if not backup.exists():
        backup.write_text(original, encoding="utf-8")

    MAIN.write_text(text, encoding="utf-8", newline="\n")

    try:
        py_compile.compile(str(MAIN), doraise=True)
        py_compile.compile(str(DESKTOP), doraise=True)
    except Exception:
        MAIN.write_text(original, encoding="utf-8", newline="\n")
        raise

    print("ETAPA07_PATCH_OK")
    print("- dev_agent: fora da superfície ativa; arquivo preservado")
    print("- game_updater: fora da superfície ativa; arquivo preservado")
    print("- desktop_control: schema sem task genérica")
    print("- main.py e actions/desktop.py: compilação OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ETAPA07_PATCH_ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
