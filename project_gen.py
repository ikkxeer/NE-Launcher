"""
project_gen.py
Genera un proyecto base de Node.js + Express listo para usar.
Crea la estructura de carpetas, instala dependencias y configura scripts.
"""

import os
import json
import subprocess
from pathlib import Path


# Contenido de cada archivo del proyecto base
PACKAGE_JSON = {
    "name": "",           # Se rellena con el nombre del proyecto
    "version": "1.0.0",
    "description": "Proyecto base Node.js + Express",
    "main": "src/index.js",
    "scripts": {
        "dev": "nodemon src/index.js",
        "start": "node src/index.js"
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "dependencies": {
        "express": "^4.18.2"
    },
    "devDependencies": {
        "nodemon": "^3.0.1"
    }
}

INDEX_JS = """\
const express = require('express');
const path    = require('path');

const app  = express();
const PORT = process.env.PORT || 3000;

// Middlewares básicos
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Archivos estáticos (página de bienvenida y assets futuros)
app.use(express.static(path.join(__dirname, '..', 'public')));

// Rutas de la API
app.use('/api', require('./routes/api'));

app.listen(PORT, () => {
    console.log(`Servidor iniciado en http://localhost:${PORT}`);
});
"""

API_ROUTER = """\
const { Router } = require('express');

const router = Router();

// Ejemplo de endpoint GET
router.get('/hello', (req, res) => {
    res.json({ message: 'Hola desde la API!' });
});

module.exports = router;
"""

GITIGNORE = """\
node_modules/
.env
*.log
dist/
.DS_Store
"""

ENV_EXAMPLE = """\
PORT=3000
# Añade aquí tus variables de entorno
"""

WELCOME_HTML = """\
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{project_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:        #060910;
      --surface:   #0d1117;
      --border:    #1c2333;
      --accent:    #6366f1;
      --accent2:   #22d3ee;
      --green:     #22c55e;
      --text:      #e2e8f0;
      --muted:     #64748b;
      --card-bg:   #0d1420;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      overflow-x: hidden;
    }}

    /* Fondo con grid sutil */
    body::before {{
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
      background-size: 40px 40px;
      opacity: 0.35;
      pointer-events: none;
      z-index: 0;
    }}

    /* Glow central */
    body::after {{
      content: '';
      position: fixed;
      top: -200px;
      left: 50%;
      transform: translateX(-50%);
      width: 700px;
      height: 500px;
      background: radial-gradient(ellipse, rgba(99,102,241,0.12) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    .wrapper {{
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 780px;
      display: flex;
      flex-direction: column;
      gap: 28px;
      animation: fadeUp 0.6s ease both;
    }}

    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(24px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ── Header ── */
    .header {{
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 14px;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 5px 14px;
      border: 1px solid var(--border);
      border-radius: 999px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: var(--green);
      background: rgba(34,197,94,0.06);
    }}

    .badge-dot {{
      width: 7px; height: 7px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 8px var(--green);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50%       {{ opacity: 0.4; }}
    }}

    h1 {{
      font-family: 'JetBrains Mono', monospace;
      font-size: clamp(2rem, 5vw, 3rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #fff 30%, var(--accent) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}

    .subtitle {{
      color: var(--muted);
      font-size: 15px;
      max-width: 460px;
      line-height: 1.6;
    }}

    /* ── Comando principal ── */
    .run-command {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .run-command .label {{
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
      font-family: 'JetBrains Mono', monospace;
    }}

    .run-command .cmd {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      font-weight: 700;
      color: var(--accent2);
    }}

    .copy-btn {{
      flex-shrink: 0;
      background: var(--border);
      border: none;
      color: var(--muted);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }}
    .copy-btn:hover {{ background: var(--accent); color: #fff; }}

    /* ── Grid de cards ── */
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }}

    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      transition: border-color 0.2s, transform 0.2s;
    }}
    .card:hover {{
      border-color: var(--accent);
      transform: translateY(-2px);
    }}

    .card-icon {{
      font-size: 22px;
      margin-bottom: 12px;
    }}

    .card h3 {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 6px;
    }}

    .card p {{
      font-size: 12px;
      color: var(--muted);
      line-height: 1.6;
    }}

    .card code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      background: rgba(99,102,241,0.12);
      color: var(--accent);
      padding: 1px 5px;
      border-radius: 4px;
    }}

    /* ── Estructura del proyecto ── */
    .tree {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 24px;
    }}

    .tree h2 {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .tree pre {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--text);
      line-height: 1.9;
    }}

    .tree .dim  {{ color: var(--muted); }}
    .tree .hi   {{ color: var(--accent2); }}
    .tree .good {{ color: var(--green); }}

    /* ── Footer ── */
    .footer {{
      text-align: center;
      font-size: 12px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="wrapper">

    <div class="header">
      <div class="badge">
        <span class="badge-dot"></span>
        servidor corriendo
      </div>
      <h1>{project_name}</h1>
      <p class="subtitle">
        Tu proyecto Node.js + Express está listo.<br/>
        Abre tu editor, empieza a editar y guarda — nodemon recargará solo.
      </p>
    </div>

    <div class="run-command">
      <div>
        <div class="label">// ejecuta esto en tu terminal</div>
        <div class="cmd">npm run dev</div>
      </div>
      <button class="copy-btn" onclick="copyCmd()">Copiar</button>
    </div>

    <div class="cards">
      <div class="card">
        <div class="card-icon">⚡</div>
        <h3>Punto de entrada</h3>
        <p>El servidor vive en <code>src/index.js</code>. Aquí configuras middlewares, puertos y montas las rutas.</p>
      </div>
      <div class="card">
        <div class="card-icon">🔀</div>
        <h3>Rutas de la API</h3>
        <p>Añade tus endpoints en <code>src/routes/api.js</code>. Ya tienes un ejemplo en <code>GET /api/hello</code>.</p>
      </div>
      <div class="card">
        <div class="card-icon">🌍</div>
        <h3>Variables de entorno</h3>
        <p>Copia <code>.env.example</code> a <code>.env</code> y pon ahí tus claves. Nunca subas el <code>.env</code> a git.</p>
      </div>
      <div class="card">
        <div class="card-icon">🎨</div>
        <h3>Frontend estático</h3>
        <p>Esta misma página está en <code>public/index.html</code>. Edítala o reemplázala con tu propia UI.</p>
      </div>
    </div>

    <div class="tree">
      <h2>Estructura del proyecto</h2>
      <pre>
<span class="good">{project_name}/</span>
<span class="dim">├──</span> <span class="hi">src/</span>
<span class="dim">│   ├──</span> index.js          <span class="dim">← servidor Express</span>
<span class="dim">│   └──</span> routes/
<span class="dim">│       └──</span> api.js        <span class="dim">← tus endpoints</span>
<span class="dim">├──</span> <span class="hi">public/</span>
<span class="dim">│   └──</span> index.html        <span class="dim">← esta página</span>
<span class="dim">├──</span> .env.example
<span class="dim">├──</span> .gitignore
<span class="dim">└──</span> package.json
      </pre>
    </div>

    <div class="footer">
      Creado con Node Express Launcher &nbsp;·&nbsp; <span id="url">http://localhost:3000</span>
    </div>

  </div>

  <script>
    function copyCmd() {{
      navigator.clipboard.writeText('npm run dev').then(() => {{
        const btn = document.querySelector('.copy-btn');
        btn.textContent = '✓ Copiado';
        setTimeout(() => btn.textContent = 'Copiar', 2000);
      }});
    }}
  </script>
</body>
</html>
"""

README = """\
# {project_name}

Proyecto base creado con Node Express Launcher.

## Instalación

```bash
npm install
```

## Desarrollo

```bash
npm run dev
```

## Producción

```bash
npm start
```

## Estructura

```
src/
├── index.js        # Punto de entrada
└── routes/
    └── api.js      # Rutas de la API
```
"""


def create_project(project_name: str, destination_path: str, on_log=None) -> tuple[bool, str]:
    """
    Crea el proyecto base en destination_path/project_name.
    on_log: función opcional para enviar mensajes de progreso a la UI.
    Devuelve (éxito, mensaje_final).
    """

    def log(msg: str):
        if on_log:
            on_log(msg)

    try:
        project_path = Path(destination_path) / project_name

        # 1. Crear carpetas
        log("📁 Creando estructura de carpetas...")
        dirs = [
            project_path / "src" / "routes",
            project_path / "public",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

        # 2. Crear package.json
        log("📦 Generando package.json...")
        pkg = PACKAGE_JSON.copy()
        pkg["name"] = project_name.lower().replace(" ", "-")
        package_json_path = project_path / "package.json"
        package_json_path.write_text(json.dumps(pkg, indent=2), encoding="utf-8")

        # 3. Crear archivos fuente
        log("📝 Creando archivos del proyecto...")
        (project_path / "src" / "index.js").write_text(INDEX_JS, encoding="utf-8")
        (project_path / "src" / "routes" / "api.js").write_text(API_ROUTER, encoding="utf-8")
        (project_path / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
        (project_path / ".env.example").write_text(ENV_EXAMPLE, encoding="utf-8")
        (project_path / "README.md").write_text(
            README.format(project_name=project_name), encoding="utf-8"
        )

        # 4. Generar página de bienvenida
        log("🎨 Generando página de bienvenida...")
        (project_path / "public" / "index.html").write_text(
            WELCOME_HTML.format(project_name=project_name), encoding="utf-8"
        )

        # 5. Instalar dependencias con npm install
        log("⬇️  Instalando dependencias (npm install)...")
        result = subprocess.run(
            "npm install",
            shell=True,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            return False, f"Error en npm install:\n{result.stderr}"

        log("✅ Dependencias instaladas correctamente.")
        log(f"🎉 Proyecto '{project_name}' listo en:\n   {project_path}")

        return True, str(project_path)

    except Exception as e:
        return False, f"Error inesperado: {str(e)}"
