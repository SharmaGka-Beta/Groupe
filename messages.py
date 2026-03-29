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
                ("AR", "150000", "Fully automatic rifle", "ammunitions", " ", "4"),
                ("MachineGun", "175000", "Sprays bullets fast", "ammunitions", "🔱 ", "3"),
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

rob_targets = ["Chaudhary Baldev Singh", "Gil Thorpe", "Tammy Swanson", "Jack Dawson", "Stuart Bloom",
               "Melvina Whitaker", "Dawn Lerner", "Luke Cooper", "Paige Novick", "Carmen Molina"]

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