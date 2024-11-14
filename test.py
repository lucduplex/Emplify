# test_openai_api.py

import openai
from dotenv import load_dotenv
import os

# Chargez les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai_competence_extraction():
    # Texte d'exemple à analyser
    test_text = "Compétences : Python, gestion de projet, communication"

    try:
        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Analyse ce texte et extraits-en les compétences : {test_text}"}
            ],
            max_tokens=100,
            temperature=0.2
        )

        # Affichage de la réponse brute
        competences = response.choices[0].message['content'].strip()
        print("Réponse de l'API :", competences)

    except Exception as e:
        print("Erreur lors de l'appel à l'API OpenAI :", e)

# Exécutez la fonction de test
if __name__ == "__main__":
    test_openai_competence_extraction()
