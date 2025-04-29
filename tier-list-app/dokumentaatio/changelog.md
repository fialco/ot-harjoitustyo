## Viikko 3
Viikolla keskitytty käyttöliittymän rakentamiseen ja kuvien lisäämiseen.

- Käyttäjä pystyy lisäämään tier listiin yksittäisesti kuvia drag and droppina
- Käyttäjä pystyy liikuttamaan kuvia hiirellä ja asettamaan niitä tiereille
- Lisätty ImageItem-luokka joka vastaa yksittäisestä lisätystä elementistä
- Lisätty ImageRepository-luokka vastaa kuvan lataamisesta
- Lisätty ItemService-luokka vastaa elementtien rakentamisesta ja liikuttamisesta
- Lisätty UI-luokka joka vastaa käyttöliittymän toiminnasta

## Viikko 4

- Lisätty tuki tietokannasta luvulle
- Käyttäjä pystyy valitsemaan kahdesta valmiista tier lististä ja käyttämään niitä
- Lisätty ListView-luokka joka vastaa käyttöliittymän tier listien listauksesta
- Lisätty TierListService-luokka joka vastaa sovelluslogiikasta
- Lisätty TierListRepository-luokka joka vastaa tietokantaoperaatioista
- Siiretty ImageItem- ja ItemService käyttöliittymän alle

## Viikko 5

- Lisätty alustava tuki tier list pohjien tekemiseen ja tallentamiseen
- Lisätty tiereille oma tietokantataulukko ja entity
    - Tällä hetkellä vielä omiin pohjiin default tierit
- Laajennettu kuvien lisäämistä tier listiin
    - Jos kuva alunperin jossain muualla kuin /data/images/ hakemistossa
    siitä tallennetaan pienennetty kopio /data/images/ hakemistoon
    - Tietokantaan tallennetaan vain suhteellinen /data/images/kuva.jpg polku kuviin
    - Kuvia voi vetää pudotuslaatikkoon useamman (vielä korkeintaan 5) kerralla

## Viikko 6

- Mahdollisuus tier listien poistoon tietokannasta käyttöliittymän kautta
- Tierien nimet voi itse määrittää
- Poistettu suora viittaus repositorioon käyttöliittymästä. Riippuvuus nyt vain serviceen.