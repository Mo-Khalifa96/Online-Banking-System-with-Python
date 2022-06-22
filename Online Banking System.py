#ONLINE BANKING SYSTEM (course project)


#Defining a function for importing information about bank clients from the file 'bank.txt'
def import_and_create_bank(filename):     
    """ This function is used to create a bank dictionary. The given argument is the
    file name or path to load. According to the file passed, a dictionary, 'bank',
    is created with the user name and account balance for each client."""

    bank = {}

    fhandle_read = open(filename, "r")
    filelines = fhandle_read.readlines()      #reads lines into a list 
    updated_list = list()
    #traversing and extracting info 
    for line in filelines:
        line = line.strip()
        wlist = line.split(":")
        if len(wlist) <= 1:
            continue
        key = wlist[0].strip()         #key = username
        value = wlist[1].strip()         #value = account balance
        try:
            value = float(value)
        except:
            continue
        # if account doesn't exist (and initially it doesn't bec. bank = {} as defined above), 
        # creates one and assigns 0 as its value
        bank[key] = bank.get(key, 0) + value

    fhandle_read.close()

    #Updating the file by storing the updated lines and rewriting them over the original file.    
    for key, val in bank.items(): 
        updated_line = str(key) + ": " + str(val) + "\n"
        updated_list.append(updated_line)

    fhandle_write = open(filename, "w")
    updated_list.sort()
    fhandle_write.writelines(updated_list)
    fhandle_write.close()

    return bank


#Defining a function for importing clients' user accounts and log-in information from the file 'users.txt'
def import_and_create_accounts(filename):       
    """This function is used to create a user accounts dictionary and
    a login dictionary. It takes a file name/path to load as an argument,
    extracts the usernames and passwords from that file, and appends them
    to the dictionaries, provided that they meet the necessary requirements.
    
    The password must meet the following requirements:
    -The password must be at least 8 characters.
    -The password must contain at least one lowercase character.
    -The password must contain at least one uppercase character.
    -The password must contain at least one numeric character.
    -The username and password cannot be the same."""

    user_accounts = {}
    log_in = {}

    #to open and read the users file
    fhandle_read = open(filename, 'r')
    filelines = fhandle_read.readlines()
    updated_list = list()
    #traversing and extracting the info 
    for line in filelines:
        line = line.strip()
        try:
            wlist = line.split("-")
        except:
            continue
        if len(wlist) <= 1:
            continue
        key = wlist[0].strip()        #key = username
        value = wlist[1].strip()      #value = password 
        #To check if the password contains at least 8 characters
        if len(value) < 8:
            continue
        #To check if the password consists of both letters and numbers, but no special characters
        elif value.isalnum() == False:
            continue
        #To check if the password is not the same as the username 
        elif key == value:  
            continue
        #To check if the password contains: uppercase letters, lowercase letters, and numeric digits
        if any(char.islower() for char in value) == True:
            if any(char.isupper() for char in value) == True:
                if any(char.isnumeric() for char in value) == True:
                    if key not in user_accounts:        #note: registers only the first username-password association it encounters
                        user_accounts[key] = value
                        log_in[key] = False
                else:
                    continue
            else:
                continue
        else:
            continue

    fhandle_read.close()

    #Now that we have read the 'users.txt' file, we can update it and rewrite it with the appropriate info
    for key, val in user_accounts.items():
        updated_line = str(key) + " - " + str(val) + "\n"
        updated_list.append(updated_line)

    fhandle_write = open(filename, 'w')
    updated_list.sort()   
    fhandle_write.writelines(updated_list)
    fhandle_write.close()

    return user_accounts, log_in


def signup(user_accounts, log_in, bank, username, password):
    """This function allows new users to sign up and create a bank account.
    If the username and password meet the requirements:
    -Updates the username and corresponding password in the user_accounts dictionary.
    -Updates the log_in dictionary, setting the value to False.
    -It returns True. Otherwise, if any of the conditions above are not met, 
    it returns False.

    The requirments for signing up:
    -The username already exists in the user_accounts.
    -The password must be at least 8 characters.
    -The password must contain at least one lowercase character.
    -The password must contain at least one uppercase character.
    -The password must contain at least one numeric character. 
    -The username and password cannot be the same."""

    #To check if the password meets the requirements 
    if len(password) < 8:
        print("\nPassword is too short. Your password should contain at least 8 characters.\nPlease try again.\n")
        return False
    if password.isalnum() == False:
        print("\nPassword is incorrect. Your password should contain no special characters.\nPlease try again.\n")
        return False
    elif username == password:
        print("\nPassword is incorrect. Your password should not be the same as your username.\nPlease try again.\n")
        return False
    
    #To check if the password contains: uppercase letters, lowercase letters, and numeric digits
    if any(char.islower() for char in password) == True:
        if any(char.isupper() for char in password) == True:
            if any(char.isnumeric() for char in password) == True:
                if username not in user_accounts:
                    #Adding the new user's info into the users.txt file 
                    user_accounts[username] = password
                    log_in[username] = False
                    fhandle1 = open("users.txt", "a")
                    fhandle1.write("{} - {}\n".format(username, password))
                    fhandle1.close()
                    #updating the user_accounts dictionary 
                    null = {}
                    user_accounts, null = import_and_create_accounts('users.txt')       #updating and sorting the users.txt file and dictionaries

                    #to ask if the user wants to open a bank account on the platform:
                    if username not in bank:
                        while True:
                            option = input("Would you like to open a bank account? (Yes/No)\n")
                            if option == "Yes" or option == "yes" or option == "Y" or option == "y":
                                bank[username] = 0.0          #new account balance 
                                #Adding the new user's info into the bank.txt file 
                                fhandle2 = open("bank.txt", "a")
                                fhandle2.write("{}: 0.0\n".format(username))
                                fhandle2.close()
                                import_and_create_bank('bank.txt')       #updating and sorting the bank.txt file
                                break
                            elif option == "No" or option == "no" or option == "N" or option == "n":
                                print("\nA bank account will not be created. Thanks for signing up!")
                                break
                            else:
                                print("\nInvalid answer. Please answer with yes or no only.")
                                continue
                    #to ensure that the function successfully carried out all of its actions
                    print("\nYou have signed up successfully.\n")
                    return True
                elif username in user_accounts:
                    print("\nAccount already exists. Try signing up again.\n")
                    return False
            else:
                print("\nPassword is incorrect. Your password should contain at least one numeric character.\nPlease try again.\n")
                return False
        else:
            print("\nPassword is incorrect. Your password should contain at least one uppercase letter.\nPlease try again.\n")
            return False
    else:
        print("\nPassword is incorrect. Your password should contain at least one lowercase letter.\nPlease try again.\n")
        return False


def login(user_accounts, log_in, username, password):
    """This function allows users to log in with their username and
    password. The user_accounts dictionary and log_in dictionary
    have the users' information stored in advance.
    If the username does not exist in user_accounts or the password
    is incorrect, this function returns False.
    Otherwise, if the username and passwords meet the requirements:
    -it updates the user's log-in status to True, and
    -returns True."""

    if username in user_accounts:
        if user_accounts[username] == password:
            log_in[username] = True
            print("\nYou have logged in successfully.\n")
            return True
        else:
            print("\nThe password you entered is incorrect. Try again.")
            return False
    else:
        print("\nLog-in unsuccessful. You are not registered in the system.\n")
        return False


def update(bank, log_in, username, amount):
    """This function updates users' bank account with a given amount.

    'bank' is a dictionary which stores the user's username and corresponding
    income amount.
    log_in is a dictionary which stores the user's log-in status.
    'amount' is the new income amount to update the bank dictionary with. The
    amount can be positive or negative.

    To update a user's account the following conditions must be met:
    -The user exists in the log_in dictionary.
    -The user's status must be True, i.e. they're logged in.
    If the user doesn't exist in the bank dictionary, this function:
    -Creates a bank account
    -The starting amount cannot be negative in the bank account.

    Finally, this function returns True if the user's account was updated.
    Otherwise, if the account wasn't updated, it returns False."""

    if username in log_in:
        #checks if the user is currently logged in
        if log_in[username] == True: 
            #if the user created an online "user account", are currently logged in, but they don't have a BANK ACCOUNT:
            if username not in bank:
                if amount >= 0:
                    bank[username] = amount          #creates a new bank account with the given balance
                    #Adding the new user's info into the bank.txt file  
                    fhandle = open("bank.txt", "a")
                    new_entry = "{}: {}".format(username, amount)
                    fhandle.write(new_entry + '\n')
                    fhandle.close()
                    import_and_create_bank('bank.txt')
                    print("\nYour new bank account was created successfully. Your starting balance is {}.\n".format(amount))
                    return True
                elif amount < 0:
                    print("\nYour starting balance cannot be negative. Please try again.")
                    return False

            #if they've created an online account, are logged in, AND have a bank account:
            elif username in bank:
                new_amount = bank[username] + amount       #updates the account balance with the new amount
                if new_amount >= 0:
                    bank[username] = new_amount
                    #Updating the user's info in the bank.txt file 
                    fhandle = open("bank.txt", "a")
                    new_entry = "{}: {}".format(username, new_amount)
                    fhandle.write(new_entry + '\n')
                    fhandle.close()
                    #to sort the bank.txt file appropriately and update the dictionaries
                    import_and_create_bank('bank.txt')
                    #to ensure that the function successfully carried out all of its actions
                    print("\nYour account balance was updated successfully.\n")
                    return True
                elif new_amount < 0:
                    print("\nBalance update was unsuccessful. The resulting balance cannot be negative.\n")
                    return False
        else:
            print("\nBalance update was unsuccessful. You are not logged in. Please try logging in first.\n")
            return False
    else:
        print("\nBalance update was unsuccessful. You are not registered in the system.\nSign up first and then try again.\n")
        return False


def transfer(bank, log_in, userA, userB, amount):
    """This function performs money transfer between two user accounts, userA and userB.
    the bank dictionary stores users' usernames and account balance.

    'log_in' stores users' log-in status.
    'amount' is the amount to be transferred between the two user accounts. It's always positive.

    The following requirements must be met for transaction to be successful:
    -UserA must be in the bank, must be in log_in, and their log-in status must be True.
    -UserB doesn't have to be in the bank, but they must be in log_in, regardless of their current log-in status.
    -No user can have a negative amount in their account (neither before nor after transaction).

    If transfer is successful, it returns True."""

    if userA in bank and userB in bank:
        if userA in log_in and userB in log_in:
            if log_in[userA] == True:
                if bank[userA] >= 0:
                    #substracting the amount to be transfered from the sender (userA) and adding it to the receiver(userB)
                    userA_after_amount = bank[userA] - amount
                    userB_after_amount = bank[userB] + amount
                    if userA_after_amount >= 0 and userB_after_amount >= 0:
                        bank[userA] = userA_after_amount
                        bank[userB] = userB_after_amount
                        #to update the files with the balance changes in both accounts 
                        fhandle = open('bank.txt', 'a')
                        fhandle.write("{}: ".format(userA) + str(float(-amount)) + '\n')
                        fhandle.write("{}: ".format(userB) + str(float(+amount)) + '\n')
                        fhandle.close()
                        import_and_create_bank('bank.txt')        #to sort the file correctly
                        #to ensure that the function successfully carried out all of its actions
                        print("\nMoney transaction was completed successfully. Your account balance is currently: {}.\n".format(userA_after_amount))
                        return True
                    else:
                        print("\nTransaction was unsuccessful. Amount is not enough to complete the required transaction.\n")
                        return False
                else:
                    print("\nTransaction unsuccessful. Your balance is not enough to make a transaction.\n")
                    return False
            else:
                print("\nTransaction was unsuccessful. You are not logged in.\nTry logging in first before making a transaction.\n")
                return False
        else:
            if userA not in log_in:
                print("\nTransaction was unsuccessful. {} is not currently registered in the system.\nTry signing up first before making a transaction.\n".format(userA))
                return False
            elif userB not in log_in:
                print("\nTransaction was unsuccessful. {} is not currently registered in the system.\n".format(userB))
                return False
    else:
        if userA not in bank:
            print("\nThis user: {}, doesn't have a bank account.\n".format(userA))
        elif userB not in bank:
            print("\nThis user: {}, doesn't have a bank account.\n".format(userB))
        return False


def change_password(user_accounts, log_in, username, old_password, new_password):
    """This function allows users to change their password.

    If all of the following requirements are met, this function changes
    the password and returns True. Otherwise, returns False.
    The requirements are:
    -The username exists in in the user_accounts dictionary.
    -The user is logged in.
    -The old_password is the user's current password.
    -The new_password should be different from the old one.
    -The new_password fulfills the requirements in signup."""

    #password filters 
    if len(new_password) < 8:
        print("\nPassword is too short. Your password should contain at least 8 characters.\nPlease try again.\n")
        return False
    elif new_password.isalnum() == False:
        print("\nPassword is incorrect. Your password should contain no special characters.\nPlease try again.\n")
        return False
    elif username == new_password:
        print("\nPassword is incorrect. Your password should not be the same as your username.\nPlease try again.\n")
        return False
    if any(char.islower() for char in new_password) == True:
        if any(char.isupper() for char in new_password) == True:
            if any(char.isnumeric() for char in new_password) == True:
                #if all the previous conditions were met, the new_password is valid
                #to try to update the password
                if username in user_accounts:
                    if username in log_in:
                        if log_in[username]:        # i.e. if log_in[username] == True
                            if user_accounts[username] == old_password:
                                if old_password != new_password:
                                    #to change the password
                                    user_accounts[username] = new_password
                                    
                                    #to update the files
                                    new_entry = "{} - {}\n".format(username, new_password)
                                    with open("users.txt", "r") as fhandle:
                                        filelines = fhandle.readlines()
                                        filelines.insert(0, new_entry)
                                    with open("users.txt", "w") as fhandle_updated:
                                        fhandle_updated.writelines(filelines) 
                                    #to sort the users.txt file correctly and update the dictionaries
                                    import_and_create_accounts('users.txt')
                                    #to ensure that the function successfully carried out all of its actions
                                    print("\nYour password was changed successfully.\n")
                                    return True
                                else:
                                    print("\nChanging password was unsuccessful.\nYour new password cannot be the same as your old password. Please try entering another one.\n")
                                    return False
                            else:
                                print("\nChanging password was unsuccessful.\nThe password you entered is incorrect. Please try again.\n")
                                return False
                        else:
                            print("\nChanging password was unsuccessful.\nYou are not currently logged in. Try logging in first before changing your password.\n")
                            return False
                    else:
                        print("\nChanging password was unsuccessful.\nYou are not currently registered in the system.\n")
                        return False
                else:
                    print("\nChanging password was unsuccessful.\nYou are not currently registered in the system.\n")
                    return False
            else:
                print("\nPassword is incorrect. Your password should contain at least one numeric character.\nPlease try again.\n")
                return False
        else:
            print("\nPassword is incorrect. Your password should contain at least one uppercase letter.\nPlease try again.\n")
            return False
    else:
        print("\nPassword incorrect. Your password should contain at least one lowercase letter.\nPlease try again.\n")
        return False


def delete_account(user_accounts, log_in, bank, username, password):
    """This function completely deletes the user from the online banking system:
    if all the requirements are met, it deletes the user from the bank dictionary,
    the user_accounts dictionary, and the log_in dictionary.
    The requirements are:
    -The user exists in the bank, user_accounts, and log_in dictionaries.
    -The user's password is correct.
    -The user is currently logged in.

    Upon completion, this function returns True. If any of the requirements
    isn't met, it returns False."""

    if username in bank and username in user_accounts and username in log_in:
        if user_accounts[username] == password:
            if log_in[username] == True:
                del bank[username]              
                del user_accounts[username]
                del log_in[username]
                #to delete the user from the files
                with open("bank.txt", "r") as fhandle:
                    filelines = fhandle.readlines()
                with open("bank.txt", "w") as fhandle_updated:
                    for line in filelines:
                        if username not in line:
                            fhandle_updated.write(line)
                        else:
                            continue 
                #to sort the file appropiately and update the dictionaries
                import_and_create_bank('bank.txt')         
                #same goes for the users.txt file
                with open("users.txt", "r") as fhandle:
                    filelines = fhandle.readlines()
                with open("users.txt", "w") as fhandle_updated:
                    for line in filelines:
                        if username not in line:
                            fhandle_updated.write(line)
                        else:
                            continue  
                #to sort the users.txt file appropriately and update the dictionaries 
                import_and_create_accounts('users.txt') 
                #to ensure that the function successfully carried out all of its actions
                print("\nYour account was deleted successfully.\n")
                return True
            else:
                print("\nAccount delete unsuccessful.\nYou are not currently logged in. Try logging in first before deleting your account.\n")
                return False
        else:
            print("\nAccount delete unsuccessful.\nThe password you entered is incorrect. Please try again.\n")
            return False
    else:
        print("\nAccount delete unsuccessful.\nYou are not currently registered in the bank or don't have an online account.")
        return False


#The program's main function 
def main():
    """The main function is a skeleton for testing the functionality of the overall program."""

    bank = import_and_create_bank("bank.txt")
    user_accounts, log_in = import_and_create_accounts("users.txt")      

    while True:
        #for debugging purposes:
        #print('\nbank:', bank)
        #print('user_accounts:', user_accounts)
        #print('log_in:', log_in)
        #print('')

        option = input("What do you want to do? Please enter a numeric option below.\n"
        "1. login\n"
        "2. signup\n"
        "3. change password\n"
        "4. delete account\n"
        "5. update amount\n"
        "6. make a transfer\n"
        "7. exit\n\n"
        "Enter choice: ")
        print('')

        if option == "1":
            username = input("Please input the username\n")
            password = input("Please input the password\n")
            #Executes the login() function
            login(user_accounts, log_in, username, password)
        elif option == "2":
            username = input("Please input the username\n")
            password = input("Please input the password\n")
            #Executes the signup() function
            signup(user_accounts, log_in, bank, username, password)
        elif option == "3":
            username = input("Please input the username\n")
            old_password = input("Please input the old password\n")
            new_password = input("Please input the new password\n")
            #Executes the change_password() function
            change_password(user_accounts, log_in, username, old_password, new_password)
        elif option == "4":
            username = input("Please input the username\n")
            password = input("Please input the password\n")
            #Executes the delete_account() function
            delete_account(user_accounts, log_in, bank, username, password)
        elif option == "5":
            username = input("Please input the username\n")
            while True:
                amount = input("Please input the amount\n")
                try:
                    amount = float(amount)
                    break
                except:
                    print("\nThe amount you entered is invalid. Please re-enter a valid amount.\n")
                    continue
            #Executes the update() function
            update(bank, log_in, username, amount)
        elif option == "6":
            userA = input("Please input the user who will be deducted\n")
            userB = input("Please input the user who will be added\n")
            while True:
                amount = input("Please input the amount\n")
                try:
                    amount = float(amount)
                    break
                except:
                    print("\nThe amount you entered is invalid. Please re-enter a valid amount.\n")
                    continue
            #Executes the transfer() function
            transfer(bank, log_in, userA, userB, amount)
        elif option == "7":
            #Exits the main() function
            print("\nGoodbye, we hope to see you again!")
            break
        else:
            print("The option you entered is invalid. Please re-enter a valid option.\n")
            continue 

#to execute the main function/the whole program
if __name__ == "__main__":
    main()
