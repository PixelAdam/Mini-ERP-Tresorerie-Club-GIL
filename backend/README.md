# Mini ERP Club GIL — Backend API

API REST développée avec **FastAPI + SQLAlchemy + MySQL**.

---

## Structure du projet

```
mini-erp-backend/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── database.py          # Connexion MySQL
│   ├── models/              # Modèles SQLAlchemy (tables BD)
│   │   ├── membre.py
│   │   ├── cotisation.py
│   │   ├── evenement.py
│   │   ├── sponsor.py
│   │   ├── sponsorisation.py
│   │   └── transaction.py
│   ├── schemas/             # Validation des données (Pydantic)
│   │   ├── membre.py
│   │   ├── cotisation.py
│   │   ├── evenement.py
│   │   ├── sponsor.py
│   │   └── transaction.py
│   └── routers/             # Endpoints de l'API
│       ├── membres.py
│       ├── cotisations.py
│       ├── evenements.py
│       ├── sponsors.py
│       └── transactions.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Installation

### 1. Cloner le projet et créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données
```bash
cp .env.example .env
# Éditer .env avec vos identifiants MySQL
```

### 4. Importer le schéma SQL
```bash
mysql -u root -p < BD_mini_erp.sql
```

### 5. Lancer le serveur
```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur **http://localhost:8000**
Documentation Swagger : **http://localhost:8000/docs**

---

## Endpoints disponibles

### 👥 Membres — `/membres`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/membres/` | Lister tous les membres |
| GET | `/membres/{id}` | Détails d'un membre |
| POST | `/membres/` | Créer un membre |
| PUT | `/membres/{id}` | Modifier un membre |
| DELETE | `/membres/{id}` | Supprimer un membre |

### 💰 Cotisations — `/cotisations`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/cotisations/` | Lister toutes les cotisations |
| GET | `/cotisations/stats` | Stats (total, taux de paiement) |
| POST | `/cotisations/` | Enregistrer un paiement |
| PUT | `/cotisations/{id}` | Modifier |
| DELETE | `/cotisations/{id}` | Supprimer |

### 🗓️ Événements — `/evenements`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/evenements/` | Lister tous les événements |
| GET | `/evenements/stats` | Stats par statut |
| POST | `/evenements/` | Créer un événement |
| PUT | `/evenements/{id}` | Modifier |
| DELETE | `/evenements/{id}` | Supprimer |

### 🤝 Sponsors — `/sponsors`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/sponsors/` | Lister tous les sponsors |
| GET | `/sponsors/stats` | Stats (montant confirmé, etc.) |
| POST | `/sponsors/` | Ajouter un sponsor |
| PUT | `/sponsors/{id}` | Modifier |
| DELETE | `/sponsors/{id}` | Supprimer |
| GET | `/sponsors/{id}/evenements` | Événements d'un sponsor |
| POST | `/sponsors/sponsorisations` | Lier sponsor ↔ événement |
| DELETE | `/sponsors/sponsorisations/{sp}/{ev}` | Délier |

### 📊 Transactions — `/transactions`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/transactions/` | Lister toutes les transactions |
| GET | `/transactions/stats` | Solde, revenus, dépenses |
| GET | `/transactions/stats/mensuel` | Évolution mensuelle |
| POST | `/transactions/` | Enregistrer une transaction |
| PUT | `/transactions/{id}` | Modifier |
| DELETE | `/transactions/{id}` | Supprimer |

---

## Connexion avec le frontend HTML

Dans `app_html_version2.html`, remplacer les fonctions qui modifient `DB` local par des appels `fetch` :

```javascript
// Exemple : charger les membres au démarrage
async function loadMembres() {
    const res = await fetch("http://localhost:8000/membres/");
    const data = await res.json();
    // Mettre à jour l'affichage avec data
}

// Exemple : ajouter un membre
async function saveMembre(membre) {
    const res = await fetch("http://localhost:8000/membres/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(membre)
    });
    return await res.json();
}
```
