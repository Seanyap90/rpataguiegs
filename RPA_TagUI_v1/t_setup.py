import rpa as r
import time
from time import sleep
import requests
import pandas as pd

#Declare variables and input your login details here
login_email = 'YOUR LOGIN EMAIL ACCOUNT'
login_password = 'YOUR LOGIN PASSWORD'


#logon
print("login")
r.init(visual_automation=True)
r.url('https://app.thunderquote.com')
r.click('/html/body/div[1]/div/div/div[1]/div/form[1]/div[1]/input')
r.type('Your email', login_email)
r.click('/html/body/div[1]/div/div/div[1]/div/form[1]/div[2]/input')
r.type('Your password', login_password)
r.click('/html/body/div[1]/div/div/div[1]/div/form[1]/div[3]/button')
time.sleep(2)

#go to lead page
print("go to lead page")
r.click('Find Leads')
time.sleep(6)
r.click('/html/body/div[3]/div/div[2]/div/div/div/nav/div/ul/li[1]/a')
time.sleep(3)

#find your desired categories
counting = r.count('/html/body/div[3]/div/div[2]/div/div/div/nav/div/ul/li[1]/div/a')
selection = []
category_index = []
for n in range(1, counting+1):
    category_index.append(n)
    selection_line = r.read(f'(/html/body/div[3]/div/div[2]/div/div/div/nav/div/ul/li[1]/div/a)[{n}]')
    selection.append(selection_line)

print("Please find your category")
dict = {'Category Index': category_index, 'Selection': selection}
df = pd.DataFrame(dict)
pd.set_option('display.max_rows',df.shape[0]+1)
print(df)

print("input your desired category in your next script")

r.close()

