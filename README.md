# Election Scraper

Třetí projekt na Python Akademii od Engeta.

## Popis projektu
Tento skript slouží ke scrapování výsledků voleb z webu [volby.cz](https://www.volby.cz/). Po zadání URL adresy okresu stáhne a zpracuje výsledky voleb pro všechny obce v daném okrese a uloží je do CSV souboru.

## Instalace knihoven
Pro správné fungování skriptu je třeba mít nainstalované následující knihovny:

```sh
pip install requests beautifulsoup4
```

## Spuštění projektu
Projekt se spouští příkazem:

```sh
python election_scraper.py "URL" "NAZEV_SOUBORU.csv"
```

Kde:
- `URL` je odkaz na konkrétní okres z webu volby.cz
- `NAZEV_SOUBORU.csv` je název výstupního souboru

### Ukázka spuštění pro okres Karviná

```sh
python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103" "vysledky_karvina.csv"
```

### Průběh programu v konzoli:
```sh
Downloading data from selected URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103
Saving data to file: vysledky_karvina.csv
All done, closing...
```

## Částečný výstup CSV

```csv
Code,Location,Registered,Envelopes,Valid,Party 1,Party 2,Party 3,Party 4,...
12345,Karviná,50000,40000,39000,15000,12000,8000,4000,...
12346,Havířov,35000,29000,28500,10000,9000,6000,3500,...
...
```

Soubor obsahuje ID obce, název obce, počet registrovaných voličů, vydané obálky, platné hlasy a hlasy pro jednotlivé strany.

---

Tento projekt byl vytvořen jako součást třetího projektu Python Akademie od Engeta.

