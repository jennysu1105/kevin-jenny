# Kevin ♥ Jenny Discord Bot

## Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Future Features](#future-features)

## General Info
This project is a Discord chat bot that can store information.
| Command | Name | Use | Description |
| :-----: | :--- | :--- | :--- |
| **help** | Help | /help \<type\> | Get information on commands | 
| c | Command Help | /help c | General Commands help | 
| mc | Minecraft Help | /help mc | Minecraft Commands help |
|  mem | Memory Help | /help mem | Memory Command help |
| **time** | Time | /time | How long have we been together? ~~*slightly inaccurate*~~| 
| **mc** | Minecraft Commands |
| time | MC time | /mc time | How long have has our server been alive? ~~*slightly inaccurate*~~ |
| spt | Save Point | /spt \<x y z\> \<name\> \[type\] | Save point x y z as name |
| vpt | View Point | /vpt \[type\] \[name\] | View list of points with name and/or type |
| **mem** | Memory Commands |  | *future feature: comment made using interaction user* | 
| memstore | Store memory | /memstore \<name\> \<type\> \<user\> \<address\> \[date\] \[details\] \[logo\] \[photo\] | Store memory to database |
| watchsave | Store watch | /watchsave \<name\> \<type\> \<user\> \[address\] \[date\] \[details\] \[cover\] \[photo\] | Store something we've watched together |
| viewmem | View Memories | /viewmem \[type\] \[id\] | View single memory and all details with id OR list of memories by type \(*future feature: by name*\)|
| watchlist | View Watches | /watchlist \[type\] \[id\] | View single watch and all details with id OR list of memories by type \(*future feature: by name*\)|
| updatemem | Update Memory or Watch | /updatemem \<id\> \<user\> \[name\] \[date\] \[details\] \[address\] \[type\] \[logo\] \[photo\] | Change information from memories |

* \< required \> , \[ optional/lateral \]

## Technologies
| Module | Version | Use |
| :------ | :-------: | :--- |
| Python | 3.10.5 | 
| python-dotenv | 1.0.1 | Evironment Variables |
| Flask | 3.1.0 | Local Server |
| discord.py | 2.4.0 | Library |
| python-dateutil | 2.9.0.post0 | Library: Date/Time |
| typing | 3.7.4.3 | Library: Optional/Literal inputs |
| pillow | 11.0.0 | *not used yet* Library: Image processing |
| pytz | 2025.1 | Library: Timezones |
| geopy | 2.4.1 | Library: Location Search |

## Setup
1. Create new application at https://discord.com/developers/applications
2. Find bot token in Bot tab
3. Create .env file in main folder
```TOKEN= insert token here ...```
4. Run program with main.py

Download packages with python -m pip install -U, sometimes python3.9 -m pip install

## Future Features
| Feature | Description |
| :-----: | :--|
| filter by name | being able to filter memories and watchlist by name |
| ~~time accuracy~~ | ~~make time commands more accurate~~ | 
| comment using interaction user | use discord interaction to check who comments using details |
| bot on server | currently running locally. One day, set up server for it | 
| add art commands | show and store art made during the relationship |
| save images to local | save in case discord becomes weird |
| ~~modularize memory database~~ | ~~separate address and logos~~ |
