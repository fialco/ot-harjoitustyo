# Arkkitehtuurikuvaus

## Luokkakaavio

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
  UI->UI: show_tier_list_view(1)
```

Painikkeen painamisella ensin siirrytään tier_list_view sivulle. Sitten kutsutaan sovelluslogiikan `TierListService` eri metodeja parametrina tier listin id. Näillä kerätään `TierListRepository`:n avulla tier listin, sen eri esineiden/asioiden ja tierien dataa. Data käsitellään UI:lle sopivaan muotoon ja jäädään tier_list_view näkymään.