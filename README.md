# Ohjelmistotekniikka, harjoitustyö

Kurssin harjoitustyönä on **graaffisella käyttöliittymällä** varustettu *Tier list* sovellus.

## Dokumentaatio
* [Käyttöohje](/tier-list-app/dokumentaatio/kayttoohje.md)
* [Vaatimusmäärittely](/tier-list-app/dokumentaatio/vaatimusmaarittely.md)
* [Tuntikirjanpito](/tier-list-app/dokumentaatio/tuntikirjanpito.md)
* [Changelog](/tier-list-app/dokumentaatio/changelog.md)
* [Arkkitehtuurikuvaus](/tier-list-app/dokumentaatio/arkkitehtuuri.md)

## Python ja poetry versioista
Ohjelma testattu sekä fuksiläppärillä jossa Python 3.12.3 ja poetry 2.1.2,
että virtuaaliympäristössä jossa Python 3.10.12 ja poetry 2.1.2.

## Asennus

 <b>HUOM! Kaikki asennuksen komennot ajetaan tier-list-app hakemistossa.</b>

1. Siirry tier-list-app hakemistoon ja asenna riippuvuudet komennolla:

```bash
poetry install
```
2. :warning: Koskee viikon 5 deadline releasea. Asennus todennäköisesti tuottaa Pillowin kanssa virheen joka ei releaseen kerennyt. Suorita poetryn ehdottama komento joka korjaa ongelma.

```bash
poetry lock --no-cache --regenerate
```

3. Uudelleennimeä <b>.env.template .env</b> tiedostoksi ja <b>.env.test.template .env.test</b> tiedostoksi

4. Suorita alustavat toimenpiteet komennolla:

```bash
poetry run invoke build
```

5. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komentorivitoiminnot

 <b>HUOM! Kaikki komennot ajetaan tier-list-app hakemistossa.</b>

### Testaus

Testien suoritus:

```bash
poetry run invoke test
```

### Testikattavuus

Kattavuusraportin saa HTML muodossa komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu htmlcov-hakemistoon.

### Pylint

Pylint tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```
Tarkistukset suoritetaan [.pylintrc](tier-list-app/.pylintrc) määritelmien mukaisesti

<b>Ylimääräinen koodikatselmointi:</b>
https://github.com/antoKeinanen/ohjelmistotekniikka-harjoitus
