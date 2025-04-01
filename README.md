# Stardew Valley Save Checker
---

# Table of Contents
1. [Description](#description)
2. [Code Prerequisites](#code-prerequisites)
3. [Save File Breakdown](#save-file-breakdown)


## Description
***This is still a work-in-progress and may contain bugs.***\
This is a program designed to check the progress of a given save file for the game, Stardew Valley. It is designed to work with save files in all game versions from 1.5 to the most recent. It is written in Python so it is not the fastest program. See [Code Prerequisites](#code-prerequisites) for required Python packages and other dependencies.
## Code Prerequisites
- **xmltodict** v0.4.3\
[https://pypi.org/project/xmltodict/0.4.3/]\
`pip install xmltodict==0.4.3`
## Save File Breakdown
Stardew Valley utilizes XML files to store player data. Each game save is split into two files:
1. SaveGameInfo
2. [FarmerName]_[FarmSeed] *(i.e: Farmer_1234567890)*

There are also two additional files in each *vanilla* save that are named nearly identically. The only difference is that they end in `_old`. Some saves may or may not contain these. The checker will not interact with these in any way.

Here's the breakdown of each individual file.

### SaveGameInfo
