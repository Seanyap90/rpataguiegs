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
print("logging in")
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
print("browsing and filtering")
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
time.sleep(3)

#View your own opportunities from open opportunities
print("view your own opportunities")
something = r.read('/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td/ul/li[2]/ul/li[1]/a')
print(something)
r.click('/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td/ul/li[2]/a')
r.click('/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td/ul/li[2]/ul/li[1]/a')
time.sleep(5)

#access your latest open opportunities
leadcount = r.count('/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr')
print(leadcount)
rfq_ref_2 = []
description_2 = []
closing_period = []
status = []
rfq_url = []
requestor = []
rfq_email = []
rfq_contact = []
rfq_pdf_url = []
nda = []

print("acccess individual details")
for n in range(1, leadcount+1):
    #Access individual opportunities from main table
    rfq_ref_2_line = r.read(f'(/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr/td[2])[{n}]')
    print(rfq_ref_2_line)
    rfq_ref_2.append(rfq_ref_2_line)
    description_2_line = r.read(f'(/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr/td[3])[{n}]')
    description_2.append(description_2_line)
    closing_period_line = r.read(f'(/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr/td[6])[{n}]')
    closing_period.append(closing_period_line)
    status_line = r.read(f'(/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr/td[7])[{n}]')
    status.append(status_line)
    rfq_url_line = r.read(f'(/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr/td[11]/a/@href)[{n}]')
    rfq_url.append(rfq_url_line)
    
    # browse further details about that opportunity
    r.click(f'(/html/body/table/tbody/tr[2]/td/center/div[2]/div/table/tbody/tr/td[11]/a)[{n}]')
    
    if r.present('NON-DISCLOSURE AGREEMENT') == True:
        #check whether NDA has been initiated
        nda_line = 'NDA not signed'
        nda.append(nda_line)
        requestor_line = {0}
        requestor.append(requestor_line)
        rfq_email_line = {0}
        rfq_email.append(rfq_email_line)
        rfq_contact_line = {0}
        rfq_contact.append(rfq_contact_line)
        rfq_pdf_url_line = {0}
        rfq_pdf_url.append(rfq_pdf_url_line)
        r.click('Source Key')
        r.click('View ITQ/ITT/RFI/PQ/RFQ')
    else:
        requestor_line = r.read('/html/body/table/tbody/tr[2]/td/center/div[2]/form/table[1]/tbody/tr[18]/td[2]')
        requestor.append(requestor_line)
        rfq_email_line = r.read('/html/body/table/tbody/tr[2]/td/center/div[2]/form/table[1]/tbody/tr[20]/td[2]')
        rfq_email.append(rfq_email_line)
        rfq_contact_line = r.read('/html/body/table/tbody/tr[2]/td/center/div[2]/form/table[1]/tbody/tr[21]/td[2]')
        rfq_contact.append(rfq_contact_line)
        rfq_pdf_url_line = r.read('/html/body/table/tbody/tr[2]/td/center/div[2]/form/table[3]/tbody/tr[4]/td[5]/a/@href')
        rfq_pdf_url.append(rfq_pdf_url_line)
        
        #go back to main page
        r.click('/html/body/table/tbody/tr[2]/td/center/div[1]/a[1]')
	

#close and auto logout
print("logout and close browser")
r.close()

print("to csv")
dict = {'RFQ REF': rfq_ref_2, 'DESCRIPTION': description_2, 'CLOSING': closing_period,
        'STATUS': status, 'RFQ URL': rfq_url, 'REQUESTOR': requestor, 'CONTACT EMAIL': rfq_email,
        'CONTACT EMAIL': rfq_contact, 'PDF': rfq_pdf_url}   
df2 = pd.DataFrame(dict)

df2.to_csv('sesami_your_open.csv', index=None, sep=' ', mode='a')
