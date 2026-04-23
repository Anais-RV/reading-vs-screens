# Frontend App

Landing React/Vite orientada a conversión, simulación y generación de cards para bookstagram.

## Desarrollo

```bash
npm install
npm run dev
```

Servidor local por defecto:

- http://localhost:4173/

## Build

```bash
npm run build
```

## Configuración

Copia `.env.example` a `.env` si quieres definir la URL pública de esta app.

Variable disponible:

- `VITE_PUBLIC_APP_URL`: URL pública de esta landing para compartirla desde móvil.

## Deploy rápido

Opciones recomendadas:

- Vercel: detecta `vercel.json` y publica `dist`.
- Netlify: usa `netlify.toml` y publica `dist`.

En ambos casos:

1. Configura `VITE_PUBLIC_APP_URL` con la URL final de la landing.
2. Ejecuta el build en deploy con `npm run build`.

## Enfoque recomendado

- Esta landing se usa para captación, simulación y descarga de cards.
- El foco de producto está en una experiencia única y rápida en React.

## Limpieza del repo

No subas carpetas generadas localmente como:

- `node_modules/`
- `dist/`

El deploy debe reconstruir todo desde `package.json`.