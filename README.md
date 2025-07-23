# EduFlex 📚 - Version Démo

**Générateur automatique de planning scolaire - Démonstration**

> ⚠️ **Important**: Cette version publique est une **démonstration** des capacités d'EduFlex. L'algorithme complet d'optimisation et les fonctionnalités avancées sont disponibles dans la version complète du logiciel.

EduFlex est une solution moderne qui révolutionne la création de plannings éducatifs en automatisant l'assignation optimale des cours, professeurs, classes et salles.

## 🎯 Vision du Projet

Transformer la planification scolaire complexe en un processus fluide et optimisé grâce à des algorithmes avancés et une interface utilisateur intuitive.

## ✨ Fonctionnalités Démontrées

- **Interface Web Moderne** : Configuration simple via formulaire responsive
- **Architecture Modulaire** : Backend FastAPI + Frontend JavaScript  
- **Gestion des Ressources** : Attribution des professeurs, classes et salles
- **Planning de Base** : Génération automatique sur 5 jours ouvrés
- **Analyse Simple** : Statistiques par professeur et classe

## 🚀 Fonctionnalités Complètes (Version Payante)

### Algorithmes Avancés
- **Optimisation Multi-Contraintes** : Maximisation intelligente des ressources
- **Résolution de Conflits** : Gestion automatique des incompatibilités  
- **Planification Parallèle** : Cours simultanés selon disponibilités
- **Contraintes Complexes** : Matières, horaires, disponibilités personnalisées

### Fonctionnalités Entreprise
- **Gestion Multi-Établissements** : Réseau d'écoles
- **Import/Export** : Excel, PDF, Google Calendar
- **API Complète** : Intégrations tierces
- **Multi-Utilisateurs** : Permissions et collaboration
- **Analytics Avancées** : Rapports et statistiques détaillées

## 🏗️ Architecture (Version Démo)

```
├── backend/
│   ├── models.py           # Classes métier (Salle, Professeur, Classe)
│   ├── sheduler_demo.py    # Algorithme simplifié pour démonstration
│   └── app.py             # API FastAPI
└── frontend/
    ├── index.html         # Interface utilisateur
    ├── script.js          # Logique client
    └── style.css          # Design moderne
```

## 🛠️ Technologies

- **Backend** : Python, FastAPI, Pydantic
- **Frontend** : HTML5, CSS3, JavaScript ES6
- **Architecture** : REST API, Programmation Orientée Objet

## 🚀 Installation & Test

### Prérequis
- Python 3.8+

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

3. **Démarrer l'API (Version Démo)**
```bash
uvicorn app:app --reload --port 8000
```

4. **Ouvrir l'interface**
```
Ouvrir frontend/index.html dans votre navigateur
```

### Test de la Démo

1. **Configuration** : Remplissez le formulaire avec des valeurs de test
2. **Génération** : Cliquez sur "Générer le Planning"  
3. **Résultat** : Obtenez un planning basique pour évaluation

> 📧 **Contact pour Version Complète**: matzer667@github.com

## ⚡ Différences Version Démo vs Complète

| Fonctionnalité | Version Démo | Version Complète |
|---|---|---|
| Planning basique | ✅ | ✅ |
| Interface web | ✅ | ✅ |
| Optimisation avancée | ❌ | ✅ |
| Contraintes complexes | ❌ | ✅ |
| Cours parallèles | ❌ | ✅ |
| Export PDF/Excel | ❌ | ✅ |
| Multi-utilisateurs | ❌ | ✅ |
| Support technique | ❌ | ✅ |

## 🎯 Cas d'Usage

- **Écoles Primaires & Secondaires** : Planning hebdomadaire automatisé
- **Centres de Formation** : Optimisation des ressources  
- **Établissements Privés** : Gestion personnalisée

## 📈 Pourquoi EduFlex ?

✅ **Gain de Temps** : Automatisation complète de la planification  
✅ **Zéro Erreur** : Élimination des conflits et doublons  
✅ **Flexibilité** : Adaptation à tout type d'établissement  
✅ **Évolutif** : De la démo à l'entreprise

## 💼 Obtenir la Version Complète

Intéressé par l'algorithme complet et les fonctionnalités avancées ?

- 📧 **Email** : matzer667@github.com
- 🔗 **Demo Live** : [Sur demande]
- 💰 **Tarifs** : Selon besoins (école, district, région)

## 📝 Licence

Cette version démo est fournie à des fins d'évaluation uniquement.  
L'algorithme complet et les fonctionnalités avancées sont propriétaires.

---

*EduFlex - Simplifiez votre planification scolaire* 🎓
