# Arkkitehtuurikuvaus

## Luokkakaavio

```mermaid
classDiagram
    class Item {
        name
        image_path
        tierlist_id
    }
    class TierList {
        id
        name
    }

    Item "*" --> "1" TierList
```