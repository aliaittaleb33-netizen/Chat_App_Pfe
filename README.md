# 🎓 Student Chat App

Application web de messagerie en temps réel pour étudiants, avec gestion des comptes et panel d'administration.

---

## 📋 Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [Structure du projet](#structure-du-projet)
- [API REST (FastAPI)](#api-rest-fastapi)
- [Identifiants par défaut](#identifiants-par-défaut)

---

## 📖 Aperçu

Cette application permet à des étudiants de s'inscrire, d'être approuvés par un administrateur, puis de communiquer entre eux via un chat privé ou en groupe, en temps réel.

---

## ✨ Fonctionnalités

- **Inscription & Connexion** — Création de compte avec validation des champs
- **Approbation admin** — Les nouveaux comptes doivent être approuvés avant de pouvoir se connecter
- **Chat privé** — Messagerie en temps réel entre deux étudiants via WebSocket
- **Chat de groupe** — Création de groupes avec sélection de membres et messagerie collective
- **Statut en ligne** — Indicateur 🟢/🔴 de présence en temps réel
- **Panel admin** — Gestion des étudiants (approbation, rejet, bannissement) et historique de connexion
- **API REST séparée** — Backend FastAPI indépendant pour la gestion CRUD des utilisateurs

---

## 🛠️ Technologies utilisées

| Catégorie | Technologie |
|-----------|-------------|
| Backend principal | Python, Flask, Flask-SocketIO |
| ORM / Base de données | Flask-SQLAlchemy, MySQL (PyMySQL) |
| Temps réel | Socket.IO 4.x |
| API REST | FastAPI, Uvicorn, Pydantic |
| Frontend | HTML, CSS, JavaScript vanilla |
| Autre | Flask-CORS |

---

## ⚙️ Prérequis

- Python 3.8+
- MySQL (port `3307` par défaut dans la config)
- pip

---

## 🚀 Installation

**1. Cloner le dépôt**

```bash
git clone https://github.com/votre-utilisateur/student-chat-app.git
cd student-chat-app
```

**2. Créer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Installer les dépendances**

```bash
pip install flask flask-sqlalchemy flask-socketio flask-cors pymysql fastapi uvicorn pydantic
```

---

## 🔧 Configuration

Ouvrir `app.py` et modifier la ligne suivante selon votre configuration MySQL :

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/app'
```

Remplacer `root`, le mot de passe (vide par défaut), `localhost:3307` et `app` selon votre environnement.

Créer la base de données MySQL :

```sql
CREATE DATABASE app;
```

Les tables sont créées automatiquement au premier lancement.

---

## ▶️ Lancement

**Application Flask (chat + interface web) :**

```bash
python app.py
```

L'application sera accessible sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

**API REST FastAPI (optionnel) :**

```bash
python main.py
```

L'API sera accessible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Documentation interactive : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Structure du projet

```
student-chat-app/
│
├── app.py              # Application Flask principale (routes, modèles, SocketIO)
├── main.py             # API REST FastAPI indépendante
│
├── templates/
│   ├── login.html      # Page de connexion
│   ├── register.html   # Page d'inscription
│   ├── chat.html       # Interface de chat (privé + groupes)
│   └── admin.html      # Panel d'administration
│
└── static/
    ├── style.css       # Feuille de styles globale
    └── chat-box.js     # Logique Socket.IO côté client
```

---

## 🔌 API REST (FastAPI)

L'API `main.py` expose les endpoints suivants pour la gestion des utilisateurs :

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/users` | Lister tous les utilisateurs |
| `POST` | `/users` | Créer un utilisateur |
| `GET` | `/users/{id}` | Récupérer un utilisateur par ID |
| `PUT` | `/users/{id}` | Modifier un utilisateur |
| `DELETE` | `/users/{id}` | Supprimer un utilisateur |

---

## 🔑 Identifiants par défaut

| Rôle | Nom d'utilisateur | Mot de passe |
|------|-------------------|--------------|
| Administrateur | `admin` | `admin123` |

> ⚠️ **Important** : Changez la `secret_key` dans `app.py` et le mot de passe admin avant toute mise en production.
