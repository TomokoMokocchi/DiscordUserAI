import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.chrome.service import Service
import time
import json
import threading
import pyperclip
import shutil
import urllib
import zipfile
import atexit
from io import BytesIO
from selenium.webdriver import ActionChains
import struct

size_in_bits = str(struct.calcsize("P") * 8)
print(f"Python is running in {size_in_bits}-bit mode (using struct)")

def get_documents_folder():
    return os.path.expanduser("~/Documents")

url = "http://127.0.0.1:5000/v1/chat/completions"


headers = {
    "Content-Type": "application/json"
}

history = []

character = "Assistant"

lastmsg = ""

def my_exit_function():
    try:
        driver.quit()
    except:
        pass

driverver = 0

def update():
    global driverver
    print("Updating chrome drivers...",flush=True)
    lastver = "116.0.5809.2"
    latestversion = 0
    with urllib.request.urlopen("https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json") as url:
        data = json.load(url)
        a = data["versions"]
        for item in a:
            if float(item["version"][:5])>=float(lastver[:5]):
                    for temp in item["downloads"]["chromedriver"]:
                        if temp["platform"]=="win"+size_in_bits:
                            lastver = item["version"]
                            latestversion = temp["url"]
                    for temp in item["downloads"]["chrome"]:
                        if temp["platform"]=="win"+size_in_bits:
                            lastver = item["version"]
                            latestchver = temp["url"]
    print("Found update urls: "+latestversion +"\n" +latestchver,flush=True)

    path = os.getcwd()+"/driver/"+lastver
    driverver = lastver
    if os.path.exists(path):
        print("Drivers already up to date!")
    else:
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(e)
            pass
        os.makedirs(path)
        with urllib.request.urlopen(latestversion) as zipresp:
            with zipfile.ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(path)
        with urllib.request.urlopen(latestchver) as zipresp:
            with zipfile.ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(path)
                print("Chromedriver successfully updated to: " + lastver,flush=True)

update()

try:
    os.makedirs(get_documents_folder()+"/PasswordInfo/")
except:
    pass
if os.path.exists(get_documents_folder()+'/PasswordInfo/info.json'):
    with open(get_documents_folder()+'/PasswordInfo/info.json', 'r') as file:
        data = json.load(file)
else:
    os.system('cls')
    print("Discord Email: ")
    eminput = input("> ")
    print("Discord Password: ")
    pwinput = input("> ")
    data = {"Password":pwinput,"Email":eminput}
    with open(get_documents_folder()+'/PasswordInfo/info.json', 'w') as f: # This saves your discord login in your documents folder.
        json.dump(data, f, indent=4)
    os.system('cls')

def outputtodiscord(msg):
    try:

        msgbox = driver.find_element(By.XPATH, "//div[@class='placeholder__1b31f slateTextArea_ec4baf fontSize16Padding__74017']/../div[2]/div/span")

        pyperclip.copy(":robot: "+msg)
        act = ActionChains(driver)
        act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        msgbox.send_keys(" \n")
    except:
        time.sleep(0.1)
        outputtodiscord(msg)



def sendmessage(msg,reply):
    history.append({"role": "user", "content": msg})
    data = {
        "mode": "chat",
        "character": character,
        "messages": history
    }
    if reply!=None:
        try:
            action = ActionChains(driver)
            action.move_to_element(reply)
            action.click()
            action.perform()
        except Exception as e:
            print(e,flush=True)
    def generate():
        localgenerated = requests.post(url, headers=headers, json=data, verify=False)
        testa = localgenerated.json()['choices'][0]['message']['content']
        if len(testa)>2000:
            return generate()
        else:
            return testa
    response = generate()
    history.append({"role": "assistant", "content": response})
    print(character+": "+ response)
    outputtodiscord(character+": "+ response)



if __name__ == "__main__":
    checkingpings = False
    atexit.register(my_exit_function)
    # Open and read the JSON file

    email = data["Email"]
    password = data["Password"]


    service = Service(executable_path=os.getcwd()+"/driver/"+driverver+"/chromedriver-win"+size_in_bits+"/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.binary_location = os.getcwd()+"/driver/"+driverver+"/chrome-win"+size_in_bits+"/chrome.exe"
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://discord.com/app')

    def checkelementexists(type,path,timesran=0):
        try:
            return driver.find_element(type, path)
        except:
            time.sleep(0.2)
            if timesran>2:
                return False
            else:
                return checkelementexists(type,path)
            
    def waitforelement(type,path):
        try:
            return driver.find_element(type, path)
        except:
            time.sleep(0.2)
            return waitforelement(type,path)

    time.sleep(2)

    if "login" in driver.current_url:
        emailbox = waitforelement(By.XPATH, "//input[@name='email']")
        emailbox.send_keys(email)
        passwordbox = waitforelement(By.XPATH, "//input[@name='password']")
        passwordbox.send_keys(password)
        login = waitforelement(By.XPATH, '//div[text()="Log In"]')
        login.click()
    def checkpings():
        global checkingpings
        try:
            aaa = driver.find_elements(By.XPATH, "//div[@class='numberBadge__2b1f5 base__2b1f5 eyebrow__2b1f5 baseShapeRound__2b1f5']")
            checkingpings = True
            for clicklol in aaa:
                time.sleep(0.3)
                try:
                    oof = clicklol.find_element(By.XPATH, "./../../../../..")
                    oof.click()
                except:
                    pass
                try:
                    oof = clicklol.find_element(By.XPATH, "./../../../..")
                    oof.click()
                except:
                    pass
                try:
                    oof = clicklol.find_element(By.XPATH, "./../../../")
                    oof.click()
                except:
                    pass
                try:
                    oof = clicklol.find_element(By.XPATH, "./../..")
                    oof.click()
                except:
                    pass
                try:
                    action = ActionChains(driver)
                    action.move_to_element(clicklol)
                    action.move_by_offset(-25, 0)
                    action.click()
                    action.pause(0.5)
                    action.click()
                    action.move_to_element(clicklol)
                    action.perform()
                    time.sleep(0.5)
                except Exception as e:
                    pass
                try:
                    oof = clicklol.find_element(By.XPATH, "./../../../../..")
                    oof.click()
                except Exception as e:
                    pass
            checkingpings = False
        except:
            pass

    speaker = character

    time.sleep(1.5)

    waitforelement(By.XPATH, "//div[@aria-label='Add Friend']").click()

    newestmsg = ""
    lastmsg = newestmsg
    time.sleep(1)
    localpfp = waitforelement(By.XPATH, "(//img[@class='avatar__44b0c'])[last()]").get_attribute("src")
    driver.minimize_window()
    print("Found user PFP: "+localpfp)

    while True:
        checkpings()
        try:
            newestmsg = ""
            messagestrings = driver.find_elements(By.XPATH, "(//div[@class='contents_c19a55'])[last()]/div/*")
            for localmsg in messagestrings:
                try:
                    newestmsg = newestmsg+localmsg.text
                except:
                    pass
            reply = None
            pfp = driver.find_element(By.XPATH, "(//img[@class='avatar_c19a55 clickable_c19a55'])[last()]").get_attribute("src")
            if lastmsg!=newestmsg and newestmsg!="" and checkingpings==False:
                if pfp.split("size=")[0]!=localpfp.split("size=")[0] or not character in newestmsg and pfp.split("size=")[0]==localpfp.split("size=")[0]:
                    speaker = driver.find_element(By.XPATH, "(//span[@class='headerText_c19a55'])[last()]/span").text
                    try:
                        if pfp.split("size=")[0]!=localpfp.split("size=")[0]:
                            msgthing = driver.find_element(By.XPATH, "(//div[@class='contents_c19a55'])[last()]")
                            action = ActionChains(driver)
                            action.move_to_element(msgthing)
                            action.perform()

                            reply = driver.find_element(By.XPATH, "(//div[@aria-label='Reply'])[last()]")
                    except Exception as e:
                        pass

                    print(speaker+ ": "+newestmsg,flush=True)
                    threading.Thread(target=sendmessage, args=(speaker+ ": "+newestmsg,reply,)).start()
            lastmsg = newestmsg
        except Exception as ex:
            pass