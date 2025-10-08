import random

keep = [0,0,0,0,0]  # 0 = don't keep; 1 = keep
dices = [0,0,0,0,0]
score = [["Aces",0, True], ["Twos",0, True], ["Threes",0, True], ["Fours",0, True], ["Fives",0, True], ["Sixes",0, True],["Bonus",0,True], ["Three of a Kind",0, True], ["Four of a Kind",0, True], ["Full House",0, True], ["Small Straight",0, True], ["Large Straight",0, True], ["Yahtzee",0, True], ["Chance",0, True],["Yathzee Bonus",0, True]]
available_rerolls = 3


def rolling():
    global dices
    for i in range(5):
        if keep[i] == 0:
            dices[i] = random.randint(1,6)
    return dices

def set_keep():
    global available_rerolls
    if available_rerolls > 0:
        k = list((input("What to keep? ")))
        if k == []: 
                return "assign score"
        try:
            for i in range(5):
                if len(k) == 5 and (int(k[i]) == 0 or int(k[i]) == 1):
                    keep[i] = int(k[i])
                else:
                    print("Not a valid sequence")
                    return set_keep()
            
        except: 
                print("Not a valid sequence")
                return set_keep()
        available_rerolls += -1
        return keep
    else:
        return "assign score"

def assign_score():
    try:
        k = int(input("Where to score: "))
    except:
        print("please insert a number")
        return assign_score()
    if yathzee() == 50 and score[12][1] == False:
        score[14][1] += 100
        score[14][2] = False
    try:
        if (score[k-1][2] and 1 <= k <= 6) or (score[k][2] and 7 <= k <= 13):
            if 1 <= k <= 6 :
                score[k-1][1] = k*dices.count(k)
                score[k-1][2] = False

            elif k == 7 or k == 8:
                score[k][1] = x_of_a_kind(k-4) #3 or 4 of a kind
                score[k][2] = False

            elif k == 9:
                score[k][1] = house()
                score[k][2] = False
            
            elif k == 10 or k == 11:
                score[k][1] = x_straight(k-6)
                score[k][2] = False

            elif k == 12:
                score[k][1] = yathzee()
                score[k][2] = False

            elif k == 13:
                score[k][1] = sum(dices)
                score[k][2] = False

            else:
                print("Not a valid spot")
                return assign_score()
            
            if sum([points[1] for points in score[:6]]) >= 63:
                score[6][1] = 35
                score[6][2] = False

        else: 
            print("Already used!")
            return assign_score()

    except:
        print("Not a valid spot")
        return assign_score()

def x_of_a_kind(x):
    for i in range(6):
        if dices.count(i+1) >= x:
            return (sum(dices))
        
    return(0)

def house():
    for i in range(6):
        if dices.count(i+1) == 3 and [number for number in dices if number != i+1][0] == [number for number in dices if number != i+1][1]:
            return(25)
    if not score[12][2] and dices.count(dices[0]) == 5 and not score[dices[0]-1][2]:
        return(25)
    return(0)

def x_straight(x):
    lenght = 1
    for i in sorted(set(dices)):
        if i+1 in dices: 
            lenght += 1
        elif i+1 not in dices and lenght < x:
            lenght = 1
        elif lenght >= x:
            return((x-1)*10)
        if not score[13][2] and dices.count(dices[0]) == 5 and not score[dices[0]-1][2]:
            return((x-1)*10)
    return(0)

def yathzee():
    if len(set(dices)) == 1:
        return(50)
    else:
        return(0)

def print_score():
    print()
    print()
    for i, s in enumerate(score):
        if s[2]:
            points = ""
        else:
            points = s[1]
        print(f"{str(i+1) + ') ' if i < 6 else ''}{str(i) + ') ' if 7 <= i <= 13 else ''}{s[0]}: {points}")
    print()
    print()

def main():
    global keep
    global available_rerolls
    print_score()
    while len([used[2] for i, used in enumerate(score) if i not in (6,14) and used[2]]) !=  0:
        print(rolling())
        if set_keep() == "assign score":
            keep = [0,0,0,0,0]
            available_rerolls = 3
            assign_score()
            print_score()
    
    print(f"Final score: {sum([points[1] for points in score])}")

main()
