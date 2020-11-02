# NFLGameSimulator (beta)

## Overview
This program simulates an NFL game and generates a faux play-by-play as well as a final score.
</br>
To run:</br> 
  - Open Terminal/Command Line at folder with project files </br>
  - Type in *python SimEngine.py*</br>

## Modules

**Sim Engine:** 
Keeps track of time, ball placement, yards, team with possession, etc. Generates plays by calling methods from the PlayGen module.<br/>

**PlayGen:**
Contains the Pass, Rush, and PlayCaller classes.<br/>
Pass is used to generate a throw based on quarterback/opponent statistics.<br/>
Rush is used to generate a run based on offensive team tendencies as well as rusher/opponent statistics.<br/>
PlayCaller is used to generate a playcall ("throw"/"run") based on team tendencies. Sacks are determined here as well.<br/>

**Scraper:**
Gets player and team data and statistics from provided html files.<br/>

**Utility:**
Use to convert between naming schemes (Abbreviation <--> Full Team Name)<br/>

## Future Directions and Expected Changes
  Web-Scraper<br/>
  Post-Game Recap<br/>
  Special Teams Simulation<br/>
  More Advanced Play-by-Play<br/>
