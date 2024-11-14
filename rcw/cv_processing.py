import openai
from django.conf import settings

# Assurez-vous que la clé API est définie
openai.api_key = settings.OPENAI_API_KEY

def extract_competences(cv_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Analyse ce fichier et extraits-en les compétences professionnelles: il y'a un titre competences je voudrais que tu extrait tout les element de ce titre  : {cv_text}"}
            ],
            max_tokens=200,
            temperature=0.2
        )

        competences = response.choices[0].message['content'].strip()
        
        # Vérifiez si des compétences ont été extraites
        if competences:
            # Transformez les compétences en une liste si nécessaire
            return [comp.strip() for comp in competences.split(",") if comp.strip()]
        else:
            return []

    except Exception as e:
        print("Erreur lors de l'appel à l'API OpenAI :", e)
        return []
