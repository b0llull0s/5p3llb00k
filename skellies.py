## Hex generator ##
import random
import string
hex_characters='0123456789abcdef'
## User length ##
hexname_length=13  
## User name ##
hexname=''
for _ in range(hexname_length):
    hexname+=random.choice(hex_characters)
## email ##
email_list=["gmail","yahoo","outlook","proton"]
print("Choose an email from this list:\n",email_list)
email=input("Email:")
if email in email_list:
    if email=="proton":
        email=hexname+"@"+email+".me"
    else:
        email=hexname+"@"+email+".com"
else:
    print("Invalid email provider chosen.") 
print("Random Hex email address:",email)
## Password String ##
all_characters=string.ascii_letters+string.digits+string.punctuation
## Password length ##
password_length=int(input("Enter the desired length of the password: "))
password=''.join(random.choice(all_characters) for _ in range(password_length))
print("Generated Password:",password)
