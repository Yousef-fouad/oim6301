
# TV Show Catalog ERD

```mermaid
erDiagram
    ACTOR {
        int ActorID PK
    }
    SHOWS {
        int ShowID PK
    }
    WRITERS {
        int WriterID PK
    }
    GENRE {
        int GenreID PK
    }
    SHOW_ACTOR {
        int ShowID PK,FK
        int ActorID PK,FK
    }
    SHOW_WRITERS {
        int ShowID PK,FK
        int WriterID PK,FK
    }
    SHOW_GENRES {
        int ShowID PK,FK
        int GenreID PK,FK
    }

    ACTOR ||--o{ SHOW_ACTOR : appears_in
    SHOWS ||--o{ SHOW_ACTOR : has
    SHOWS ||--o{ SHOW_WRITERS : has
    WRITERS ||--o{ SHOW_WRITERS : writes
    SHOWS ||--o{ SHOW_GENRES : has
    GENRE ||--o{ SHOW_GENRES : categorizes
```
