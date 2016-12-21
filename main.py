import enum
import random

class Card:
    def __init__(self, suit, number):
        self._suit = suit
        self._number = number
    def __repr__(self):
        return "%s%s" % (self._suit.name.lower()[0], self._number.name.upper()[0])

    @property
    def number(self):
        return self._number
    @property
    def suit(self):
        return self._suit

Suits = enum.Enum("Suits", "spade club heart diamond")
Numbers = enum.Enum("Numbers", "2 3 4 5 6 7 8 9 ten jack queen king ace")
Ranks = enum.Enum("Ranks", "hi_card one_pair two_pair three_of_a_kind straight flush full_house four_of_a_kind straight_flush")
deck = [Card(s,n) for n in Numbers for s in Suits]
random.shuffle(deck)

class Player:
    def __init__(self, name):
        self._name = name
        self._hand = None

    def deal(self, hand):
        self._hand = hand

    @property
    def hand(self):
        return self._hand

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "name:%s, hand:%s" % (self._name, self._hand)

def pick(deck, num):
    r = deck[:num]
    return r, deck[num:]

ps = [Player("A"),Player("B")]
#ps = [Player("A"),Player("B"),Player("C"),Player("D"),Player("E"),Player("F"),Player("G"),Player("H"),Player("I"),Player("J"),Player("K")]

# initial
# pre-flop
for p in ps:
    hand, deck = pick(deck, 2)
    p.deal(hand)

# betting time

# flop
pocket, deck = pick(deck, 3)
# betting time


# turn
c, deck = pick(deck, 1)
pocket.extend(c)
# betting time

# rever
c, deck = pick(deck, 1)
pocket.extend(c)

# betting time


# showdown
print("hand")
for p in ps: print(p)
print("pocket")
print(pocket)
def divide(cards, same):
    divide_lists = []
    for card in cards:
        predicate = lambda c: same(c, card)
        is_same = False
        for divide_list in divide_lists:
            if not any(map(predicate, divide_list)): continue
            is_same = True
            divide_list.append(card)
            break
        if is_same: continue
        new_list = []
        new_list.append(card)
        divide_lists.append(new_list);
    return divide_lists

def handsOf(cards):
    ret = None
    c = cards[:]
    c.sort(key=lambda o: o.suit.value + (o.number.value << 4))

    divide_by_suits = divide(c, lambda a,b: a.suit == b.suit)
    divide_by_number = divide(c, lambda a,b: a.number == b.number)
    over5_suits = [a for a in divide_by_suits if 5 <= len(a)]
    if len(over5_suits):
        ret = (Ranks.flush, (over5_suits[0][-1],))
    by_number_count = len(divide_by_number)
    if by_number_count == 7:
        ret = (Ranks.hi_card, (divide_by_number[-1][0],))
    elif by_number_count == 6:
        ret = (Ranks.one_pair, ([l for l in divide_by_number if len(l) == 2][0][0],))
    elif by_number_count == 5:
        if [l for l in divide_by_number if len(l) == 3]:
            ret = (Ranks.three_of_a_kind, ([l for l in divide_by_number if len(l) == 3][0][0],))
        else:
            tmp = [l for l in divide_by_number if len(l) == 2]
            ret = (Ranks.two_pair, (tmp[0][0], tmp[1][0]))
    elif by_number_count == 4:
        if [l for l in divide_by_number if len(l) == 4]:
            ret = (Ranks.four_of_a_kind, ([l for l in divide_by_number if len(l) == 4][0][0],))
        elif [l for l in divide_by_number if len(l) == 3]:
            tmp = [l for l in divide_by_number if len(l) == 3]
            tmp2 = [l for l in divide_by_number if len(l) == 2]
            ret = (Ranks.full_house, (tmp2[0][0], tmp[0][0]))
        else:
            tmp = [l for l in divide_by_number if len(l) == 2]
            ret = (Ranks.two_pair, (tmp[-2][0], tmp[-1][0]))
    elif by_number_count == 3:
        if [l for l in divide_by_number if len(l) == 4]:
            ret = (Ranks.four_of_a_kind, ([l for l in divide_by_number if len(l) == 4][0][0],))
        else:
            tmp = [l for l in divide_by_number if 2 <= len(l)]
            ret = (Ranks.full_house, (tmp[-2][0], tmp[-1][0]))
    tmp = isStraight(c)
    if tmp:
        hi = tmp[0][-1][-1]
        if ret[0] == Ranks.flush:
            ret = (Ranks.straight_flush, (hi,))
        elif ret is None or ret[0].value < Ranks.straight.value:
            ret = (Ranks.straight, (hi,))
    if not ret:
        raise
    return ret

def isStraight(cards):
    a = [z for z in [(x,y) for x, y in zip(cards, cards[1:])] if z[0].number.value+1==z[1].number.value]
    return [z for z in divide(a , lambda x,y: x[1] == y[0]) if 4 <= len(z)]

results = [(p,) + handsOf(p.hand + pocket) for p in ps]
for (player, rank, opt) in results: print("%s : %s[%s]" % (player, rank, opt))

def optToPoint(options):
    return sum([opt.number.value << (index*4) for index, opt in enumerate(options)])

def judge(results):
    r = [((rank.value << 8) + optToPoint(opt), player, rank, opt) for player, rank, opt in results[:]]
    r.sort(key=lambda a: a[0], reverse=True)
    return divide(r, lambda a, b: a[0] == b[0])

print("judge")
for a in judge(results): print(a)
