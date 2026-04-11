def freq(arr):

    count = {}

    for i in arr:
        if i in count.keys():
            count[i] += 1
            continue
        count[i] = 1

    return count

def high(nums):
    return max(nums)

def pair(nums):

    count = freq(nums)

    pairs = []

    for i in count.items():
        if i[1] >= 2:
            pairs.append(i[0])
    
    return pairs        #returns a list of all possible pairs

def three(nums):

    count = freq(nums)
    threes = []
    for i in count.items():
        if i[1] >= 3:
            threes.append(i[0])
        
    return threes       #all possible threes


def straight(nums):
    
    s = []
    n = nums[:]

    if 1 in nums:
        n.append(14)

    for i in nums:
        if (((i+1) in n) and ((i+2) in n) and ((i+3) in n) and ((i+4) in n)):
            s.append(i)
        

    return list(set(s))     #returns a list of the starting values of all possible straights

def flush(suits, cards):

    count = freq(suits)
    f = []
    for i in count.items():
        if i[1] >= 5:
            f.append(i[0])

    if len(f) == 0:
        return []
    
    max = 0
    for i in cards:
        if i[1] == f[0] and i[0] > max:
            max = i[0]

    return [f[0], max]            #returns a list of suits of all flushes

def full_house(nums):

    pairs = pair(nums)
    threes = three(nums)
    fulls = []
    for i in threes:
        for j in pairs:
            if i != j:
                fulls.append((j, i))

    return fulls        #returns a list of (pair, three) for all full houses

def four(nums):
    count = freq(nums)
    fours = []
    for i in count.items():
        if i[1] == 4:
            fours.append(i[0])
    return fours        #returns all four of a kind
        

def straight_flush(cards, suits):

    fl = flush(suits, cards)
    if len(fl) == 0:
        return []
    
    temp = [m for m in cards if m[1] == fl[0]]
    
    n = [m[0] for m in temp]
    st = straight(n)
    return [st, fl[0]]      #only one sf possible. gives staring element and suite

def royal_flush(cards, suits):

    st = straight_flush(cards, suits)

    if len(st) == 0:
        return 0
    
    if 10 in st[0]:
        return 1
    return 0                #1 if royal flush 0 if not 
    

        
def best_hand(cards):

    nums = [m[0] for m in cards]
    suits = [m[1] for m in cards]

    best = ['high', high(nums)]

    temp = pair(nums)
    if len(temp) > 0:
        best = ['pair', max(temp)]

    if len(temp) > 1:
        a = max(temp)
        temp.remove(a)
        b = max(temp)
        best = ['two pair', (a, b)]

    temp = three(nums)
    if len(temp) > 0:
        best = ['three of a kind', max(temp)]

    temp = straight(nums)
    if len(temp) > 0:
        best = ['straight', max(temp)]

    temp = flush(suits, cards)
    if len(temp) > 0:
        best = ['flush', temp[1]]

    temp = full_house(nums)
    if len(temp) > 0:
        p = [m[0] for m in temp]
        t = [m[1] for m in temp]
        best = ['full house', (max(p), max(t))]
    
    temp = four(nums)
    if len(temp) > 0:
        best = ['quads', temp[0]]

    temp = straight_flush(cards, suits)
    if len(temp) > 0 and len(temp[0]) > 0:

        best = ['straight flush', (max(temp[0]), temp[1])]

    temp = royal_flush(cards, suits)
    if temp:
        best = ['ROYAL FLUSH']

    return best


