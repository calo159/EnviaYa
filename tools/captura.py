"""Convierte la salida de un comando en una captura PNG estilo terminal.

Uso: python tools/captura.py salida.txt captura.png "titulo de la ventana"
Renderiza con Microsoft Edge en modo headless.
"""
import html
import pathlib
import subprocess
import sys

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def colorear(linea):
    esc = html.escape(linea)
    if "FAILED" in linea or " failed" in linea or "Error" in linea or linea.startswith("E "):
        return f'<span style="color:#ff6b6b">{esc}</span>'
    if "PASSED" in linea or " passed" in linea and "failed" not in linea:
        return f'<span style="color:#7ee787">{esc}</span>'
    if linea.startswith("PS ") or linea.startswith("$ "):
        return f'<span style="color:#79c0ff">{esc}</span>'
    return esc


def main():
    entrada, salida, titulo = sys.argv[1], sys.argv[2], sys.argv[3]
    texto = pathlib.Path(entrada).read_text(encoding="utf-8", errors="replace")
    lineas = texto.rstrip().splitlines()
    cuerpo = "\n".join(colorear(l) for l in lineas)
    alto = 70 + 17 * len(lineas)
    pagina = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#1e1e1e;font-family:Consolas,monospace;font-size:13px}}
.bar{{background:#323233;color:#ccc;padding:6px 12px;font-family:Segoe UI,sans-serif;font-size:12px}}
pre{{margin:0;padding:10px 12px;color:#d4d4d4;white-space:pre;line-height:17px}}
</style></head><body><div class="bar">{html.escape(titulo)}</div><pre>{cuerpo}</pre></body></html>"""
    tmp = pathlib.Path(salida).with_suffix(".html")
    tmp.write_text(pagina, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={pathlib.Path(salida).resolve()}",
                    f"--window-size=1100,{alto}", tmp.resolve().as_uri()],
                   check=True, capture_output=True)
    tmp.unlink()


if __name__ == "__main__":
    main()
