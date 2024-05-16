#BRUAL_KEIRK_XANDREX_M. CS-1202
#Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 10, "cost": 2},
    "Super Mario Bros": {"quantity": 10, "cost": 3},
    "Tetris": {"quantity": 10, "cost": 1},
    "Pac Man": {"quantity": 10, "cost": 4 }}
#global
user_accounts = {}
users_inventory = {}
user_bought_games = {}
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print(f"\n{'-'*70} ")
    print("THIS IS THE LIST OF MOVIES AVAILABLE FOR SALE")
    print(f"{'-'*70}")
    for i, (games, details) in enumerate(game_library.items(), 1):
        quantity = details['quantity']
        cost = details ['cost']
        print(f"{i}. {games} \n     quantity: {quantity} cost: {cost}")  
    input("Press enter key to go back to main....")
# Function to register a new user
def register_user():
    print(f"\n{'-'*70}")
    print("PLEASE REGISTER YOUR DESIRED USERNAME AND PASSWORD")
    print(f"{'-'*70} ")
    username = input("Enter the username that you want to use: ")
    password = input("Enter the password that you want to use(min of 8 characters): ")
    if username in user_accounts:
        print("USERNAME IS ALREADY TAKEN...")
        input("press enter key to continue...")
    elif len(password) < 8:
        print("Invalid input of password must be more than 7 characters.")
        input("press enter key to continue...")
    else:
        user_accounts[username] = {'username': username, 'password': password, 'balance': 0,  'points': 0}
        users_inventory[username] = {}
        print("YOU HAVE CREATED YOUR ACCOUNT SUCCESFULLY.")
        input("press enter key to continue...")      
# Function to rent a game
def rent_game(username):
    print(f"\n{'-'*70}")
    print("WELCOME TO RENT GAMES TAB")
    print("AVAILABLE GAMES FOR SALE")
    print(f"{'-'*70}")
    for i, (games, details) in enumerate(game_library.items(),1 ):
        quantity = details['quantity']
        cost = details ['cost']
        print(f"{i}. {games} quantity: {quantity} cost: {cost}")
    try:
        while True:
            choice = input("\nEnter the number of the game you want to buy (type 'end' if you are done selecting your games): ")
            if choice.lower() == 'end':
                print("THANK YOU, PLEASE PROCEED TO CHECK OUT ONCE YOURE DONE..")
                input("press enter key to continue...")
                break
            number = int(choice)
            if 1 <= number <= len(game_library):
                buy_game = list(game_library.keys())[number - 1]   
                units_game = int(input("\nEnter how many units you will rent: "))
            if units_game <= 0:
                print("Input must be greater than 0...")
                continue
            else:
                if buy_game in game_library:
                    if game_library[buy_game]['quantity'] >= units_game:
                        cost_game = game_library[buy_game]['cost'] * units_game
                        if buy_game in users_inventory.get(username, {}):
                            users_inventory[username][buy_game]['quantity'] += units_game
                            users_inventory[username][buy_game]['cost'] += cost_game
                            print("SUCCESFULLY RENTED HANDLE WITH CARE.")
                        else:
                            users_inventory.setdefault(username, {}).setdefault(buy_game, {'quantity': units_game, 'cost': cost_game})
                            game_library[buy_game]['quantity'] -= units_game
                    else:
                        print("No available units for this game, please choose other games...")
                        input("press enter key to continue...")
                else:
                    print(f"Invalid input or there are no such game...")
                    input("press enter key to continue...")
    except ValueError:
        print("You can only enter numbers!")
        input("press enter key to continue...")
# Function to return a game
def return_game(username):
    print(f"\n{'-'*70}")
    print("WELCOME TO RETURN GAMES TAB")
    print("This is your current inventory")
    if not user_bought_games.get(username):
        print("Your Inventory is empty can't return games.")
        input("press enter key to continue...")
        logged_in_menu(username)
    for i, (games, details) in enumerate(user_bought_games[username].items(), 1):
        quantity = details['quantity']
        print(f"{i}. {games} quantity: {quantity}")
    try: 
        while True: 
            choice = input("\nEnter the number of the game you want to return (type 'end' if you are done selecting your games): ")
            if choice.lower() == 'end':
                print("Thank you for returning our games ")
                input("press enter key to continue...")
                break
            number = int(choice)
            if 1 <= number <= len(user_bought_games[username]):
                return_game = list(user_bought_games[username].keys())[number - 1]   
                units_game = int(input("\nEnter how many units you will return: "))
                if return_game not in user_bought_games[username]:
                    print("you're returning a game you dont have.")
                    input("press enter key to continue...")
                    break
                if units_game > user_bought_games[username][return_game]['quantity']:
                    print("Input must be lesser or equal than the unit you have...")
                    input("press enter key to continue...")
                    break
                else: 
                    if return_game in user_bought_games[username]:
                        if units_game <= user_bought_games[username][return_game]['quantity']:
                            user_bought_games[username][return_game]['quantity'] -= units_game
                            game_library[return_game]['quantity'] += units_game
                            print("successfully returned.")
                            input("press enter key to continue...")
                            break
                        else:
                            print("You dont have enough units to return please try again")
                            input("press enter key to continue...")
                            break
                    else:
                        print("You don't have this game please try again.")
                        input("press enter key to continue...")
                        break      
    except ValueError:
        print("Invalid Input Please try again.")
        input("press enter key to continue...")
#function to check out the games
def payment_out(username):
    while True:
        print("PAYOUT TAB")
        balance = user_accounts[username]['balance']
        print(f"Your Current balance is: {balance} $")
        if users_inventory.get(username):
            for i, (games, details) in enumerate(users_inventory[username].items(), 1):
                quantity = details['quantity']
                cost = details ['cost']
                print(f"{i}. {games} quantity: {quantity} cost: {cost}")
        else:
            print("Your Stash is currently empty....")
            input("press enter key to continue...")
            break
        total_to_pay = sum(details['cost']for details in users_inventory[username].values())
        print(f"your to pay is: {total_to_pay}")
        payment = input("proceed to payment? (y/n): ")
        if payment == 'y':
            if user_accounts[username]['balance'] < total_to_pay:
                print("your balance is quite low. Please top up.")
                input("press enter key to continue...")
                break
            else: 
                user_balance = user_accounts[username]['balance']
                user_balance -= total_to_pay
                user_accounts[username]['balance'] = user_balance
                reward_points = total_to_pay // 2 
                user_accounts[username]['points'] += reward_points
                for games, details in users_inventory[username].items():
                    quantity = details['quantity']     
                if username not in user_bought_games:
                    user_bought_games[username] = {}
                if games in user_bought_games[username]:
                    user_bought_games[username][games]['quantity'] += quantity
                else:
                    user_bought_games[username][games] = {'quantity': quantity}
                users_inventory[username].clear()
                print(f"Your new balance is: {user_balance} ")
                print(f"You gained {reward_points} redeemable points.")
                print("Payment complete. Please proceed.")
                print(f"\n{'-'*70}")
                print("choose from below choices.")
                print("1. Proceed to logout(back to main)") 
                print("2. Redeem points")
                print("3. Back to user login to do more.")
                choice = input("enter the number you want to do: ")
                if choice =='1':
                    main()
                elif choice =='2':
                    redeem_free_rental(username)
                elif choice == '3':
                    logged_in_menu(username)
        elif payment == 'n':
            print("PROCEED TO USER LOGIN TO DO MORE.")
            input("press enter key to continue...")
            break
        else:
            print("Invalid input please try again.")
            input("press enter key to continue...")           
# Function to top-up user account
def top_up_account(username):
    try:
        print(f"\n{'-'*70}")
        print("WELCOME TO TOPUP TAB")
        print(f"{'-'*70}")
        balance = user_accounts[username]['balance']
        print(f"Your Current balance is: {balance} $")
        new_balance = int(input("How many credits you want to top-up: "))
        if new_balance <= 0:
            print("TOP UP MUST BE GREATER THAN 1!")
            print("TRY AGAIN...")
            input("press enter key to continue...")
        else:
            balance = new_balance + balance
            print(f"your new credit balance is: {balance} $")
            user_accounts[username]['balance'] = balance
            input("press enter key to continue...") 
    except ValueError:
        print("You can only enter numbers (inetegers) !")
        input("press enter key to continue...")
# Function to display user's inventory
def display_inventory(username):
    print(f"\n{'-'*70}")
    print(f"\nWELCOME TO INVENTORY '{username}'")
    print(f"{'-'*70}")
    balance = user_accounts[username]['balance']
    print(f"Your Current balance is: {balance} $")
    print("\nHere is your to pay inventory: ")
    if users_inventory.get(username):
        for i, (games, details) in enumerate(users_inventory[username].items(), 1):
            quantity = details['quantity']
            cost = details ['cost']
            print(f"{i}. {games} quantity: {quantity} cost: {cost}")
    else:
        print("Your Stash is currently empty....")
        input("press enter key to continue...")
    print("\nhere is your paid inventory: ")
    
    if user_bought_games.get(username):
        for i, (games, details) in enumerate(user_bought_games[username].items(), 1):
            quantity = details['quantity']
            print(f"{i}. {games}\n       quantity: {quantity}")
        input("press enter key to continue...")
    else:
        print("you don't have any paid games")
        input("press enter key to continue...")
    
    
# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    try:
        print("\nWELCOME TO REDEEM TAB")
        print(f"{'-'*70}")
        while True:
            if user_accounts.get(username):
                points = user_accounts[username].get('points', )
                print(f"\nYou have {points} redeemable points. for 1 game costs 3 points")
                choice = input("would you like to redeem your points? (y/n): ")
                if choice == 'y':
                    if points < 3:
                        print("can't redeem a game")
                        input("press enter key to continue...")
                        logged_in_menu(username)
                        break
                    else:
                        for i, (games, details) in enumerate(game_library.items(), 1):
                            quantity = details['quantity']
                            cost = details ['cost']
                            print(f"{i}. {games} quantity: {quantity} cost: {cost}")
                        choice_1 = int(input("Enter the number of the game you want to redeem: "))
                        if 1 <= choice_1 <= len(game_library):
                            buy_game = list(game_library.keys())[choice_1 - 1]   
                            units_game = int(input("Enter how many units you will rent: "))
                            if units_game <= 0:
                                print("Input must be greater than 0...")
                                continue
                            else:
                                if buy_game in game_library:
                                    if game_library[buy_game]['quantity'] >= units_game:
                                        if buy_game in user_bought_games.get(username, {}):
                                            user_bought_games[username][buy_game]['quantity'] += units_game
                                            game_library[buy_game]['quantity'] -= units_game
                                            user_accounts[username]['points'] -= 3
                                        else:
                                            user_bought_games.setdefault(username, {}).setdefault(buy_game, {'quantity': units_game})
                                            game_library[buy_game]['quantity'] -= units_game
                                            user_accounts[username]['points'] -= 3
                                    else:
                                        print("No available units for this game, please choose other games...")
                                        input("press enter key to continue...")
                                else:
                                    print(f"Invalid input or there are no such game...")
                                    input("press enter key to continue...")
                        else: 
                            print("Invalid Input... Please try again.")
                            input("press enter key to continue...")
                elif choice == 'n':
                    print(f"Thank {username} for buying games.")
                    input("press enter key to proceed to login menu...")
                    logged_in_menu(username)
                    break
                else:
                    print("invalid input please choose between ('y' or 'n' ) ")
                    input("press enter key to continue...")
            else:
                print("You don't have any redeemable points")
                input("press enter key to continue...")
    except ValueError:
        print("Inavlid Input...")
        input("press enter key to continue...") 
# Function for admin to update game details
def admin_update_game():
    try:
        while True:
            for i, (games, details) in enumerate(game_library.items(), 1):
                quantity = details['quantity']
            cost = details['cost']
            print(f"{i}. {games}\n      quantity: {quantity} cost: {cost}")
            choice = input("Enter the number of the game you want to choose (type 'end' if your'e done): ")
            if choice.lower() == 'end':
                print("Please Proceed Thank You Admin.")
                input("press eneter key to continue...")
                break
            number = int(choice)
            if 1 <= number <= len(game_library):
                change_game = list(game_library.keys())[number - 1]
                if change_game in game_library:
                    print("1. Quantity")
                    print("2. Cost")
                    choice = input("Input the number that you want to change: ")
                    if choice == '1':
                        print("\nwhat do you want to do to quantity add or remove")
                        choice = input("enter '1' to add or choose '2' to remove: ")
                        if choice == '1':
                            add_quantity = int(input("How many you want to add: "))
                            if add_quantity < 0:
                                input("please enter a valid number. press enter key to continue...")
                            else:
                                game_library[change_game]['quantity'] += add_quantity
                                print(f"quantity for {change_game} is changed")
                                input("press enter key to continue...")
                        elif choice == '2':
                            minus_quantity = int(input("How many you want to add: "))
                            if minus_quantity < 0:
                                input("please enter a valid number. press enter key to continue...")
                            else:
                                game_library[change_game]['quantity'] -= minus_quantity
                                print(f"quantity for {change_game} is changed")
                                input("press enter key to continue...")
                        else:
                            print("Invalid Input. please try again.")
                            input("press enter key to conitnue...")                
                    elif choice =='2':
                        print("\nwhat do you want to do to cost add or remove")
                        choice = input("enter '1' to add or choose '2' to remove: ")
                        if choice == '1':
                            add_cost = int(input("How many you want to add: "))
                            if add_cost < 0:
                                input("please enter a valid number. press enter key to continue...")
                            else:
                                game_library[change_game]['cost'] += add_cost
                                print(f"cost for {change_game} is changed")
                                input("press enter key to continue...")
                        elif choice == '2':
                            minus_cost = int(input("How many you want to add: "))
                            if minus_cost < 0:
                                input("please enter a valid number. press enter key to continue...")
                            else:
                                game_library[change_game]['cost'] -= minus_cost
                                print(f"cost for {change_game} is changed")
                                input("press enter key to continue...")
                        else:
                            print("Invalid Input. please try again.")
                            input("press enter key to conitnue...")    
                    else:
                        print("Invalid Input. please try again.")
                        input("press enter key to conitnue...") 
                else:
                    print("GAME NOT FOUND")
                    input("press enter key to conitnue...")            
            else: 
                print("Invalid Input. Please try again.")
                input("press enter key to conitnue...") 
    except ValueError:
        print("Invalid Input.")
        input("press enter key to  continue...")
# Function for admin login
def admin_login():
    while True:
        print(f"\n{'-'*70}")
        print("WELCOME TO ADMIN LOGIN")
        print(f"{'-'*70}")
        try_admin = input("please login for verification: ")
        if try_admin == admin_username:
            try_password = input("Enter admin passcode for entry: ")
            if try_password == admin_password:
                admin_menu()
            else:
                print("Incorrect password... PLEASE TRY AGAIN.")
                input("press enter key to continue...")
        else:
            print("Incorrect username... PLEASE TRY AGAIN.")
            input("press enter key to continue...")   
# Admin menu
def admin_menu():
    while True:
        print(f"\n{'-'*70}")
        print("WELCOME TO ADMIN MENU ")
        print(f"{'-'*70}")
        print("1. Inventory check up")
        print("2. Update game details")
        print("3. Back")
        choice = input("Enter the choice that you want to do from the above numbers: ")
        if choice == '1':
            display_available_games()
        elif choice == '2':
            admin_update_game()
        elif choice == '3':
            print("THANK YOU ADMIN")
            input("press enter key to continue...")
            main() 
        else:
            print("Invalid input... PLEASE TRY AGAIN")
            input("press enter key to continue...")
# Function to handle user's logged-in menu
def logged_in_menu(username):
    while True:
        print(f"\n{'-'*70}")
        print("WELCOME TO GAME STORE")
        print(f"You are logged in as {username}")
        balance = user_accounts[username]['balance']
        print(f"Your Current balance is: {balance} $")
        print(f"{'-'*70}")
        print("1. Top-Up")
        print("2. Rent Game")
        print("3. Return Game")
        print("4. User Inventory")
        print("5. Avialable Games For Sale")
        print("6. Check Out")
        print("7. Redeem points")
        print("8. Log Out")
        choice = input("Enter the number that you want to do: ")
        if choice == '1':
            top_up_account(username)
        elif choice == '2':
            rent_game(username)
        elif choice == '3':
            return_game(username)
        elif choice =='4':
            display_inventory(username)
        elif choice == '5':
            display_available_games()
        elif choice == '6':
            payment_out(username)
        elif choice == '7':
            redeem_free_rental(username)
        elif choice == '8':
            print("THANK YOU. for buying games.")
            input("press enter key to continue...")
            break
        else: 
            print("Invalid input... PLEASE TRY AGAIN.")
            input("press any key to contiune...")
# Function to check user credentials
def check_credentials():
    try:
        while True:
            print(f"\n{'-'*70}")
            print("CHECKING LOGINS TAB")
            username = str(input("Input the username you want check in the logins: "))
            if username not in user_accounts:
                print("Username not found. PLEASE REGISTER YOUR USERNAME")
                input("press enter key to continue...")
                break
            if username in user_accounts:
                print("your username is in the current logins")
                password = input("Please input the password for your username: ")
                if password == user_accounts[username]['password']:
                    print(f"Hello {username}, You are currently in our logins!")
                    input("press enter key to continue...")
                else:
                    print("Incorrect password. PLEASE TRY AGAIN")
                    input("press enter key to continue...")
            else:
                print("Incorrect Username. PLEASE TRY AGAIN")
                input("press enter key to continue...")
    except ValueError:
        print("YOUR USER CREDENTIALS IS CURRENTLY UNAVAILABLE!")
        input("press enter key to continue...") 
# Main function to run the program
def main():
    while True:
        print(f"\n{'-'*70}")
        print("WELCOME TO GAME STORE HAPPY TO SERVE")
        print(f"{'-'*70}")
        print("1. Sign Up")
        print("2. Log In Store")
        print("3. Check Accounts")
        print("4. Admin Log In")
        print("5. Avialable Games For Sale")
        print("6. Exit")
        choice = input("\nEnter the choice that you want to do from the above numbers: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            username = input("Enter your logged username: ")
            if username in user_accounts:
                password = input("Enter your username password: ")
                if password == user_accounts[username]['password']:
                    logged_in_menu(username)
                else:
                    print("Incorrect password... PLEASE TRY AGAIN.")
                    input("press any key to continue...")
            else:
                print("Username not found... PLEASE TRY AGAIN.")
                input("press any key to continue...")
        elif choice == '3':
            check_credentials()
        elif choice == '4':
            admin_login()
        elif choice == '5':
            display_available_games()
        elif choice == '6':
            ("THANK YOU FOR SHOPPING...")
            break
        else:
            print("Invalid input... PLEASE TRY AGAIN.")
            input("press enter key to continue...")

if __name__ == "__main__":
    main()