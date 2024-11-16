import pandas as pd
import re
from cvss import CVSS3

# Charger votre dataset à partir du fichier CSV
df = pd.read_csv('our-cti-vspwith-model-outputs.csv')

# Fonction pour extraire le vecteur CVSS (format CVSS:3.X/...)
def extract_cvss(text):
    match = re.search(r'CVSS:3\.\d/[A-Z]+:[A-Z](?:/[A-Z]+:[A-Z])*', text)
    return match.group(0) if match else None

# Fonction pour calculer le score CVSS à partir du vecteur
def get_cvss_score(cvss_vector):
    try:
        c = CVSS3(cvss_vector)
        return c.scores()[0]  # Récupère le score de base CVSS
    except Exception as e:
        print(f"Erreur lors de l'analyse du vecteur CVSS: {e}")
        return None

# Fonction pour calculer l'erreur absolue moyenne (MAD)
def compute_mad(df, pred_col, gt_col):
    error = 0
    total = 0
    
    # Boucle pour parcourir chaque ligne du DataFrame
    for idx, row in df.iterrows():
        pred = row[pred_col]
        gt = row[gt_col]
        
        # Extraire les vecteurs CVSS à partir des colonnes
        pred_vector = extract_cvss(pred)
        gt_vector = extract_cvss(gt)

        if pred_vector and gt_vector:
            try:
                pred_score = get_cvss_score(pred_vector)
                gt_score = get_cvss_score(gt_vector)
                
                if pred_score is not None and gt_score is not None:
                    # Ajouter l'erreur absolue
                    error += abs(pred_score - gt_score)
                    total += 1
                else:
                    print(f"Vecteurs CVSS invalides à la ligne {idx + 1}")
            except Exception as e:
                print(f"Erreur à la ligne {idx + 1}: {e}")
                continue
        else:
            print(f"Pas de vecteur CVSS extrait à la ligne {idx + 1}")
    
    if total == 0:
        print("Aucune prédiction valide pour calculer l'erreur.")
        return None

    mad = error / total  # Calculer l'erreur absolue moyenne
    print(f"Erreur absolue totale : {error}, Nombre total : {total}")
    return mad

# Comparer et calculer l'erreur entre les colonnes 'output' et 'model_outputs'
mad = compute_mad(df, pred_col='model_outputs', gt_col='output')

if mad is not None:
    print(f"Erreur absolue moyenne (MAD) : {mad:.2f}")
