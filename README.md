# EduFlex 📚

**Générateur automatique de planning scolaire intelligent**

EduFlex est une solution SaaS moderne qui révolutionne la création de plannings éducatifs en automatisant l'assignation optimale des cours, professeurs, classes et salles.

## 🎯 Vision du Projet

Transformer la planification scolaire complexe en un processus fluide, intelligent et optimisé grâce à des algorithmes avancés et une interface utilisateur intuitive.

## ✨ Fonctionnalités Actuelles

- **Interface Web Moderne** : Configuration simple via formulaire responsive
- **Algorithme Optimisé** : Attribution intelligente des ressources (prof/classe/salle)
- **Gestion des Contraintes** : Respect des capacités, effectifs et disponibilités
- **Planning Dynamique** : Génération automatique sur 7 jours avec créneaux personnalisables
- **Analyse Complète** : Statistiques détaillées par professeur et classe
- **Architecture Modulaire** : Backend FastAPI + Frontend JavaScript

## 🚀 Objectifs Finaux

### Performance & Optimisation
- **Algorithme Ultra-Optimisé** : Maximisation de l'utilisation des ressources
- **Traitement Rapide** : Génération efficace même pour grandes institutions
- **Scalabilité** : Support de milliers d'étudiants et professeurs

### Gestion Avancée
- **Multi-Contraintes** : Respect automatique des règles complexes
- **Résolution de Conflits** : Détection et résolution des incompatibilités
- **Flexibilité Totale** : Adaptation à tout type d'établissement

### Expérience Utilisateur
- **Interface Fluide** : UX/UI moderne avec feedback instantané
- **Personnalisation** : Configurations sur-mesure par établissement
- **Collaboration** : Gestion des droits et édition

### Fonctionnalités Avancées
- **Export Multi-Format** : PDF, Excel, iCal, Google Calendar
- **Notifications** : Alertes automatiques et rappels
- **Analyse** : Statistiques détaillées et rapports

## 🏗️ Architecture Technique

```
├── backend/
│   ├── models.py          # Classes métier (Salle, Professeur, Classe)
│   ├── sheduler.py        # Algorithme de planification
│   └── app.py            # API FastAPI
└── frontend/
    ├── index.html        # Interface utilisateur
    ├── script.js         # Logique client
    └── style.css         # Design moderne
```

## 🛠️ Technologies

- **Backend** : Python, FastAPI, Pydantic
- **Frontend** : HTML5, CSS3, JavaScript ES6
- **Architecture** : REST API, Programmation Orientée Objet
- **Optimisation** : Algorithmes de recherche et contraintes

## 🎯 Cas d'Usage

- **Écoles Primaires & Secondaires** : Planning hebdomadaire automatisé
- **Universités** : Gestion complexe multi-campus et multi-filières  
- **Centres de Formation** : Optimisation des ressources et formateurs
- **Écoles Spécialisées** : Contraintes métier et équipements spécifiques

## 📈 Avantages Concurrentiels

✅ **Gain de Temps** : 95% de réduction du temps de planification manuelle  
✅ **Optimisation Maximale** : Utilisation optimale des salles et professeurs  
✅ **Zéro Conflit** : Élimination des erreurs humaines et doublons  
✅ **Flexibilité Totale** : Adaptation à tout type d'établissement  
✅ **ROI Immédiat** : Retour sur investissement dès la première utilisation

## 🌟 Différenciation

EduFlex se distingue par son **algorithme propriétaire de maximisation des ressources** qui permet une utilisation optimale des créneaux horaires en programmant simultanément plusieurs cours parallèles selon la disponibilité des professeurs, classes et salles.

## 🔮 Roadmap

**Phase 1** ✅ : Prototype fonctionnel avec algorithme de base  
**Phase 2** 🚧 : Optimisation avancée et contraintes complexes  
**Phase 3** 📋 : Interface premium et fonctionnalités collaboratives  
**Phase 4** 🎯 : Analytics avancées et intégrations  
**Phase 5** 🚀 : Solution SaaS multi-tenant enterprise

## 🚀 Installation & Utilisation

### Prérequis
- Python 3.8+
- Node.js (pour le développement frontend)

### Installation Rapide

1. **Cloner le projet**
```bash
git clone https://github.com/matzer667/EduFlex.git
cd EduFlex
```

2. **Installer les dépendances Python**
```bash
cd backend
pip install fastapi uvicorn pydantic
```

3. **Démarrer l'API**
```bash
uvicorn app:app --reload --port 8000
```

4. **Ouvrir l'interface**
```
Ouvrir frontend/index.html dans votre navigateur
```

### Utilisation

1. **Configuration** : Remplissez le formulaire avec :
   - Heures de début/fin de journée
   - Nombre de professeurs, classes, salles
   - Effectifs min/max des classes
   - Capacités min/max des salles
   - Matières enseignées

2. **Génération** : Cliquez sur "Générer le Planning"

3. **Résultat** : Obtenez automatiquement :
   - Planning complet par jour/heure
   - Répartition des heures par professeur
   - Répartition des heures par classe
   - Statistiques d'utilisation

### API Endpoints

- `GET /` : Page d'accueil de l'API
- `POST /planning` : Génération de planning (JSON)

---

*EduFlex - L'avenir de la planification éducative* 🎓
