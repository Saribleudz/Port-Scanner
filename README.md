# Port Scanner

Outil de scan de ports réseau avec interface web, développé en Python avec Flask.

## Aperçu

Tu entres une IP ou un nom de domaine, une plage de ports, et l'outil te liste en quelques secondes tous les ports ouverts avec le service associé. Les résultats sont exportables en CSV.

## Fonctionnalités

- Scan TCP multi-threadé (100 threads simultanés) — rapide sur de larges plages
- Détection automatique du service associé à chaque port (SSH, HTTP, HTTPS, MySQL, RDP...)
- Plage de ports configurable de 1 à 65535
- Export des résultats en CSV
- Interface web sobre et responsive
- Résolution DNS automatique (accepte IP et noms de domaine)

## Stack technique

- **Python** — socket, concurrent.futures, csv
- **Flask** — serveur web et API REST
- **HTML / CSS / JavaScript** — interface web sans dépendance externe

## Installation

```bash
git clone https://github.com/Saribleudz/Port-Scanner.git
cd Port-Scanner
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Ouvrir `http://127.0.0.1:5000` dans le navigateur.

## Utilisation

1. Entrer une IP ou un domaine (ex: `127.0.0.1`)
2. Définir la plage de ports (ex: `1-1024`)
3. Cliquer sur **Scanner**
4. Exporter les résultats en CSV si besoin

> ⚠️ Scanner une machine sans autorisation est illégal. Pour tester : utiliser `127.0.0.1` (localhost) ou `scanme.nmap.org` (serveur de test officiel nmap, autorisation explicite).

## Structure du projet

```
├── app.py              # Backend Flask — scan TCP + export CSV
├── requirements.txt    # Dépendances Python
├── assets/             # Screenshots
└── templates/
    └── index.html      # Interface web
```

## Contexte

Projet personnel développé pour approfondir les concepts réseau (TCP/IP, ports, sockets) et les mettre en pratique via un outil concret.  
Développé par Danee Ayasamy — étudiant ingénieur CESI Lyon.
