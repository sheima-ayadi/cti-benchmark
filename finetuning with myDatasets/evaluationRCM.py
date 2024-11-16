import pandas as pd
import re

# Charger votre dataset à partir du fichier CSV
df = pd.read_csv('our-cti-rcm-with-model-outputs.csv')

# Fonction pour extraire le code CWE (format CWE-XXX)
extract_cwe = lambda text: re.search(r'CWE-\d+', text).group(0) if re.search(r'CWE-\d+', text) else None

# Appliquer la fonction d'extraction sur les colonnes 'model_output' et comparer avec 'output'
df['extracted_model_output'] = df['model_outputs'].apply(extract_cwe)

# Calculer le nombre de prédictions correctes
correct_predictions = (df['output'] == df['extracted_model_output']).sum()

# Calculer le pourcentage d'exactitude
accuracy = (correct_predictions / len(df)) * 100

# Afficher la précision et les premières comparaisons
print(f"Précision du modèle : {accuracy:.2f}%")
print(df[['output', 'extracted_model_output']].head())
