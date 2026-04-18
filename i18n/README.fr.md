<p align="center">
  <img src="https://socialify.git.ci/cololi/hath-version-monitor/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="hath-version-monitor" width="640" />
</p>

<h1 align="center">Moniteur de Version et de Statut Hentai@Home</h1>

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
  <strong>Un outil Python léger et sans dépendances pour surveiller les mises à jour et le statut en temps réel du client H@H.</strong>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
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
curl -L https://raw.githubusercontent.com/cololi/hath-version-monitor/main/config.toml.example -o config.toml

# 2. Modifiez le config.toml avec vos cookies EH et vos jetons de notification
# (Utilisez votre éditeur préféré : vi, nano ou bloc-notes)
vi config.toml 

# 3. Démarrez le conteneur du moniteur
docker run -d \
  --name hath-monitor \
  --restart unless-stopped \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/hath_monitor.db:/app/hath_monitor.db \
  ghcr.io/cololi/hath-monitor:latest
```

### 🐍 Installation Manuelle

Si vous préférez l'exécuter directement avec Python (3.11+) :

```bash
# 1. Clonez le dépôt et entrez dans le répertoire
git clone https://github.com/cololi/hath-version-monitor.git && cd hath-version-monitor

# 2. Générez le fichier de configuration par défaut
python3 hath_monitor.py

# 3. Modifiez le config.toml généré
vi config.toml

# 4. Démarrez le moniteur en mode démon
python3 hath_monitor.py --daemon
```

---

## 🛠️ Configuration

Le fichier `config.toml` est divisé en trois sections principales : `[monitor]`, `[notify]`, et `[system]`.

### Canaux de Notification

| Canal | Requis |
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

## ⌨️ Options CLI

| Drapeau | Description |
| :--- | :--- |
| `--daemon` | Exécute le script en arrière-plan en tant que démon. |
| `--verbose` | Active la journalisation de débogage détaillée. |
| `--history` | Affiche les 20 dernières entrées de l'historique de statut. |
| `--push-all` | Envoie immédiatement un rapport de statut complet à tous les canaux activés. |
| `--config PATH` | Spécifie un chemin personnalisé pour le fichier de configuration. |

---

## 📜 Licence & Remerciements

*   **Licence** : Ce projet est sous [Licence MIT](LICENSE).
*   **Crédits** : Remerciements particuliers à la communauté Hentai@Home et aux développeurs des différents services de notification supportés.

---

## 👥 Contributeurs

<p align="center">
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/cololi">
          <img src="https://github.com/cololi.png" width="100px;" alt="Cololi"/><br />
          <sub><b>Cololi</b></sub>
        </a><br />
        🚀 <b>Développeur Principal</b>
      </td>
      <td align="center">
        <a href="https://gemini.google.com/">
          <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png" width="100px;" alt="Gemini AI"/><br />
          <sub><b>Gemini AI</b></sub>
        </a><br />
        🤖 <b>Assistant IA</b>
      </td>
    </tr>
  </table>
</p>

<p align="center">Fait avec ❤️ pour la communauté H@H</p>
