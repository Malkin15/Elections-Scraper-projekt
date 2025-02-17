"""
election_scraper.py: Třetí projekt do Engeto Python Akademie
author: Roman Šimík
email: simik@sonet.cz
discord: malkin8729
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def main():
    """Hlavní funkce scraperu volebních výsledků."""
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    url, file_name = check_arguments(base_url)

    print(f"Stahuji data z vybraného URL: {url}")
    
    first_soup = get_html(url)
    if first_soup is None:
        sys.exit(1)
    
    results, header = get_municipality_links(first_soup, base_url)
    if not results:
        sys.exit(1)
    
    print(f"Ukládám data do souboru: {file_name}")
    save_to_csv(results, header, file_name)
    print("Vše hotovo, zavírám...")

def check_arguments(base_url):
    """Kontrola argumentů příkazového řádku."""
    if len(sys.argv) != 3:
        sys.exit(1)
    if not sys.argv[1].startswith(base_url) or not sys.argv[2].endswith(".csv"):
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def get_html(url):
    """Stáhne HTML stránku z dané URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException:
        return None

def get_municipality_links(first_soup, base_url):
    """Získá odkazy na obce a připraví hlavičku CSV."""
    results = []
    names = [name.text.strip() for name in first_soup.find_all('td', {'class': 'overflow_name'})]
    td_elements = first_soup.find_all('td', {'class': 'cislo'})

    for index, each_td in enumerate(td_elements):
        if index >= len(names):
            continue
        
        line = [each_td.text, names[index]]
        link = each_td.a['href'] if each_td.a else None
        if not link:
            continue
        
        soup = get_html(base_url + link)
        if soup is None:
            continue
        
        if index == 0:
            header = create_header(soup)
        
        line.extend(collect_numbers(soup))
        results.append(line)
    
    return results, header

def collect_numbers(second_soup):
    """Získá volební údaje pro obec."""
    try:
        data = [
            clean_numbers(second_soup.find('td', {'headers': 'sa2'}).text),
            clean_numbers(second_soup.find('td', {'headers': 'sa5'}).text),
            clean_numbers(second_soup.find('td', {'headers': 'sa6'}).text)
        ]
        data.extend(collect_votes(second_soup))
        return data
    except AttributeError:
        return []

def clean_numbers(number):
    """Odstraní mezery a neviditelné znaky."""
    return number.replace("\xa0", "").strip()

def create_header(second_soup):
    """Vytvoří hlavičku CSV."""
    return ["Code", "Location", "Registered", "Envelopes", "Valid"] + \
           [party.text.strip() for party in second_soup.find_all('td', {'class': 'overflow_name'})]

def collect_votes(second_soup):
    """Získá hlasy pro každou stranu."""
    votes = []
    for number in range(1, len(second_soup.find_all('table'))):
        votes.extend(
            [clean_numbers(vote.text) for vote in second_soup.find_all('td', {'headers': f't{number}sa2 t{number}sb3'})]
        )
    return votes

def save_to_csv(results, header, file):
    """Uloží data do CSV souboru."""
    try:
        with open(file, "w", encoding="utf-8", newline="") as csv_s:
            writer = csv.writer(csv_s, dialect="excel")
            writer.writerow(header)
            writer.writerows(results)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()