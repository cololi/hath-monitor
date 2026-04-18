<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Monitor de Versión y Estado de Hentai@Home</h1>

<p align="center">
  <a href="https://github.com/cololi/hath-version-monitor/releases">
    <img src="https://img.shields.io/github/v/release/cololi/hath-version-monitor?style=flat-square&color=blue" alt="release">
  </a>
  <a href="https://github.com/cololi/hath-version-monitor/pkgs/container/hath-monitor">
    <img src="https://img.shields.io/badge/docker-ghcr.io-blue?style=flat-square&logo=docker" alt="docker">
  </a>
  <a href="https://github.com/cololi/hath-version-monitor/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/cololi/hath-version-monitor?style=flat-square&color=green" alt="license">
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
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. Edite el config.toml con sus cookies de EH y tokens de notificación
# (Use su editor favorito: vi, nano o bloc de notas)
vi config.toml 

# 3. Inicie el contenedor del monitor
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Instalación Manual

Si prefiere ejecutarlo directamente con Python (3.11+):

```bash
# 1. Clone el repositorio y entre en el directorio
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. Genere el archivo de configuración por defecto
python3 hath_monitor.py

# 3. Edite el config.toml generado
vi config.toml

# 4. Inicie el monitor en modo demonio
python3 hath_monitor.py --daemon
```

---

## 🛠️ Configuración

El archivo `config.toml` se divide en tres secciones principales: `[monitor]`, `[notify]` y `[system]`.

### Canales de Notificación

| Canal | Requisito Clave |
| :--- | :--- |
| **Bark** | `bark_url` |
| **Telegram** | `telegram_bot_token`, `telegram_chat_id` |
| **Discord** | `discord_webhook` |
| **Slack** | `slack_webhook` |
| **Pushover** | `pushover_user_key`, `pushover_api_token` |
| **Gotify** | `gotify_url`, `gotify_token` |
| **Matrix** | `matrix_url`, `matrix_token`, `matrix_room_id` |
| **PushPlus** | `pushplus_token` |
| **PushDeer** | `pushdeer_key` |
| **DingTalk** | `dingtalk_access_token` |
| **Webhooks** | `webhooks = ["url1", "url2"]` |

---

## ⌨️ Opciones de CLI

| Bandera | Descripción |
| :--- | :--- |
| `--daemon` | Ejecuta el script en segundo plano como un demonio. |
| `--verbose / -v` | Habilita el registro de depuración detallado. |
| `--history` | Muestra las últimas 20 entradas del historial de estado. |
| `--push-all` | Envía inmediatamente un informe de estado completo a todos los canales habilitados. |
| `--config PATH` | Especifica una ruta personalizada para el archivo de configuración. |

---

## 📜 Licencia y Agradecimientos

*   **Licencia**: Este proyecto está bajo la [Licencia MIT](LICENSE).
*   **Créditos**: Agradecimientos especiales a la comunidad Hentai@Home y a los desarrolladores de los diversos servicios de notificación soportados.
