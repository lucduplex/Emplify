import requests
from bs4 import BeautifulSoup
from .models import JobOffer, Recruteur

def scrape_indeed_jobs():
    url = "https://emplois.ca.indeed.com/jobs?q=pr%C3%A9pos%C3%A9+aux+b%C3%A9n%C3%A9ficiaires&l=Montr%C3%A9al%2C+QC&from=searchOnHP&vjk=f708994cb038ec2c"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="job_seen_beacon")

    for job_card in job_cards:
        title = job_card.find("h2", class_="jobTitle").get_text(strip=True)
        company = job_card.find("span", class_="companyName").get_text(strip=True)
        location = job_card.find("div", class_="companyLocation").get_text(strip=True)
        description = job_card.find("div", class_="job-snippet").get_text(strip=True)

        if not JobOffer.objects.filter(titre=title, description=description).exists():
            recruteur, _ = Recruteur.objects.get_or_create(user=None, entreprise=company)
            job_offer = JobOffer(
                recruteur=recruteur,
                titre=title,
                description=description,
                localisation=location
            )
            job_offer.save()
