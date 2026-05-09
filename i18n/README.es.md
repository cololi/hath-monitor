<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">Monitor de Versión y Estado de Hentai@Home</h1>

<p align="center">
  <a href="https://github.com/cololi/hath-monitor/releases">
    <img src="https://img.shields.io/github/v/release/cololi/hath-monitor?style=flat-square&color=blue" alt="release">
  </a>
  <a href="https://github.com/cololi/hath-monitor/pkgs/container/hath-monitor">
    <img src="https://img.shields.io/badge/docker-ghcr.io-blue?style=flat-square&logo=docker" alt="docker">
  </a>
  <a href="https://github.com/cololi/hath-monitor/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/cololi/hath-monitor?style=flat-square&color=green" alt="license">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python" alt="python">
  </a>
</p>

<p align="center">
  <strong>Una herramienta de Python ligera y sin dependencias para monitorear las actualizaciones y el estado en tiempo real del cliente H@H.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | Español | <a href="README.fr.md">Français</a> | <a href="README.ru.md">Русский</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ar.md">العربية</a> | <a href="README.he.md">עברית</a>
</p>

---

## 🚀 Características Principales

*   **🔍 Seguimiento de Versiones Multi-fuente**: Monitorea el cliente oficial de Java (`repo.e-hentai.org`), `hath-rust` (GitHub Releases) y la página de gestión H@H de E-Hentai para cambios de versión.
*   **📡 Monitoreo de Estado en Tiempo Real**: Rastrea el estado en línea/fuera de línea, cambios de IP, niveles de confianza, hitrate y calidad para todos sus clientes H@H.
*   **📅 Alertas de Cuota Diaria**: Notificaciones diarias automáticas para su Cuota de Archivo Gratuita (Free Archive Quota).
*   **🔔 Notificaciones Enriquecidas**: Soporta más de 10 canales, incluyendo Discord (Rich Embeds), Telegram, Slack, Bark, Gotify, Matrix y más.
*   **🌍 Soporte Multi-idioma**: Notificaciones totalmente localizadas en 11 idiomas.
*   **🛡️ Cero Dependencias**: Construido estrictamente con las bibliotecas estándar de Python 3.11+. No requiere `pip install`.
*   **🐳 Listo para Contenedores**: Imágenes de Docker optimizadas para un despliegue sencillo.

---

## ⚙️ Inicio Rápido

### 🐳 Usando Docker (Recomendado)

Copie y pegue estos comandos para comenzar de inmediato:

```bash
# 1. Descargue la plantilla de configuración
curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/.env.example -o .env

# 2. Edite el .env con sus cookies de EH y tokens de notificación
# (Use su editor favorito: vi, nano o bloc de notas)
vi .env 

# 3. Inicie el contenedor del monitor
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Instalación Manual

Si prefiere ejecutarlo directamente con Python (3.11+):

```bash
# 1. Clone el repositorio y entre en el directorio
git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor

# 2. Copie la plantilla de variables de entorno
cp .env.example .env

# 3. Edite el archivo de configuración .env
vi .env

# 4. Inicie el monitor en modo demonio
python3 hath_monitor.py --daemon
```

---

## 🛠️ Configuración

Consulte [.env.example](../.env.example) para obtener la lista completa de variables de entorno.

### Canales de Notificación

| Canal | Requisito Clave |
| :--- | :--- |
| **Bark** | `BARK_URL` |
| **Telegram** | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| **Discord** | `DISCORD_WEBHOOK` |
| **Slack** | `SLACK_WEBHOOK` |
| **Pushover** | `PUSHOVER_USER_KEY`, `PUSHOVER_API_TOKEN` |
| **Gotify** | `GOTIFY_URL`, `GOTIFY_TOKEN` |
| **Matrix** | `MATRIX_URL`, `MATRIX_TOKEN`, `MATRIX_ROOM_ID` |
| **PushPlus** | `PUSHPLUS_TOKEN` |
| **PushDeer** | `PUSHDEER_KEY` |
| **DingTalk** | `DINGTALK_ACCESS_TOKEN` |
| **Webhooks** | `WEBHOOKS` |

---

## ⌨️ Opciones de CLI

| Bandera | Descripción |
| :--- | :--- |
| `--daemon` | Ejecuta el script en segundo plano como un demonio. |
| `--verbose / -v` | Habilita el registro de depuración detallado. |
| `--push-all` | Envía inmediatamente un informe de estado completo a todos los canales habilitados. |

---

## 📜 Licencia y Agradecimientos

*   **Licencia**: Este proyecto está bajo la [Licencia MIT](LICENSE).
*   **Créditos**: Agradecimientos especiales a la comunidad Hentai@Home y a los desarrolladores de los diversos servicios de notificación soportados.
