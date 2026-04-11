workp = ["Normal day at work.", 
         "Manager made you work overtime.", 
         "Your manager sent a 'quick update' at leaving time. You didn't go home that night.", 
         "It was a coworker's birthday. You didn't get any work done.", 
         "It was take your children to work day. If only you had a partner...",
         "PRETZEL DAY!!!",
         "You sent in a sick leave. Your manager approved it!!", 
         "There are rumours of downsizing. You hope it's not you. Actually you hope it is you.",
         "It was Funday-Friday. The HR made you play team- building 'games'.",
         "The SQL query to update 2 lines ran for 20 minutes.",
         "Your coworker thanked you for solving his merge conflict. Scumbag."]

workn = ["Your car broke down on the way to work. Manager yelled at you for being late.",
         "You were stopped by the mob on your way to work.",
         "The police searched your car for drugs while you were returning. Corrupt pieces of shits",
         "You forgot your wallet in the car and a rogue stole it."]

items_gun = [   ("Pistol", "50000", "A basic handgun", "ammunitions", "🔫 ", "6"),
                # ("SMG", "75000", "Machine gun but smol", "ammunitions", " ", "2"),
                ("Shotgun", "100000", "Beast at close range", "ammunitions", " ", "2"),
                ("AR", "150000", "Fully automatic rifle", "ammunitions", " ", "3"),
                ("MachineGun", "175000", "Sprays bullets fast", "ammunitions", "🔱 ", "2"),
                ("Sniper", "200000", "One shot, one kill", "ammunitions", "🎯 ", "1")
            ]
items_drugs =  [("Weed", "10000", "Mild and cheap", "drugs", "🌿 "),
                ("LSD", "50000", "Trippy", "drugs", "🔵 "),
                ("Cocaine", "75000", "The classic", "drugs", "⚪ "),
                ("BlueMeth", "100000", "Say my name", "drugs", "🥶 "),
                ("Heroin", "150000", "Dangerous stuff", "drugs", "💉 "),
                ]

items_items = []

hit_targets = ["Joaquin Salamanca", "Ed Truck", "Charles McGill", "Negan Smith", "Becca Butcher", 
            "Susan Duffy", "Imran Ansari", "Ann Perkins", "Veronica Duncan", "Meera Eston"]

rob_targets = ["Chaudhary Baldev Singh", "Gil Thorpe", "Tammy Swanson", "Jack Dawson", "Bert Kibbler",
               "Melvina Whitaker", "Dawn Lerner", "Luke Cooper", "Paige Novick", "Carmen Molina"]

extort_targets = ["Stuart Bloom - Comic Shop", "Kevin Malone - Bar", "Bogdan Wolynetz - Car Wash", "Ernesto - Street Vendor",
                  "Manuel Varga - Furniture Repair Store", "Tom Haverford - Bistro", "George Weasley - Magic Shop"]

patrol_targets = [("Brother Sam", 1), ("El Sapo", 1), ("Isaak Sirko", 1), ("Oliver Saxon", 2), ("James Doakes", 2), ("Freebo", 2),
                  ("Lumen Pierce", 3), ("The Skinner", 3), ("The Brain Surgeon", 4), ("IceTruck Killer", 4), ("The Bay Harbor Butcher", 5)]

items = items_gun + items_drugs + items_items

spades = [[m, ':spades:'] for m in range (1, 14)]
hearts = [[m, ":hearts:"] for m in range (1, 14)]
clubs = [[m, ':clubs:'] for m in range (1, 14)]
diamonds = [[m, ':diamonds:'] for m in range(1, 14)]

deck = spades + hearts + clubs + diamonds


special_cards = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}

cop_messages_positive = [
    "Alright, move along. Don't let me see you here again.",
    "You didn't hear this from me, but get out of here. Now.",
    "I'm going to pretend I didn't see that. You owe me one.",
    "Get out of my sight before I change my mind.",
    "Consider this your lucky day. Don't waste it.",
    "I've got kids too. Go home.",
    "Next time I won't be so understanding. Move.",
    "You've got two minutes to be gone. I'm not looking.",
    "Don't make me regret this.",
]

cop_messages_negative = [
    "Hands where I can see them. You're coming with me.",
    "Save it. I've heard every story in the book.",
    "Turn around. Slowly.",
    "Wrong place, wrong time, wrong answer.",
    "You just made this a lot worse for yourself.",
    "Keep talking. I dare you.",
    "I've had a long night and you just made it longer.",
    "That's enough. On the ground.",
    "You have the right to remain silent. I suggest you use it.",
    "Call it in — yeah, I've got one here.",
]

charity_messages = [
    "Donate to a homeless shelter downtown?",
    "Drop cash into a street musician's case?",
    "Fund a kid's school supplies for the year?",
    "Pay for a stranger's groceries at checkout?",
    "Donate to the local food bank?",
    "Sponsor a stray dog's adoption fee at the shelter?",
    "Leave a fat tip for the overworked diner waitress?",
    "Bring meals for the guys sleeping under the bridge?",
    "Cover someone's hospital bill?",
    "Cover the costs of a small local church's roof repairs?",
]

volunteer_messages = [
    "Volunteer Symphony?",
    "Help an old lady carry her groceries home?",
    "Spend a day serving food at a homeless shelter downtown?",
    "Volunteer Synergy?",
    "Assist at a local blood drive?",
    "Volunteer Spandan?",
    "Volunteer Confluence?",
    "Help an elderly man fix his fence?",
    "Spend a day mentoring at-risk youth?",
    "Volunteer Infini8?",
]

slots_weights =  [3, 5, 8, 10, 11, 12, 20]
slots_symbols = ['💎', '👑', '⭐', '🍒', '💵', '🔫', '💊']
slots_payouts = {"💊": 2, "🔫": 3, "💵": 5,  "🍒": 10,  "⭐": 15, "👑": 20, "💎": 25}

role_colors = {
    "civilian":  0x3498db,  # blue
    "associate": 0xf1c40f,  # yellow
    "underboss": 0xe67e22,  # orange
    "godfather": 0xed4245,  # brand red
    "rookie": 0x008000,
    "detective": 0x228B22,
    "chief": 0x2E8B57
}

hit_chance = {"pistol": 1, "shotgun": 2, "ar": 3, "machinegun": 4, "sniper": 5}

promotion_req = {"associate": ("underboss", 50),
                 "underboss": ("godfather", 75),
                 "rookie": ("detective", 50),
                 "detective": ("chief", 75)}

mob_welcome_messages = [
    "You're one of us now. God help you.",
    "Welcome to the family. Don't make us regret it.",
    "From this moment, you bleed for us. And we bleed for you.",
    "You're made. Don't waste it.",
    "The city just got a little more dangerous. Good.",
    "You just signed your soul away. Spend it wisely.",
    "The boss has spoken. You're in. Don't make him speak again.",
    "Welcome to Sin City, associate. Try to stay alive.",
    "You're family now. Family doesn't get to quit.",
]

police_welcome_messages = [
    "Badge is yours. Don't make me take it back.",
    "Welcome to the force. Watch your back.",
    "You're a cop now. The city will never look the same.",
    "Sworn in. Good luck. You'll need it.",
    "The precinct has a new face. Let's hope it lasts.",
    "You're one of the good guys now. Whatever that means in this city.",
    "Welcome aboard. Try not to end up on the wrong side of your own handcuffs.",
    "The badge is heavy. You'll feel it more every day.",
    "You're in. Just remember — in this city, everyone has an angle. Even us.",
    "Congratulations officer. The criminals already know your name.",
]
   

help_commands={
    "⚙️General commands":[
        {
            "name":"profile",
            "format":"sin profile <member>(takes default member as sender)",
            "description":"View your profile or another players stats."
        },
        {
            "name":"inventory",
            "format":"sin inventory",
            "description":"View your inventory."
        },
        {
            "name":"shop",
            "format":"sin shop",
            "description":"Opens the shop to buy gins,drugs and items."
        },
        {
            "name":"buy",
            "format":"sin buy <item> <quantity>",
            "description":"Buy items from the shop(default quantity=1"
        },
        {
            "name": "sell",
            "format":"sin sell <item> <quantity>",
            "description": "Sell items from your inventory for coins"
        },
        {
            "name": "leaderboard",
            "format": "sin leaderboard",
            "description": "View leaderboards (coins, wanted, integrity, black money)"
        },
        {
            "name": "transfer",
            "format": "sin transfer <amount> <member>",
            "description": "Send coins to another player"
        },
    ],
    "👤Civilian":[
        {
            "name":"work",
            "format":"sin work",
            "description":"Work a job to earn coins(not always)." 
        },
        {
            "name":"charity",
            "format":"sin charity",
            "description":"Donate coins to earn integrity and reduce wanted level."
        },
        {
            "name":"hit",
            "format":"sin hit",
            "description":"Take a hit to eliminate a target."
        },
        {
            "name":"volunteer",
            "format":"sin volunteer",
            "description":"Volunteer to increase integrity and reduce wanted level."
        },
        {
            "name":"rob",
            "format":"sin rob",
            "description":"Attempt to rob a target for money."
        },
        {
            "name":"mob",
            "format":"sin mob",
            "description":"Attempt to join mob(requires weapon,high wanted level and low integrity)."
        }
    ],
    "👾Mob":[
        {
            "name":"extort",
            "format":"sin extort",
            "description":"Extort money from target."
        },
        {
            "name":"deal",
            "format":"sin deal",
            "description":"Deal illegal drugs for money."
        },
        {
            "name":"promote",
            "format":"sin promote",
            "description":"Attempt to promote at higher rank in the mob."
        }
    ],
    "🎰Gambling":[
        {
            "name":"roulette",
            "format":"sin roulette <amount> <red/balck/number>",
            "description":"Bet coins on a colour or number(1-36)."
        },
        {
            "name":"blackjack",
            "format":"sin blackjack <amount>",
            "description":"Play blackjack against the dealer using hit/stand."
        },
        {
            "name":"slots",
            "format":"sin slots <amount>",
            "description":"Spin the slot machine to get a chance to win big."
        }
    ]
}
