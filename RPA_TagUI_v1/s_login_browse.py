import rpa as r
import time
from time import sleep
import requests
import pandas as pd
import csv

#this assumes that user is familiar with browsing through seasmi procurement platform to view various RFQ details
#declare variables for login details
Org_ID = 'YOUR ORG ID'
User_ID = 'YOUR USER ID'
Password = 'YOUR PASSWORD'


#login to sesami
r.init(visual_automation = True)
r.url('https://sesami.online/nus/Login.jsp')
r.click('OrgID')
r.type('Org ID', Org_ID)
r.click('UserID')
r.type('User ID', User_ID)
r.click('Password')
r.type('Password', Password)
r.click('OrgID')
r.keyboard('[tab]')
r.click('UserID')
r.keyboard('[tab]')
r.keyboard('[tab]')
r.keyboard('[enter]')

#browsing sesami
r.click('/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/div[@id="rfqTender_length"]/label/select')
r.keyboard('[down]')
r.keyboard('[down]')
r.keyboard('[down]')
r.keyboard('[enter]')
time.sleep(0.5)
r.click('/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/thead/tr/th[3]')
time.sleep(1)
#r.click('/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/thead/tr/th[8]')
r.click('//th[8]')
time.sleep(1)

#get data of all leads available
counting = r.count('/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/tbody/tr')
print(counting)

rfq_ref = [] #column 2
rfq_type = [] #column 3
rfq_category = [] #column 5
rfq_description = [] #column 6
rfq_close_date = [] #column 8

for n in range(1, counting+1):
    rfq_ref_line = r.read(f'(/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/tbody/tr/td[2])[{n}]')
    rfq_ref.append(rfq_ref_line)
    rfq_type_line = r.read(f'(/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/tbody/tr/td[3])[{n}]')
    rfq_type.append(rfq_type_line)
    rfq_category_line = r.read(f'(/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/tbody/tr/td[5])[{n}]')
    rfq_category.append(rfq_category_line)
    rfq_description_line = r.read(f'(/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/tbody/tr/td[6])[{n}]')
    rfq_description.append(rfq_description_line)
    rfq_close_date_line = r.read(f'(/html/body/table[@id="content"]/tbody/tr/td/table/tbody/tr/td/div[@id="listContainer"]/form[@id="RTPInviteForm"]/div[@id="rfqTender_wrapper"]/table[@id="rfqTender"]/tbody/tr/td[8])[{n}]')
    rfq_close_date.append(rfq_close_date_line)

#close browser and automatic logout
r.close()

# create dataframe and csv
dict = {'Ref': rfq_ref, 'Type': rfq_type, 'Category': rfq_category, 
        'Description': rfq_description, 'Closure': rfq_close_date}
df = pd.DataFrame(dict)

df.to_csv('sesami_latest_open.csv', index=None, sep=' ', mode='a')


