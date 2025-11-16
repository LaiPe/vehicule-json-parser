# Vehicle JSON Parser

Un script Python pour extraire et transformer des attributs spécifiques à partir de jeux de données de véhicules électriques, avec conversion automatique d'unités et calculs dérivés.

## Aperçu

Ce script traite des jeux de données JSON contenant les spécifications de véhicules électriques et extrait un sous-ensemble d'attributs pertinents. Il convertit automatiquement la consommation énergétique de kWh/100 miles vers kWh/100 km et calcule la capacité de la batterie basée sur les données de charge.

## Source des données

Le script est conçu pour fonctionner avec des données de véhicules électriques provenant de :
- **Source** : https://public.opendatasoft.com/explore/dataset/all-vehicles-model/information/?flg=fr-fr&sort=modifiedon&refine.fueltype=Electricity
- **Format** : Tableau JSON d'objets véhicules
- **Contenu** : Données de certification EPA de véhicules avec spécifications techniques

## Fonctionnalités

- Extrait 3 attributs de base des données de véhicules (make, model, year)
- Convertit la consommation énergétique de l'impérial (kWh/100 miles) vers le métrique (kWh/100 km)
- Calcule automatiquement la capacité de la batterie basée sur le temps de charge et la puissance
- Gère les valeurs manquantes de manière élégante
- Fournit un aperçu des données et des statistiques de taille de fichier
- Interface en ligne de commande interactive en français

## Attributs extraits

| Attribut original | Attribut de sortie | Description |
|-------------------|------------------|-------------|
| `make` | `make` | Fabricant du véhicule |
| `model` | `model` | Nom complet du modèle |
| `year` | `year` | Année du modèle |
| `combe` | `consumption_kwh_per_100km` | Consommation énergétique (convertie en kWh/100km) |
| `charge240` + calcul | `battery_capacity_kwh` | Capacité de la batterie calculée (kWh) |

## Calculs automatiques

Le script effectue deux calculs automatiques :

1. **Conversion de consommation** : Convertit `combe` (kWh/100 miles) vers kWh/100 km
2. **Capacité de batterie** : Calcule la capacité en utilisant la formule :
   ```
   Capacité (kWh) = Temps de charge (heures) × Puissance de charge (7.2 kW)
   ```

## Prérequis

- Python 3.6 ou supérieur
- Aucune dépendance externe (utilise uniquement la bibliothèque standard)

## Utilisation

1. **Préparez votre fichier de données** :
    - Téléchargez le jeu de données depuis l'URL source ci-dessus
    - Sauvegardez-le sous `vehicles_data_original.json` ou utilisez un nom personnalisé

2. **Exécutez le script** :
   ```bash
   python vehicule-json-parser.py
   ```

3. **Suivez les invites** :
    - Entrez le nom du fichier d'entrée (défaut : `vehicles_data_original.json`)
    - Entrez le nom du fichier de sortie (défaut : `vehicles_data_extracted.json`)
    - Choisissez si vous voulez prévisualiser les résultats

## Exemple de sortie

```json
[
  {
    "make": "Tesla",
    "model": "Model S AWD - P100D",
    "year": "2017",
    "consumption_kwh_per_100km": 21.75,
    "battery_capacity_kwh": 86.4
  },
  {
    "make": "Nissan",
    "model": "LEAF",
    "year": "2018",
    "consumption_kwh_per_100km": 18.65,
    "battery_capacity_kwh": 43.2
  }
]
```

## Conversions d'unités

Le script convertit automatiquement la consommation énergétique en utilisant la formule :
```
kWh/100km = kWh/100miles × (100 ÷ 160.9344)
```

Où 160.9344 km = 100 miles (1 mile = 1.609344 km)

## Calcul de la capacité de batterie

La capacité de la batterie est calculée en utilisant :
```
Capacité (kWh) = Temps de charge 240V (heures) × 7.2 kW
```

*Note : Une puissance de charge de 7.2 kW est assumée pour les calculs.*

## Gestion des erreurs

- Les fichiers JSON invalides sont détectés et signalés
- Les attributs manquants sont traités gracieusement avec des messages d'avertissement
- Les erreurs de conversion résultent en valeurs `null`
- Les erreurs d'E/S de fichier sont capturées et affichées
- Les véhicules sans données essentielles (`combe` ou `range`) sont ignorés avec des messages informatifs

## Licence

Ce script est fourni tel quel à des fins de traitement de données. Veuillez respecter les conditions d'utilisation de la source de données originale.