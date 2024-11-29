from deck import shuffle_deck, deal_card, reset_deck
import db

def card_value(card, score, is_player_turn=False, ace_chosen=False):
    if card[0] in ["Jack", "Queen", "King"]:
        return 10
    elif card[0] == "Ace": 
        if is_player_turn and not ace_chosen:
        
            if score + 11 > 21:
                return 1
            else:
                while True:
                    choice = input(f"You drew an Ace! Choose its value (1 or 11): ")
                    if choice == "1" or choice == "11":
                        ace_chosen = True
                        return int(choice)
                    else:
                        print("Invalid choice. Please enter 1 or 11.")
        else:
            return 11 if score + 11 <= 21 else 1
    else:
        return int(card[0])

def show_hand(player_card):
    print("YOUR CARDS:")
    for card in player_card:
        print(f"{card[0]} of {card[1]}")
    print()

def calc_score(hand, is_player_turn=False):
    score = 0
    ace_chosen = False
    for card in hand:
        card_value_result = card_value(card, score, is_player_turn, ace_chosen)
        score += card_value_result
        if card[0] == "Ace" and card_value_result == 11 and not ace_chosen:
            ace_chosen = True
    return score

def place_bet(current_money):
    while True:
        bet = input(f"Bet amount (5 to 1000): $")
        print()
        try:
            bet = round(float(bet), 2)
            if bet < 5:
                print("The minimum bet is $5.")
            elif bet > 1000:
                print("The maximum bet is $1000.")
            elif bet > current_money:
                print("You don't have enough money for that bet.")
            else:
                return bet
        except ValueError:
            print("Invalid bet. Please enter a valid number.")

def title():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2\n")

def play_blackjack():

    current_money = db.load_money()
    print(f"Money: ${current_money}")
    
    if current_money < 5:
        print("You don't have enough money to play. Would you like to buy more?")
        buy_more = input("Enter 'y' to buy more or 'n' to exit: ").lower()
        if buy_more == "y":
            while True:
                amount = input("How much would you like to add? $")
                try:
                    amount = float(amount)
                    if amount >= 5:
                        current_money += amount
                        db.save_money(current_money)
                        break
                    else:
                        print("You need to add at least $5.")
                except ValueError:
                    print("Invalid amount. Please enter a number.")
        else:
            print("Goodbye!")
            return

    bet = place_bet(current_money)
    
    reset_deck()
    shuffle_deck()

    player_card = [deal_card(), deal_card()]
    dealer_card = [deal_card(), deal_card()]

    print("DEALER'S SHOW CARD")
    print(f"{dealer_card[0][0]} of {dealer_card[0][1]}\n")

    player_score = calc_score(player_card, is_player_turn=True)
    dealer_score = calc_score(dealer_card)

    if player_score == 21:
        print("BLACKJACK.\n")
        show_hand(player_card)
        print(f"YOUR POINTS:    {player_score}")
        print(f"DEALER'S SCORE: {dealer_score}\n")
        current_money += (bet * 1.5)
        db.save_money(current_money)
        return

    while True:
        show_hand(player_card)

        choice = input("What do you want to do? (hit/stand): ").lower()
        print()

        if choice == "hit":
            player_card.append(deal_card())
            player_score = calc_score(player_card, is_player_turn=True)

            if player_score == 21:
                print("BLACKJACK.\n")
                show_hand(player_card)
                print(f"YOUR POINTS:    {player_score}")
                print(f"DEALER'S SCORE: {dealer_score}\n")
                current_money += (bet * 1.5)
                db.save_money(current_money)
                return

            elif player_score > 21:
                print("Player busts! Dealer wins.\n")
                show_hand(player_card)
                print(f"YOUR POINTS:    {player_score}")
                print(f"DEALER'S SCORE: {dealer_score}\n")
                current_money -= bet
                db.save_money(current_money)
                return
        elif choice == "stand":
            break
        else:
            print("Invalid choice. Please try again.")
            continue


    while dealer_score < 17:
        dealer_card.append(deal_card())
        dealer_score = calc_score(dealer_card)

    print("DEALER'S CARDS")
    for card in dealer_card:
        print(f"{card[0]} of {card[1]}")
    print()

    print(f"YOUR POINTS:    {player_score}")
    print(f"DEALER'S SCORE: {dealer_score}\n")

    if dealer_score > 21:
        print("Dealer busts! Player wins.\n")
        current_money += bet
        db.save_money(current_money)
    elif player_score > dealer_score:
        print("Player wins (Higher score than Dealer).\n")
        current_money += bet
        db.save_money(current_money)
    elif dealer_score > player_score:
        print("Dealer wins (Higher score than Player).\n")
        current_money -= bet
        db.save_money(current_money)
    else:
        print("It's a tie.\n")

def main():
    title()
    play_blackjack()
    while True:

        replay = input("Do you want to continue? (y/n): ").lower()
        print()

        if replay == "y":
           play_blackjack()
        elif replay == "n":
            print("Come back soon!")
            print("Bye!")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
