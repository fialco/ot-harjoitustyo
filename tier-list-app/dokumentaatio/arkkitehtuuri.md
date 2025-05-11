# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne noudattelee referenssisovelluksen mukaista rakennetta eli kolmitasoista kerrosarkkitehtuuria. Koodin pakkausrakenne on seuraava:

![Pakkausrakenne](./kuvat/dokumentaatio-pakkauskaavio.png)

Pakkaus _ui_ sisältää käyttöliittymästä ja _services_ sovelluslogiikasta vastaavan koodin. _repositories_ sisältää koodin sekä tietojen pysyväistallennukselle, että kuvien polku- ja latausoperaatioille. Pakkaus _entities_ sisältää luokat, jotka kuvaavat sovelluksen käyttämiä tietokohteita.

## Käyttöliittymä

Käyttöliittymä sisältää kolme eri näkymää:

- Lista eri tier listeistä
- Uuden tier list pohjan teko
- Valmiin tier list pohjan käyttö

Listanäkymä on omassa luokassaan, mutta uusi ja vanha tier list pohja jakaa saman luokan. Näkymät ovat aina yksi kerrallaan näkyvissä ja näiden näyttämisestä vastaa [UI](../src/ui/ui.py)-luokka. Kuten pakkausrakenteeseen on kuvattu, käyttöliittymä on eritytetty kutsumaan vain [TierListService](../src/services/tier_list_service.py)-luokan metodeja.

## Sovelluslogiikka

 Luokat [TierList](../src/entities/tier_list.py), [Item](../src/entities/item.py) ja [Tier](../src/entities/tier.py) muodostavat sovelluksen loogisen tietomallin. Nämä kuvaavat tier listejä, tier listattavia asioita ja tier listin tasoja.

```mermaid
classDiagram
    class Item {
        tierlist_id
        image_path
    }
    class Tier {
        tierlist_id
        name
        rank
    }
    class TierList {
        name
        id
    }

    Item "*" --> "1" TierList
    Tier "*" --> "1" TierList
```

[TierListService](../src/services/tier_list_service.py) luokan yksi olio toimii linkkinä käyttöliittymän ja muiden osien välillä. Luokka antaa kaikille käyttöliittymän oleellisille toiminnoille oman metodin, joita on esimerkiksi:

- `get_tier_lists()`
- `get_tier_list(tierlist_id)`
- `create_tier_list_template(name, tier_data, image_paths)`
- `delete_tier_list(tierlist_id)`

_TierListService_ pääsee käsiksi tier listeihin, niistä riippuviin tietoihin (items, tiers) sekä kuviin _repositories_-hakemistossa sijaitsevien luokkien [TierListRepository](../src/repositories/tier_list_repository.py) ja [ImageRepository](../src/repositories/image_repository.py) kautta.

Ohjelman luokka/pakkauskaavio:

![Pakkausrakenne ja luokat](./kuvat/arkkitehtuuri-pakkaus-luokat.png)

## Tietojen pysyväistallennus

Pakkauksen _repositories_ luokka `TierListRepository` huolehtii tietojen tallettamisesta. Tiedot tallennetaan SQLite-tietokantaan.

Tallennustapa on halutessaan mahdollista vaihtaa Repository-suunnittelumallin ansiosta.

Vastaavasti pakkauksen _repositories_ luokka `ImageRepository` huolehtii tarvittaessa kuvien tallennuksesta [images](../data/images/)-hakemistoon.

### Tiedostot

Sovellus tallentaa tier list, item ja tier tiedot samaan SQLite-tietokanta tiedostoon.

Sovelluksen juureen sijoitettu [konfiguraatiotiedosto](./kayttoohje.md#konfigurointi) [.env](../.env) määrittelee tiedoston nimen.

Tier listit tallennetaan tauluun `tierlists`, itemit tauluun `items` ja tierit tauluun `tiers`. Nämä alustetaan [initialize_database.py](../src/initialize_database.py)-tiedostossa.

### Kuvat

Tier listissä käytettävät itemit hyödyntävät kuvia itemien esittämiseen. Kuvien käsittelyssä hyödynnetään [Pillow](https://github.com/python-pillow/Pillow/?tab=readme-ov-file) kirjastoa.

Uutta tier list pohjaa tehdessä kuvia voi ladata käyttöön mistä hakemistosta tahansa. Pohjan tallennusvaiheessa kuitenkin tarkastetaan onko kuva [images](../data/images/)-hakemistossa. Jos näin ei ole, niin 200x200 kopio tallennetaan kyseiseen hakemistoon ja tämä polku tallennetaan itemille tietokantaan.

## Päätoiminnallisuudet

Sekvenssikaavioita oleellisista toiminnallisuuksista.

### Valmiin tier listin valitseminen

Kun sovelluksessa on listattuna valmis tier list 'Programming Languages' jonka id on 1 ja käyttäjä klikkaa listin *choose* nappia tapahtuu seuraavaa:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant TierListService
  participant TierListRepository
  participant ImageRepository
  User->>UI: click "choose" button
  UI->UI: show_tier_list_view(1)
  UI->>TierListService: get_tier_list(1)
  TierListService->>TierListRepository: find_tier_list(1)
  TierListRepository-->>TierListService: tier_list
  TierListService-->>UI: tier_list
  UI->>TierListService: get_tiers_of_tier_list(1)
  TierListService->>TierListRepository: find_tiers_by_tier_list(1)
  TierListRepository-->>TierListService: tier_data
  TierListService-->>UI: tier_data
  UI->>TierListService: get_items_of_tier_list(1)
  TierListService->>TierListRepository: find_items_by_tier_list(1)
  TierListRepository-->>TierListService: items
  TierListService-->>UI: items
  UI->>TierListService: get_base_dir_path()
  TierListService->>ImageRepository: get_base_dir_path()
  ImageRepository-->>TierListService: base_dir
  TierListService-->>UI: base_dir
  loop for i, item in enumerate(items)
    UI->>TierListService: get_image(image_path)
    TierListService->>ImageRepository: get_image(image_path)
    ImageRepository-->>TierListService: photo_image
    TierListService-->>UI: photo_image
  end
  UI->UI: show_tier_list_view(1)
```

Painikkeen painamisella ensin siirrytään tier_list_view sivulle. Sitten kutsutaan sovelluslogiikan `TierListService` eri metodeja parametrina tier listin id. Näillä kerätään `TierListRepository`:n avulla tier listin, sen eri esineiden/asioiden ja tierien dataa. Kaavion loppupuolella loopataan kutsuja ladata `ImageRepository`:n avulla kuvia itemien määrän verran i.
Data käsitellään UI:lle sopivaan muotoon ja jäädään tier_list_view näkymään.

Kun listanäkymässä klikataan nappia 'New template' siirrytään myös tier_list_view sivulle ilman annettua id:tä. Käyttäjältä kysytään monta tieriä halutaan tier listille tehdä. Mitään UI:n ulkopuolisia kutsuja ei tehdä ja jäädää tier_list_view näkymään.

### Tier listin tallennus tietokantaan

Käyttäjä on 'New templaten' kautta valmistellut uutta pohjaa ja kokee että pohja on valmis. Kun hän painaa 'create'-nappia tapahtuu seuraavaa:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant TierListService
  participant TierListRepository
  participant ImageRepository
  User->>UI: click "create" button
  UI->>TierListService: create_tier_list_template('TV-shows', {0: 'Good', 1: 'Bad'}, ['/home/user/house.png', '/home/user/csi.png'])
  TierListService->>TierListRepository: create_tier_list(tier_list)
  TierListRepository-->>TierListService: tier_list
  TierListService->>ImageRepository: check_image_paths(['/home/user/house.png', '/home/user/csi.png'])
  ImageRepository-->>TierListService: ['../data/images/house.png', '../data/images/csi.png']
  TierListService->>TierListRepository: create_items(items)
  TierListRepository-->>TierListService: items
  TierListService->>TierListRepository: create_tiers(tiers)
  TierListRepository-->>TierListService: tiers
  TierListService-->>UI: -

  UI->UI: show_list_view()
```

Painikkeen painamisella kutsutaan create_tier_list_template() metodia argumentteina tier listin nimi, tier listin tasot ja esineet/asiat. Sitten kutsutaan `TierListRepositoryn` metodeja joilla tallennetaan tier list, asiat ja tasot tietokantaan. Välissä kuitenkin kuvien polut [tarkistetaan](arkkitehtuuri.md#Kuvat).

Lopulta siirrytään takaisin käyttöliittymässä listanäkymään.

### Tier listin poisto

Käyttäjä päättää poistaa tierlistin jonka id on 1 painamalla punaista X-nappia ja poiston varmistus pop-upissa painaa Yes. Tapahtuu seuraavaa:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant TierListService
  participant TierListRepository
  User->>UI: click "X" button
  UI->UI: messagebox.askyesno()
  User->>UI: click "Yes" button

  UI->>TierListService: delete_tier_list(1)
  TierListService->>TierListRepository: delete_tier_list(1)
  TierListRepository-->>TierListService: -
  TierListService-->>UI: -
  UI->UI: _draw_items()
```

Painikkeiden painamisella kutsutaan delete_tier_list() metodia argumentteina tier listin id. Sitten kutsutaan `TierListRepositoryn` metodia joilla poistetaan samalla tier list ja siihen liittyvät asiat ja tasot tietokannasta. Lopulta UI piirtää listanäkymän elementit uudestaan ilman poistettua tier listiä.