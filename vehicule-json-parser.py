#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def convert_kwh_per_100miles_to_100km(kwh_per_100miles: float) -> float | None:
    """
    Convertit la consommation de kWh/100 miles vers kWh/100 km

    Args:
        kwh_per_100miles (float): Consommation en kWh/100 miles

    Returns:
        float: Consommation en kWh/100 km (arrondie à 2 décimales)
    """
    if kwh_per_100miles is None:
        return None

    # 1 mile = 1.609344 km
    # Donc 100 miles = 160.9344 km
    # Conversion: kwh/100miles * (100 km / 160.9344 km)
    miles_to_km_factor = 1.609344
    kwh_per_100km = kwh_per_100miles * (100 / (100 * miles_to_km_factor))

    return round(kwh_per_100km, 2)

def extract_vehicle_attributes(input_file: str, output_file: str) -> None:
    """
    Extrait les attributs spécifiés des données de véhicules électriques
    et sauvegarde le résultat dans un nouveau fichier JSON.

    Args:
        input_file (str): Chemin vers le fichier JSON d'entrée
        output_file (str): Chemin vers le fichier JSON de sortie
    """

    # Dictionnaire des attributs à extraire avec leur nom de sortie
    # Format: 'nom_original': 'nom_sortie' ou 'nom_original': None (garde le même nom)
    attributes_mapping = {
        'make': None,
        'model': None,
        'basemodel': None,
        'year': None,
        'combe': 'cons_kwh_per_100km',      # Consommation électrique combinée (avec conversion)
        'range': None,           # Autonomie
        'charge240': 'time_charge240',       # Temps recharge 240V standard
        'charge240b': 'time_charge240b',     # Temps recharge 240V rapide
        'c240dscr': None,        # Description chargeur 240V standard
        'c240bdscr': None,       # Description chargeur 240V rapide
        'modifiedon': None       # Date de modification
    }

    try:
        # Lecture du fichier JSON d'entrée
        print(f"📂 Lecture du fichier : {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Vérification du format des données
        if not isinstance(data, list):
            raise ValueError("Le fichier JSON doit contenir une liste d'objets")

        print(f"✅ {len(data)} véhicules trouvés dans le fichier")

        # Extraction des attributs pour chaque véhicule
        extracted_data = []

        for i, vehicle in enumerate(data):
            if not isinstance(vehicle, dict):
                print(f"⚠️  Élément {i} ignoré (pas un objet JSON valide)")
                continue

            # Création du nouvel objet avec les attributs sélectionnés
            extracted_vehicle = {}

            for original_attr, output_attr in attributes_mapping.items():
                # Récupération de la valeur (None si l'attribut n'existe pas)
                value = vehicle.get(original_attr, None)

                # Traitement spécial pour la consommation électrique (conversion d'unité)
                if original_attr == 'combe' and value is not None:
                    value = convert_kwh_per_100miles_to_100km(float(value))


                # Utilise le nom de sortie spécifié ou garde le nom original
                final_attr_name = output_attr if output_attr is not None else original_attr
                extracted_vehicle[final_attr_name] = value

            extracted_data.append(extracted_vehicle)

        # Sauvegarde du fichier de sortie
        print(f"💾 Sauvegarde vers : {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Extraction terminée ! {len(extracted_data)} véhicules traités")
        print(f"📊 Taille fichier original : {os.path.getsize(input_file) / 1024:.1f} KB")
        print(f"📊 Taille fichier extrait : {os.path.getsize(output_file) / 1024:.1f} KB")

    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {input_file} n'existe pas")
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de format JSON : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")

def preview_extracted_data(file_path: str, num_items: int = 3) -> None:
    """
    Affiche un aperçu des données extraites

    Args:
        file_path (str): Chemin vers le fichier JSON extrait
        num_items (int): Nombre d'éléments à afficher
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n🔍 Aperçu des {min(num_items, len(data))} premiers véhicules :")
        print("=" * 60)

        for i, vehicle in enumerate(data[:num_items]):
            print(f"\n🚗 Véhicule {i+1}:")
            for key, value in vehicle.items():
                if value is not None:
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: N/A")
            print("-" * 40)

    except Exception as e:
        print(f"❌ Erreur lors de l'aperçu : {e}")

def main():
    """Fonction principale"""
    print("🔋 Extracteur d'attributs pour véhicules électriques")
    print("=" * 50)

    # Configuration des fichiers (modifiez selon vos besoins)
    input_file = "vehicles_data_original.json"  # Votre fichier d'entrée
    output_file = "vehicles_data_extracted.json"  # Fichier de sortie

    # Demande à l'utilisateur les noms de fichiers
    user_input = input(f"Nom du fichier d'entrée [{input_file}]: ").strip()
    if user_input:
        input_file = user_input

    user_output = input(f"Nom du fichier de sortie [{output_file}]: ").strip()
    if user_output:
        output_file = user_output

    # Extraction des données
    extract_vehicle_attributes(input_file, output_file)

    # Aperçu des résultats
    if os.path.exists(output_file):
        show_preview = input("\n👀 Afficher un aperçu des données extraites ? (o/N): ").strip().lower()
        if show_preview in ['o', 'oui', 'y', 'yes']:
            preview_extracted_data(output_file)

if __name__ == "__main__":
    main()