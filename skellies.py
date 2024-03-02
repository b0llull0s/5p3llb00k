import random
import string
## Variables ##
hex_characters='0123456789abcdef'
email_list=["gmail","yahoo","outlook","proton"]
## Funtions ##
def generate_hex_email(email):
    hexname_length=13
    hexname=''
    for _ in range(hexname_length):
        hexname+=random.choice(hex_characters)
    if email=="proton":
        return hexname+"@"+email+".me"
    else:
        return hexname+"@"+email+".com"

def generate_password(password_length):
    all_characters=string.ascii_letters+string.digits+string.punctuation
    return ''.join(random.choice(all_characters)for _ in range(password_length))
## Loop ##
num_combinations=int(input("How many skelletons do you want? "))
if num_combinations<1:
    print("Invalid number of combinations.")
else:
    for _ in range(num_combinations):
        print("Choose an email from this list:\n",email_list)
        email=input("Email: ").lower()
        if email in email_list:
            email=generate_hex_email(email)
            print("Random Hex email address:",email)
            password_length=int(input("Desired length of the password? "))
            password=generate_password(password_length)
            print("Generated Password:", password)
        else:
            print("Invalid email provider chosen.")
