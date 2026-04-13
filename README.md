# 👾 Groupe - A Sin City themed Discord RPG bot

- A feature-rich Discord RPG bot developed by Groupe set in the criminal underworld of Sin City.
- Featuring economy, battles, factions and interactive UI.
- Players start as civilians and work their way up through the mob or police force, committing crimes, laundering money, gambling, and battling enemies along the way.
- https://youtu.be/AnqOsN6KLx8 (Click this link to see the youtube demo of our bot)

## 🚀 Features

- ### ⚔️ Battle System
   - Turn-based combat with weapons, damage, and healing

- ### 💰 Economy System
   - Economy system with regular and black money
   - Earn coins through various role-specific and general commands (and gambling too!)

- ### 👤 Faction/Role Progression System
   - Civilian
   - Mob (Associate -> Underboss -> Godfather)
   - Police (Rookie -> Detective -> Chief)
   - Role progression based on Levels/XP

   ### 📈 Level/XP System
   - Climb the role ladder by gaining XP and increasing levels
   - Users earn XP on role specific and general commands

   ### 📊 Leaderboard
   - See the best players globally
   - Sort based on coins/levels/black money

- ### 🎰 Gambling Games
   - Roulette
   - Blackjack
   - Poker
   - Slots

- ### 🧪 Inventory System
   - Guns
   - Drugs
   - Items

- ### 🎮 Interactive UI
   - Buttons
   - Modals
   - Dynamic embeds

- ### 🚔 Crime & Law System
   - Jail mechanics
   - Income tax raids
   - Wanted system
   - Integrity level

## 🛠️ Tech Stack
   - Python
   - discord.py
   - SQLite

## 🏛 Project Structure
   - ```main.py``` — entry point
   - ```functions.py``` — core commands and bot setup
   - ```database.py``` — SQLite database layer
   - **Roles**/
      - ```civilian.py``` — civilian role commands
      - ```mob.py``` — mob role commands
      - ```police.py``` — police role commands
   - **Gambling**/
      - ```gambling.py``` — gambling commands
      - ```poker.py``` - poker system
      - ```best_hand.py ``` - poker.py helper file
   - ```battle.py``` — battle system
   - ```events.py``` — random event logic
   - ```messages.py``` — static data and flavor text

## 🔑 Setup
   - ### Locally on your system
      - Create new appliction in discord developer portal
      - Give bot required permission(Administrator recommended)
      - Turn on Server Member Intent and Message Content Intent
      - Copy your bot token
      - Go to OAuth2 and give bot scope and bot permission
      - Copy the generated URL and add bot to your server

      - Clone the github repository
        ```bash
        git clone https://github.com/SharmaGka-Beta/Groupe.git
        cd Groupe
        ```

      - Make the virtual env and install the requirements 
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
      - Make a .env file and paste your bot token as DISCORD_TOKEN = your_token_here 
      - Run main.py from inside main directory

   - ### If bot is hosted
      - Go to following link and add bot to your server
      [Invite Link](https://discord.com/oauth2/authorize?client_id=1482734885230870701&permissions=8&integration_type=0&scope=bot)
      - Keep in mind the bot may not be online for this to work. In that case you will have to add the bot locally on your system 

## 📌 Future Improvements
   - Multiplayer battles
   - Add items
   - Image based gambling
   - Improvements to jail system

## Contributors
   - Naman Sharma
   - Pratyush Prasad
   - Krtin Singhvi 


    







