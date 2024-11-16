import pandas as pd
import re

# Charger votre dataset à partir du fichier CSV
df = pd.read_csv('article-cti-rcm-with-model-outputs.csv')

# Fonction pour extraire le code CWE (format CWE-XXX)
def extract_cwe(text):
    match = re.search(r'CWE-\d+', text)
    return match.group(0) if match else None

# Extraire les colonnes 'output' et 'model_output'
output = df['output'].tolist()
model_output = df['model_outputs'].tolist()

# Vérifier que les deux listes ont la même longueur
if len(output) == len(model_output):
    # Initialiser le compteur pour les prédictions correctes
    correct_predictions = 0
    
    # Comparer chaque élément des deux listes après extraction du code CWE
    for i in range(len(output)):
        extracted_model_output = extract_cwe(model_output[i])
        print(f"Output attendu : {output[i]}, Output du modèle (extrait) : {extracted_model_output}")
        
        if output[i] == extracted_model_output:
            correct_predictions += 1  # Incrémenter si la prédiction est correcte

    # Calculer le pourcentage d'exactitude
    total_predictions = len(output)
    accuracy = (correct_predictions / total_predictions) * 100
    
    print(f"\nPrécision du modèle : {accuracy:.2f}%")
else:
    print("Les colonnes 'output' et 'model_output' n'ont pas la même longueur.")
