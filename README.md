# Discord music bot **``MUZLAG``**
[![Lint](https://github.com/Drozd0f/muzlag/actions/workflows/linter.yml/badge.svg)](https://github.com/Drozd0f/muzlag/actions/workflows/linter.yml)
[![Deploy](https://github.com/Drozd0f/muzlag/actions/workflows/deploy.yml/badge.svg)](https://github.com/Drozd0f/muzlag/actions/workflows/deploy.yml)

## Fix youtube-dl
**``pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl``**

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
PREFIX=BOT_PREFIX
TOKEN=BOT_TOKEN
YT_QUERY_LEN=MAX_LEN_OF_TEXT_TO_QUERY_SEARCH_VIDEO_ON_YOUTUBE
SRCH_RES_LEN=MAX_LEN_OF_LIST_WITH_SEARCH_VIDEO_RESULT
ENV='dev'/'prod'
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

> **Note**
> Create log file for prod

```shell
make create-log-file
```

---
## Commands

|    Command    |                 Description                  |
|:-------------:|:--------------------------------------------:|
|     ?help     |        Shows all info about commands         |
|     ?ping     |                 Healthcheck                  |
|     ?play     |      Play song by link or add to queue       |
| ?skip [count] | Skip current song (default) or several songs |
|     ?stop     |           Stop all songs in queue            |
|    ?repeat    |             Repeat song in queue             |
|    ?queue     |               Show songs queue               |
