import random
import string
## Variables ##
hex_characters='0123456789abcdef'
email_list=["gmail","yahoo","outlook","proton"]
## Hex username ##
def generate_hex_email(email,hexname_length):
    hexname=''
    for _ in range(hexname_length):
        hexname+=random.choice(hex_characters)
    if email=="proton":
        return hexname+"@"+email+".me"
    else:
        return hexname+"@"+email+".com"
## Functions ##
def generate_password(password_length):
    all_characters=string.ascii_letters+string.digits+string.punctuation
    return ''.join(random.choice(all_characters) for _ in range(password_length))

def write_to_file(data):
    with open("skellies.txt","a") as file:
        file.write(data+"\n")
## Loop ##
while True:
    num_combinations = int(input("How many different username and password combinations do you want? "))
    if num_combinations<1:
        print("Invalid number of combinations.")
        continue
    password_length=int(input("Enter the desired length of the password: "))
    repeat_email=input("Do you want to repeat the same email for all combinations? (yes/no): ").lower()=="yes"
    if repeat_email:
        print("Choose an email from this list:\n", email_list)
        email=input("Email: ").lower()
        if email not in email_list:
            print("Invalid email provider chosen.")
            continue
        hexname_length=int(input("Desired length of the hexname? "))
        email=email.split('@')[0]  # Resetting email to the original provider
        for _ in range(num_combinations):
            email_with_hexname=generate_hex_email(email, hexname_length)
            write_to_file(f"Email:{email_with_hexname},Password:{generate_password(password_length)}")
    else:
        for _ in range(num_combinations):
            print("Choose an email from this list:\n",email_list)
            email=input("Email: ").lower()
            if email not in email_list:
                print("Invalid email provider chosen.")
                continue
            hexname_length=int(input("Desired length of the hexname? "))
            email_with_hexname=generate_hex_email(email,hexname_length)
            write_to_file(f"Email:{email_with_hexname},Password:{generate_password(password_length)}")
            print("Skelletons Raised!")
    another_round=input("Do you want to raise more skelletons? (y/n): ").lower()
    if another_round != "y":
        break
