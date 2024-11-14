# app/gpt_helper.py
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def extract_competences_from_cv(cv_text):
    prompt = f"Extract the skills from this CV: {cv_text}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    competences = response.choices[0].text.strip().split(', ')
    return competences
