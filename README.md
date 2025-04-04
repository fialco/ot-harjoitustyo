# Ohjelmistotekniikka, harjoitustyö

Kurssin harjoitustyönä on **graaffisella käyttöliittymällä** varustettu *Tier list* sovellus.

## Dokumentaatio
* [Vaatimusmäärittely](/tier-list-app/dokumentaatio/vaatimusmaarittely.md)
* [Tuntikirjanpito](/tier-list-app/dokumentaatio/tuntikirjanpito.md)
* [Changelog](/tier-list-app/dokumentaatio/changelog.md)

## Python ja poetry versioista
Ohjelma testattu sekä fuksiläppärillä jossa Python 3.12.3 ja poetry 2.1.2,
että virtuaaliympäristössä jossa Python 3.10.12 ja poetry 2.1.2.

## Asennus

1. Siirry tier-list-app hakemistoon ja asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komentorivitoiminnot

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
