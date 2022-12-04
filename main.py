import random
from datetime import date
from datetime import datetime

class Player():
    def __init__(self):
        self.name = input("What is your name? ")
        self.bet = 5
        self.money = 100
        self.currency = "€"

    def betChanger(self):
        print("You have", self.money, self.currency, "left.")
        try:
            self.bet = int(input("How much do you want to bet? "))
            if self.bet > self.money:
                print("You don't have enough money.")
                self.betChanger()
            else:
                self.bet = self.bet
        except ValueError:
            print("Please enter a number.")
            self.betChanger()
    
    def deposit(self):
        try:
            self.money += int(input("How much do you want to deposit? "))
            with open(f"log_{self.name}_{date.today()}.txt", "a") as log:
                log.write(f"{datetime.now()} - {self.name} deposited {self.money} {self.currency}.\n")
            self.money = self.money
        except ValueError:
            print("Please enter a number.")
            self.deposit()


class SlotMachine():

    leftReel = [ 1, 1, 3, 4, 5, 2, 2, 3, 4, 2, 2, 5, 3, 5, 3, 4, 2, 1, 2, 5, 4, 3, 2]
    middleReel = [ 3, 1, 2, 2, 3, 5, 4, 4, 2, 2, 3, 2, 1, 5, 4, 3, 3, 2, 1, 5, 4, 1, 3, 5]
    rightReel = [2, 3, 5, 4, 4, 3, 1, 1, 2, 2, 3, 5, 4, 3, 2, 1, 2, 1, 5, 1, 3, 4, 1, 5, 2]

    def spin(self, player):
        if player.money >= player.bet:
            left = random.choice(self.leftReel)
            middle = random.choice(self.middleReel)
            right = random.choice(self.rightReel)
            spin_result = (left, middle, right)
            self.printResult(spin_result)
            bonus_amplifier = self.checkBonus(spin_result, player)
            if bonus_amplifier > 0:
                player.money += player.bet * bonus_amplifier
                print("You won", player.bet * bonus_amplifier, player.currency)
            else:
                player.money -= player.bet
                print("You lost", player.bet, player.currency)
            self.resultLog(player, spin_result, bonus_amplifier)
        elif player.money >= 5:
            player.betChanger()
        else:
            print("You don't have enough money to play.")
            player.deposit()
            exit()

    def printResult(self, spin_result):
        num_to_emoji = {1: "🍒", 2: "🍊", 3: "🍇", 4: "🍓", 5: "🍍"}
        print("________________")
        print("|", num_to_emoji[spin_result[0]], "|", num_to_emoji[spin_result[1]], "|", num_to_emoji[spin_result[2]], "|")
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    def resultLog(self, player, result, bonus_amplifier):
        with open(f"log_{player.name}_{date.today()}.txt", "a") as log:
            msg = f"timestamp: {datetime.now()},player_name:{player.name},result:{result},bet:{player.bet},amplifier:{bonus_amplifier},wallet_before_play:{player.money} {player.currency},wallet_after_play: {player.money + (player.bet * bonus_amplifier)  if bonus_amplifier > 0 else player.money - player.bet} {player.currency}\n"
            log.write(msg)

    def checkBonus(self, result, player):
        match result:
            case (1, 1, 1):
                bonus_amplifier = 2
            case (2,2,2):
                bonus_amplifier = 7
            case (3,3,3):
                bonus_amplifier = 10
            case (3,3,1):
                bonus_amplifier = 2
            case (3,3,2):
                bonus_amplifier = 2
            case (3,3,4):
                bonus_amplifier = 3
            case (3,3,5):
                bonus_amplifier = 4
            case (4,4,4):
                bonus_amplifier = 15
            case (4,4,1):
                bonus_amplifier = 5
            case (4,4,2):
                bonus_amplifier = 5
            case (4,4,3):
                bonus_amplifier = 2
            case (4,4,5):
                bonus_amplifier = 6
            case (1,2,3):
                bonus_amplifier = 2
            case (5,5,1):
                bonus_amplifier = 2
            case (5,5,5):
                bonus_amplifier = 70
            case _:
                bonus_amplifier = 0
        return bonus_amplifier 

def main():
    player = Player()
    slot_machine = SlotMachine()

    print("Welcome to the Slot Machine!")
    print("Current bet:", player.bet, player.currency)
    while True:
        print("Current money:", player.money, player.currency)
        decision = input("X - Spin\t\t\tC - Change bet\t\t\tD-Deposit Money\t\t\tQ - Quit\n")
        match decision.lower():
            case "x":
                slot_machine.spin(player)
            case "c":
                player.betChanger()
            case "q":
                print("Thanks for playing!")
                exit()
            case "d":
                player.deposit()
            case _: 
                print("Invalid input. Please try again.")
                main()

if __name__ == "__main__":
    main()