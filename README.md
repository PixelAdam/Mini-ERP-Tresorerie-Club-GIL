# 🏦 Mini ERP — Trésorerie Club GIL

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-4f8ef7?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)

**Digitalisation du processus trésorerie du Club GIL**

*Développé par la Cellule Projet — Club GIL*

</div>

---

## 📌 Description

**Mini ERP Trésorerie** est une application web de gestion financière développée et mise en place par les membres de la cellule projet du Club GIL. Elle permet la digitalisation complète du processus trésorerie du club : suivi des membres, gestion des cotisations, planification budgétaire des événements, gestion des sponsors et journal des transactions financières.

---

## ✨ Fonctionnalités

### 👥 Gestion des Membres
- Ajout, modification et suppression des membres
- Suivi par cellule (Trésorerie, Formation, Sponsoring, Design, etc.)
- Gestion des niveaux d'étude (CP1, CP2, GIL1, GIL2, GIL3)
- Suivi du statut de cotisation (Payé / En attente)

### 💰 Cotisations
- Enregistrement des paiements de cotisation
- Historique des paiements par membre
- Statistiques : total collecté, taux de paiement

### 🗓️ Événements & Budget
- Création et planification des événements du club
- Gestion des postes budgétaires par événement
- Suivi du budget estimé vs sponsors confirmés
- Statuts : Planifié, En cours, Terminé, Annulé

### 🤝 Sponsors & Partenaires
- Répertoire des sponsors et partenaires
- Liaison sponsor ↔ événement
- Suivi des négociations (Confirmé / En négociation)
- Calcul automatique du total collecté

### 📊 Transactions & Trésorerie
- Journal comptable (Revenus / Dépenses)
- Calcul du solde net en temps réel
- Historique mensuel avec filtres
- Export CSV

### 📈 Dashboard
- Vue d'ensemble de la situation financière
- KPI : solde, revenus, dépenses, taux de cotisation
- Graphique d'évolution mensuelle
- 5 dernières transactions

---

## 🛠️ Technologies utilisées

### Backend
| Technologie | Version | Rôle |
|-------------|---------|------|
| **Python** | 3.11+ | Langage principal |
| **FastAPI** | 0.111 | Framework API REST |
| **SQLAlchemy** | 2.0 | ORM — communication avec MySQL |
| **PyMySQL** | 1.1 | Connecteur MySQL pour Python |
| **Pydantic** | 2.7 | Validation des données |
| **Uvicorn** | 0.29 | Serveur ASGI |
| **python-dotenv** | 1.0 | Gestion des variables d'environnement |

### Frontend
| Technologie | Rôle |
|-------------|------|
| **HTML5** | Structure de l'interface |
| **CSS3** | Mise en page et design |
| **JavaScript (ES2022)** | Logique client, appels API (`fetch`) |
| **Syne / Instrument Sans / DM Mono** | Typographies (Google Fonts) |

### Base de données
| Technologie | Version | Rôle |
|-------------|---------|------|
| **MySQL** | 8.0 | Base de données relationnelle |

### Outils & DevOps
| Outil | Rôle |
|-------|------|
| **Git** | Versioning du code |
| **GitHub** | Hébergement du repository |
| **MySQL Workbench** | Modélisation de la base de données |

---

## 🗂️ Structure du projet

```
Mini-ERP-Tresorerie-Club-GIL/
│
├── BD/
│   └── BD_mini_erp.sql          # Script de création de la base de données
│
├── Interface/
│   └── app_html_version3.html   # Interface utilisateur (frontend)
│
├── backend/
│   ├── app/
│   │   ├── main.py              # Point d'entrée FastAPI
│   │   ├── database.py          # Connexion MySQL
│   │   ├── models/              # Modèles SQLAlchemy (tables)
│   │   │   ├── membre.py
│   │   │   ├── cotisation.py
│   │   │   ├── evenement.py
│   │   │   ├── sponsor.py
│   │   │   ├── sponsorisation.py
│   │   │   └── transaction.py
│   │   ├── schemas/             # Validation Pydantic
│   │   │   ├── membre.py
│   │   │   ├── cotisation.py
│   │   │   ├── evenement.py
│   │   │   ├── sponsor.py
│   │   │   └── transaction.py
│   │   └── routers/             # Endpoints API
│   │       ├── membres.py
│   │       ├── cotisations.py
│   │       ├── evenements.py
│   │       ├── sponsors.py
│   │       └── transactions.py
│   ├── requirements.txt
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

## 🚀 Installation & Lancement

### Prérequis
- Python 3.11+
- MySQL 8.0
- Git

### Étapes

**1. Cloner le projet**
```bash
git clone https://github.com/PixelAdam/Mini-ERP-Tresorerie-Club-GIL.git
cd Mini-ERP-Tresorerie-Club-GIL
```

**2. Créer la base de données**
```sql
-- Dans MySQL 8.0 Command Line Client
CREATE DATABASE erp;
EXIT;
```
```bash
mysql -u root -p < BD/BD_mini_erp.sql
```

**3. Installer le backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

**4. Configurer les variables d'environnement**
```bash
copy .env.example .env
# Éditer .env avec vos identifiants MySQL
```
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_NAME=erp
```

**5. Lancer le backend**
```bash
uvicorn app.main:app --reload
```

**6. Ouvrir l'interface**

Double-clic sur `Interface/app_html_version3.html` dans votre navigateur.

---

## 📡 API — Endpoints disponibles

| Module | Endpoint | Méthodes |
|--------|----------|----------|
| Membres | `/membres/` | GET, POST, PUT, DELETE |
| Cotisations | `/cotisations/` | GET, POST, PUT, DELETE |
| Événements | `/evenements/` | GET, POST, PUT, DELETE |
| Sponsors | `/sponsors/` | GET, POST, PUT, DELETE |
| Sponsorisations | `/sponsors/sponsorisations` | POST, DELETE |
| Transactions | `/transactions/` | GET, POST, PUT, DELETE |
| Stats Trésorerie | `/transactions/stats` | GET |
| Stats Mensuel | `/transactions/stats/mensuel` | GET |

📖 Documentation interactive complète : **http://localhost:8000/docs**

---

## 🗄️ Modèle de la base de données

```
membre          cotisation          evenement
──────          ──────────          ─────────
id_membre  ←── id_membre            id_evenement
nom             date_paiement            ↑
prenom          montant           sponsorisation
niveau_etude                      ──────────────
cellule         transaction_club   id_sponsor ──→ sponsor
montant_cot     ───────────────               nom_entreprise
                id_transaction                montant_accorde
                date_transaction              statut
                montant
                type (income/expense)
                description
```

---

## 👥 Équipe

Projet développé par la **Cellule Projet du Club GIL**

---

## 📄 Licence

Projet interne — Club GIL © 2026
