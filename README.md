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
## Commands

|    Command    |                  Description                 |
|:-------------:|:--------------------------------------------:|
|     ?help     |         Shows all info about commands        |
|     ?ping     |                  Healthcheck                 |
|     ?play     |       Play song by link or add to queue      |
| ?skip [count] | Skip current song (default) or several songs |
|     ?stop     |            Stop all songs in queue           |
