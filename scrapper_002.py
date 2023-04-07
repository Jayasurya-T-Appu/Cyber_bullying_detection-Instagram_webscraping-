from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import os
import joblib
import json
import smtplib, ssl
from email.message import EmailMessage
from flask import Flask, render_template

# Set up the webdriver
driver = webdriver.Chrome()

Scrapping = True
post = 1

# Navigate to the Instagram post
driver.get('https://www.instagram.com/')
driver.maximize_window()
time.sleep(3)

username = ""
password = ""

driver.find_element(By.NAME, 'username').send_keys(username)
time.sleep(2)
driver.find_element(By.NAME, 'password').send_keys(password)
time.sleep(2)

driver.find_element(By.XPATH, '//button[contains(@class, "_acan _acap _acas _aj1-")]').click()
time.sleep(5)


# Find Not Now Button
try:
    notn = driver.find_element(By.XPATH, "//*[contains(text(),'Not Now')]")
    notn.click()
    time.sleep(5)
except:
    pass

try:
    notn = driver.find_element(By.XPATH, "//*[contains(text(),'Not Now')]")
    notn.click()
    time.sleep(5)
except:
    pass

# Getting profile page

profileClick = driver.find_element("xpath", "//*[contains(text(),'Profile')]")
profileClick.click()
time.sleep(5)

# selecting the first post
first_post = "//article[contains(@class, 'x1iyjqo2')]/div/div/div/div[1]"
driver.find_element(By.XPATH, first_post).click()




# Loading full comments 
def loadAllComments():
    global post
    print(f"Loading Comment of post : {post} ")
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        last_height = new_height
        return True


# Getting all comments to a file
def write_comments_text():
    time.sleep(5)
    global post
    print(f"Writing comments to a file of post : {post}")
    commentSection = driver.find_element(By.XPATH, "//ul[@class='_a9z6 _a9z9 _a9za']") # replace class name if doesnt work
    spans = commentSection.find_elements(By.TAG_NAME,'span')
    time.sleep(3)
    f = open("data.txt", "a",encoding='utf-8')
    
    for span in spans:
        print(span.text)
        f.write(f"{span.text}")
        f.write(f"\n")
    f.close()    
    

# Clicking next to the next post
def click_next():
    global Scrapping
    try:
        print("Trying to go next page")
        next_btn = driver.find_element(By.XPATH, "//div[@class='_aeap _aeaq']/div/div[@class=' _aaqg _aaqh']")
        next_btn.click()
        time.sleep(5)
    except:
        print("Scrapping is done..")
        Scrapping = False
    

while Scrapping:
    loadAllComments()
    write_comments_text()
    click_next()



f = open('data.txt','r',encoding='utf-8')
s = open('data_after.txt', 'a',encoding='utf-8')

for line in f:
    line = line.strip()
    if len(line)> 0:
        if re.search(r'View replies \(\d+\)', line):
            pass
        else : s.write(f"{line}\n")
f.close()
s.close()

dict ={}
lst =[]
lst_name=[]
lst_comment=[]
s = open('data_after.txt', 'r',encoding='utf-8')
for line in s:
    lst.append(line.strip("\n"))

lst_name=lst[0::2]
lst_comment=lst[1::2]




    
# ######################################################
if os.path.exists("trained_model_30min.pkl") and os.path.exists("vectorizer_30min.pkl"):
    # Load the saved model and vectorizer from files
    clf = joblib.load("trained_model_30min.pkl")
    vectorizer = joblib.load("vectorizer_30min.pkl")

def predict(input_text):

    input_features = vectorizer.transform([input_text])

    # Predict the class label for the input text
    predicted_label = clf.predict(input_features)[0]

    # Map the predicted label to a class name
    class_name = "Non-Bullying" if predicted_label == 0 else "Bullying"

    # Print the result
    return class_name



# dict = {}
# bully_dict = {}
lst_bullying=[]
for i in range(len(lst_comment)):
    clasname = predict(lst_comment[i])
    lst_bullying.append(clasname)
    

dict= {
    "names" : lst_name,
    "comments" : lst_comment,
    "classname" : lst_bullying
}


with open("./website/src/predicted_data.json","w")as f:
    json.dump(dict, f)
    



with open("bullying_data.json","w")as f:
    json.dump(dict, f)

driver.close()

def mail_sender():
    port = 587  
    smtp_server = "smtp.outlook.com"
    sender_email = ""
    receiver_email = ""
    password = ""
    message = EmailMessage()
    message["Subject"] = "Cyber Bullying Report"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    try:
        message.set_content( "" + " found please take action.", subtype="plain", charset='utf-8')
    except:
         time.sleep(2)
                
                
    with open('./bullying_data.json', 'r') as f:
                json_data = f.read()
                message.add_attachment(json_data, filename='bullying_data.json')
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  
                    server.starttls(context=context)
                    server.ehlo()  
                    server.login(sender_email, password)
                    server.send_message(message)
                    
try:

    mail_sender()
except:
    pass


import subprocess
curent_wd = os.path.dirname(os.path.abspath(__file__))
result = subprocess.run('cd website && npm run build', shell=True, cwd=curent_wd)




staticPath = "./website/build/static"
temp_folder = './website/build'
app = Flask(__name__, static_folder =staticPath, template_folder=temp_folder)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()


