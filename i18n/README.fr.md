<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-monitor/image?description=1&font=Source+Code+Pro&forks=1&issues=1&name=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto" alt="hath-monitor" width="640" />
</p>

<h1 align="center">Moniteur de Version et de Statut Hentai@Home</h1>

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
  <strong>Un outil Python léger et sans dépendances pour surveiller les mises à jour et le statut en temps réel du client H@H.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | Français | <a href="README.ru.md">Русский</a> | <a href="README.de.md">Deutsch</a> | <a href="README.ar.md">العربية</a> | <a href="README.he.md">עברית</a>
</p>

---

## 🚀 Fonctionnalités Clés

*   **🔍 Suivi de Version Multi-source** : Surveille le client Java officiel (`repo.e-hentai.org`), `hath-rust` (GitHub Releases) et la page de gestion H@H d'E-Hentai pour les changements de version.
*   **📡 Surveillance du Statut en Temps Réel** : Suit l'état en ligne/hors ligne, les changements d'IP, les niveaux de confiance, le taux de réussite (hitrate) et la qualité pour tous vos clients H@H.
*   **📅 Alertes de Quota Quotidien** : Notifications quotidiennes automatiques pour votre quota d'archives gratuit (Free Archive Quota).
*   **🔔 Notifications Riches** : Supporte plus de 10 canaux, dont Discord (Rich Embeds), Telegram, Slack, Bark, Gotify, Matrix, et plus encore.
*   **🌍 Support Multi-langue** : Notifications entièrement localisées en 11 langues.
*   **🛡️ Zéro Dépendance** : Construit strictement avec les bibliothèques standard de Python 3.11+. Aucun `pip install` requis.
*   **🐳 Prêt pour les Conteneurs** : Images Docker optimisées pour un déploiement facile.

---

## ⚙️ Démarrage Rapide

### 🐳 Utilisation de Docker (Recommandé)

Copiez et collez ces commandes pour commencer immédiatement :

```bash
# 1. Téléchargez le modèle de configuration
curl -L https://raw.githubusercontent.com/cololi/hath-monitor/main/.env.example -o .env

# 2. Modifiez le .env avec vos cookies EH et vos jetons de notification
# (Utilisez votre éditeur préféré : vi, nano ou bloc-notes)
vi .env 

# 3. Démarrez le conteneur du moniteur
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Installation Manuelle

Si vous préférez l'exécuter directement avec Python (3.11+) :

```bash
# 1. Clonez le dépôt et entrez dans le répertoire
git clone https://github.com/cololi/hath-monitor.git && cd hath-monitor

# 2. Copiez le modèle de variables d'environnement
cp .env.example .env

# 3. Modifiez le fichier de configuration .env
vi .env

# 4. Démarrez le moniteur en mode démon
python3 hath_monitor.py --daemon
```

---

## 🛠️ Configuration

Consultez [.env.example](../.env.example) pour obtenir la liste complète des variables d'environnement.

### Canaux de Notification

| Canal | Requis |
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

## ⌨️ Options CLI

| Drapeau | Description |
| :--- | :--- |
| `--daemon` | Exécute le script en arrière-plan en tant que démon. |
| `--verbose / -v` | Active la journalisation de débogage détaillée. |
| `--push-all` | Envoie immédiatement un rapport de statut complet à tous les canaux activés. |

---

## 📜 Licence & Remerciements

*   **Licence** : Ce projet est sous [Licence MIT](LICENSE).
*   **Crédits**: Remerciements spéciaux à la communauté Hentai@Home et aux développeurs des différents services de notification pris en charge.
