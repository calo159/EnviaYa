"""Arma el informe PDF a partir de docs/*.md.

Uso: python tools/informe.py
Requiere: markdown (pip) y Microsoft Edge. Los diagramas Mermaid se
renderizan en Edge cargando mermaid desde jsdelivr (necesita internet).
"""
import html
import pathlib
import re
import subprocess

import markdown

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

PORTADA = """
<div class="portada">
<p class="uni">UNIVERSIDAD DE LA GUAJIRA<br>Facultad de Ingenierías · Ingeniería de Sistemas</p>
<h1>Parcial 3 · Ingeniería de Software I</h1>
<p class="sub">Equipo de calidad y mantenimiento de EnvíaYa · Tercer corte · Unidades 6 y 7</p>
<table class="ident">
<tr><th>Estudiante</th><td>Carlos David Sierra</td><th>Código estudiantil</th><td>0182410125</td></tr>
<tr><th>Asignatura</th><td>Ingeniería de Software I (273365)</td><th>Grupo</th><td>B1 · VI semestre</td></tr>
<tr><th>Docente</th><td>Ing. Robert Damián Quintero Laverde</td><th>Fecha</th><td>11 de noviembre de 2026</td></tr>
<tr><th>Repositorio</th><td colspan="3">https://github.com/calo159/EnviaYa</td></tr>
</table>
<h3>Mis parámetros</h3>
<table class="params">
<tr><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th><th>PMAX</th><th>L1</th><th>L2</th><th>RR</th><th>RN</th><th>V</th><th>S</th><th>CAMBIO</th></tr>
<tr><td>4</td><td>1</td><td>0</td><td>1</td><td>2</td><td>5</td><td>50</td><td>3</td><td>10</td><td>20 %</td><td>50 %</td><td>15 %</td><td>$2.000</td><td>0</td></tr>
</table>
<p class="nota">Código 0182410125 → seis últimos dígitos 4 1 0 1 2 5. Detalle del cálculo en la Parte 1.</p>
</div>
"""

CSS = """
@page { size: Letter; margin: 18mm 15mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #222; }
h1 { color: #9b1c1c; font-size: 18pt; border-bottom: 3px solid #f0a800; padding-bottom: 4px; margin-top: 0; }
h2 { color: #7a1010; font-size: 13pt; margin-top: 18px; }
h3 { color: #7a1010; font-size: 11pt; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 8.8pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #9b1c1c; color: #fff; text-align: left; padding: 3px 6px; }
td { border: 1px solid #ddd; padding: 3px 6px; vertical-align: top; }
tr:nth-child(even) td { background: #f7f7f7; }
code { font-family: Consolas, monospace; font-size: 8.8pt; background: #f1f1f1; padding: 0 2px; }
pre { background: #f4f4f4; padding: 8px; font-size: 8pt; white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; }
img { max-width: 100%; }
.parte { page-break-before: always; }
.portada { text-align: center; padding-top: 30px; }
.portada .uni { font-weight: bold; color: #9b1c1c; }
.portada h1 { font-size: 24pt; border: none; }
.portada .sub { color: #7a5200; }
.portada table.ident th { width: 18%; }
.portada table.params td, .portada table.params th { text-align: center; }
.nota { font-size: 8.5pt; color: #555; }
pre.mermaid { background: #fff; text-align: center; white-space: pre; font-size: 11pt; }
pre.mermaid { page-break-inside: avoid; } pre.mermaid svg { max-width: 100%; max-height: 225mm; width: auto; height: auto; }
.captura img { border: 1px solid #ccc; }
"""


def md_a_html(texto):
    texto = texto.replace("](../evidencia/", "](" + (RAIZ / "evidencia").as_uri() + "/")
    bloques = []

    def guardar(m):
        bloques.append(m.group(1))
        return f"\n\n@@MERMAID{len(bloques) - 1}@@\n\n"

    texto = re.sub(r"```mermaid\n(.*?)```", guardar, texto, flags=re.S)
    cuerpo = markdown.markdown(texto, extensions=["tables", "fenced_code"])
    for i, b in enumerate(bloques):
        cuerpo = cuerpo.replace(f"<p>@@MERMAID{i}@@</p>", f'<pre class="mermaid">{html.escape(b)}</pre>')
    return cuerpo


def main():
    partes = sorted((RAIZ / "docs").glob("0*.md"))
    cuerpo = PORTADA
    for p in partes:
        cuerpo += '<div class="parte">' + md_a_html(p.read_text(encoding="utf-8")) + "</div>"
    log = (RAIZ / "evidencia" / "07-git-log.txt").read_text(encoding="utf-8")
    cuerpo += ('<div class="parte"><h1>Anexo · Salida de git log --oneline --graph --all</h1>'
               f"<pre>{html.escape(log)}</pre></div>")
    pagina = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Parcial 3 - Ingenieria de Software - Carlos David Sierra</title><style>{CSS}</style></head><body>{cuerpo}
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, theme:'neutral', flowchart:{{useMaxWidth:true}}}});</script>
</body></html>"""
    destino = RAIZ / "informe"
    destino.mkdir(exist_ok=True)
    fuente = destino / "informe.html"
    fuente.write_text(pagina, encoding="utf-8")
    pdf = destino / "Informe-Parcial3-Carlos-Sierra.pdf"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=30000",
                    f"--print-to-pdf={pdf}", fuente.as_uri()],
                   check=True, capture_output=True)
    import time
    for _ in range(40):  # Edge termina antes de que el PDF aparezca en disco
        if pdf.exists():
            break
        time.sleep(1)
    print("PDF:", pdf, pdf.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
