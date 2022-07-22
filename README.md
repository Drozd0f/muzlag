# Discord bot **``MUZLAG``**
[![Lint](https://github.com/Drozd0f/muzlag/actions/workflows/linter.yml/badge.svg)](https://github.com/Drozd0f/muzlag/actions/workflows/linter.yml)

## Practice project
> **Note**
> Dependencies
* Docker
* docker-compose
* Make
* ffmpeg

### Quick start
> **Note**
> First of all create .env file with next variables
```
TOKEN=BOT_TOKEN
```

---

**Run**
```shell
make
```

---

Remove containers
```shell
make rm
```

---

To display muzlag logs
```shell
make log
```

---
## Category commands

### Main commands

|    Command    |                  Description                 |
|:-------------:|:--------------------------------------------:|
|     ?help     |         Shows all info about command         |
|     ?ping     |                  Healthcheck                 |
|     ?play     |       Play song by link or add to queue      |
| ?skip [count] | Skip current song (default) or several songs |
|     ?stop     |            Stop all songs in queue           |

### Easter eggs commands

| Command |    Description   |
|:-------:|:----------------:|
| ?danilo | Play Danilo song |
| ?nikita | Play Nikita song |
| ?vadick | Play Vadick song |
| ?vadoom | Play Vadoom song |
|  ?vovan |  Play Vovan song |
