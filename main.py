import requests
from bs4 import BeautifulSoup
import webbrowser
import zstd

GET_URL = "https://verify.bmdc.org.bd"
POST_URL = "https://verify.bmdc.org.bd/regfind"
POST_HEADERS = {
     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
     "Referer": "https://verify.bmdc.org.bd/",
     "Origin": "https://verify.bmdc.org.bd",
     "Content-Type": "application/x-www-form-urlencoded",
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
     "Accept-Encoding": "gzip, deflate, br, zstd",
     "Accept-Language": "en-US,en;q=0.7"
}

# Creating a Session
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
})

# Requesting the HomePage
get_resp = session.get("https://verify.bmdc.org.bd")

# Making the soup
soup = BeautifulSoup(get_resp.text, features="html.parser")

# Extracting captcha
captcha_url = soup.find_all("img")[1].get("src")
webbrowser.open(captcha_url)
captcha = input("Please enter the captcha value: ")

# Complete constructing payload
action_flag = soup.find("input", {"id": "action_flag"}).get("value")
action_key = soup.find("input", {"id": "action_key"}).get("value")
bmdc_token = soup.input.get("value")

reg_no = input("Please enter the registration number: A-")

PAYLOAD = {"reg_ful_no": reg_no, "reg_student": 1, "captcha_code": captcha, "action_key": action_key, "action_flag": action_flag, "bmdckyc_csrf_token": bmdc_token}

# Launching the payload
post_resp = session.post(POST_URL, headers=POST_HEADERS, data=PAYLOAD)
if post_resp.ok == True:
    print("Received BMDC info. Decoding - please wait...")
    soup2 = BeautifulSoup(zstd.decompress(post_resp.content), features="html.parser")
    doc_info = {label.text:value.text for (label, value) in list(zip(soup2.find_all("label"), soup2.find_all("h6")))}
    doc_info["name"] = soup2.find_all("h3")[-1].text
    print(f"Name: {doc_info['name']}")
    for key in doc_info:
        if key != "name":
            print(f"{key}: {doc_info[key]}")
else:
    print("Error: Could not retrieve data!")    
    
