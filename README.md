# 🎓 Plateforme de Formation à Distance — EST-Salé

> **Projet de Fin d'Études (PFE)**  
> Diplôme Universitaire de Technologie — Spécialité : Systèmes Informatiques et Réseaux (SIR)  
> École Supérieure de Technologie de Salé — Université Mohammed V de Rabat  
> Année universitaire : 2024-2025

---

## 👥 Réalisé par

- Ali Ait Taleb  
- Ahmade Amine Gaougaou  
- Khaoula Chhiba  
- Amine El Hannouni  

**Encadrants :** Pr. Mounir Amraoui — Pr. Adil Hilmani

---

## 📖 Description du projet

Ce projet consiste à concevoir et déployer une **infrastructure numérique sécurisée** destinée à l'ensemble de la communauté de l'EST-Salé (étudiants, enseignants, personnel administratif). Il propose une plateforme de formation à distance accessible depuis les locaux de l'établissement et depuis l'extérieur via Internet.

La solution couvre deux volets principaux :

- **Application web** : chat en temps réel, gestion des comptes, e-learning, tableau de bord administrateur
- **Infrastructure réseau** : sécurisation avec pare-feu, VLANs, VPN, Radius, IDS/IPS, supervision Nagios

---

## ✨ Fonctionnalités de l'application

### 👤 Authentification & Comptes
- Inscription avec validation des champs (nom, prénom, username, email, mot de passe)
- Approbation des comptes par l'administrateur avant accès à la plateforme
- Historique de connexion (IP, date, action)

### 💬 Chat en temps réel
- Messagerie privée entre étudiants via WebSocket (Socket.IO)
- Création de groupes de discussion avec sélection des membres
- Indicateur de présence en ligne 🟢 / hors ligne 🔴

### 🎓 E-Learning
- Tableau de bord e-learning avec accès aux ressources pédagogiques
- Ajout et gestion de ressources par les enseignants
- Suivi de la progression des étudiants
- Analyses et statistiques

### 🛡️ Administration
- Panel admin complet : approbation, rejet, bannissement des comptes
- Visualisation de tous les étudiants et de leurs statuts
- Historique des connexions avec adresses IP

---

## 🛠️ Technologies utilisées

### Application web

| Catégorie | Technologie |
|-----------|-------------|
| Backend principal | Python, Flask, Flask-SocketIO |
| Base de données | Apache Cassandra (NoSQL / Big Data) |
| ORM | Flask-SQLAlchemy |
| Temps réel | Socket.IO 4.x |
| API REST | FastAPI, Uvicorn, Pydantic |
| Frontend | HTML5, CSS3, JavaScript vanilla |
| Sécurité | Flask-CORS, gestion des sessions |

### Infrastructure réseau

| Composant | Technologie / Équipement |
|-----------|--------------------------|
| Pare-feu (NGFW) | Pare-feu 200-B |
| Switch | Cisco 2960-C |
| Points d'accès | TD8960 |
| Authentification centralisée | RADIUS (PEAP/WPA2) |
| VPN | Tunnel sécurisé site-à-site |
| Supervision | Nagios XI + SNMP |
| Détection d'intrusions | Snort (IDS/IPS) |
| Annuaire | Active Directory + DNS |
| Segmentation réseau | VLANs (LAN, DMZ, WAN) |
| OS Serveurs | Linux Ubuntu, Windows Server 2016 |

---

## 🏗️ Architecture réseau

L'infrastructure est organisée en trois zones :

- **LAN (réseau local)** — Séparé en VLANs par profil (étudiants, enseignants, serveurs, administration)
- **DMZ (zone démilitarisée)** — Héberge le frontend de la plateforme, accessible depuis Internet
- **WAN** — Accès Internet sécurisé via le pare-feu

### Table des VLANs

| VLAN | Rôle |
|------|------|
| VLAN 10 | Administration |
| VLAN 20 | Étudiants |
| VLAN 30 | Serveurs |
| VLAN 50 | Enseignants |
| VLAN 60 | Autre |

---

## ⚙️ Prérequis

- Python 3.8+
- Apache Cassandra
- MySQL (pour l'API FastAPI)
- pip

---

## 🚀 Installation

**1. Cloner le dépôt**

```bash
git clone https://github.com/votre-utilisateur/plateforme-est-sale.git
cd plateforme-est-sale
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

Modifier la connexion à la base de données dans `app.py` :

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/app'
```

Créer la base de données :

```sql
CREATE DATABASE app;
```

Les tables sont créées automatiquement au premier lancement.

---

## ▶️ Lancement

**Application Flask principale (chat + interface web) :**

```bash
python app.py
```

Accessible sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

**API REST FastAPI (gestion utilisateurs) :**

```bash
python main.py
```

Accessible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Documentation interactive : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Structure du projet

```
plateforme-est-sale/
│
├── app.py              # Application Flask principale (routes, modèles, SocketIO)
├── main.py             # API REST FastAPI indépendante (CRUD utilisateurs)
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

> ⚠️ **Important** : Changer la `secret_key` dans `app.py` et le mot de passe admin avant toute mise en production.

---

## 📚 Abréviations

| Sigle | Signification |
|-------|---------------|
| EST | École Supérieure de Technologie |
| VPN | Virtual Private Network |
| IDS/IPS | Intrusion Detection/Prevention System |
| VLAN | Virtual Local Area Network |
| DMZ | Demilitarized Zone |
| RADIUS | Remote Authentication Dial-In User Service |
| SNMP | Simple Network Management Protocol |
| NGFW | Next-Generation Firewall |
| STP | Spanning Tree Protocol |
| SSID | Service Set Identifier |
