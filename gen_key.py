import random
key = ""

for x in range(random.randint(200,300)):
    key += chr(random.randint(33,126))

with open("app_key.txt","w") as file:
    file.write(key)