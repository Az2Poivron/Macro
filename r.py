import requests
import time
import random
car = """Sutczito
BeefCakeLlama
Darkenden88
onkolik
weedwarden
don080
XprTo
Nioo2
jappa25
19yubo85
Moreau
Patryk5813
Skyfall00
Chrissiu
klicias
Kyr4l
don080
ricarsme
Danichinos
kirayoshikage14
thundersammie
invinciblyad
ityk0416
SCX55
White2137
RevisedCube
don080
TheBunker
Szkudziu
lyleargyll"""

L = car.split("\n")

cookies_dict = {"cookie": "update=valid; auth_user=Searcher; token=98595140b81b78bf3a087372f365ac62; news_curse=activated; devnotif3=executed; PHPSESSID=u9g8k02eqqm955217gq1ki8qks; friendUpdate=applied"}
for x in L:
    #time.sleep(random.randint(3,20))
    r = requests.get(f"https://web.galaxylifereborn.com/profile/{x}&a=c", cookies=cookies_dict)
    print("[SEND]",x)

