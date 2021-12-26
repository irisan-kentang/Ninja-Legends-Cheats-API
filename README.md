# Ninja Legends Cheats API

API for Ninja Legends Cheats.

## Requirements
* Docker
* Docker Compose
* Git

## Getting Started
* Clone this repo
* `docker-compose build`
* `docker-compose --compatibility up -d`

## API Docs
### Instant Mission
- Endpoint : `/instant_mission` <br>
- HTTP Method : `POST` <br>
- Request Header :
    - Accept : `application/json`
    - Content-type : `application/json`
- Request Body : 
```json
{
  "username": "",
  "password": "",
  "profile_id": "",
  "mission_id": 1
}
```
### Hunting House
- Endpoint : `/hunting_house` <br>
- HTTP Method : `POST` <br>
- Request Header :
    - Accept : `application/json`
    - Content-type : `application/json`
- Request Body : 
```json
{
  "username": "",
  "password": "",
  "profile_id": "",
  "boss_num": 0
}
```

## Cheat List
* Instant Mission (ATM Exp)
* Instant Hunting House

## Changelog
### [0.0.1]
* Add instant mission
### [0.0.2]
* Add hunting house
* Fix hash param
### [0.0.3] - 26/12/2021
* Fix total damage and session key param

## Authors
Irisan-Kentang