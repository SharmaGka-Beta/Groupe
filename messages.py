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

spades = [(m, ':spades:') for m in range (1, 14)]
hearts = [(m, ":hearts:") for m in range (1, 14)]
clubs = [(m, ':clubs:') for m in range (1, 14)]
diamonds = [(m, ':diamonds:') for m in range(1, 14)]

deck = spades + hearts + clubs + diamonds