# Node Express Launcher

Herramienta gráfica para iniciar proyectos Node.js + Express de forma rápida.

## Requisitos previos

- Python 3.10 o superior
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
python main.py
```

---

## Estructura del proyecto

```
node-express-launcher/
├── main.py              # Ventana principal y navegación
├── checker.py           # Lógica: verificar Node.js y npm
├── project_gen.py       # Lógica: generar el proyecto base
├── ui/
│   ├── checker_view.py  # Vista de verificación de entorno
│   └── creator_view.py  # Vista de creación de proyecto
└── requirements.txt
```

## ¿Qué genera el launcher?

Al crear un proyecto obtienes:

```
mi-proyecto/
├── src/
│   ├── index.js         # Servidor Express configurado
│   └── routes/
│       └── api.js       # Router de ejemplo
├── package.json         # Scripts: dev (nodemon) y start
├── .gitignore
├── .env.example
└── README.md
```
Con las dependencias ya instaladas. Solo tienes que abrir la carpeta y ejecutar:
```bash
npm run dev
```

## Página básica generada al hacer `npm run dev`
<img width="1920" height="912" alt="image" src="https://github.com/user-attachments/assets/590112df-3b94-48a4-aefe-04bffcd011d3" />




