import os
import requests
import re
import pandas as pd
from . import download_sheet
import streamlit as st

currentDirectory = os.path.dirname(os.path.abspath(__file__))

def send_image_to_group_byUpload(imagePath, fileName, caption):
    url = f'{st.secrets["apiUrl"]}/waInstance{st.secrets["idInstance"]}/sendFileByUpload/{st.secrets["apiTokenInstance"]}'

    payload = {'chatId': st.secrets["groupId"],
    'caption': caption}
    files = [
    ('file', (fileName, open(imagePath,'rb'),'image/jpeg'))
    ]
    headers= {}

    response = requests.request("POST", url, headers = headers, data = payload, files = files)

    print(response.text.encode('utf8'))

def send_text_message_to_group(message):
    url = f'{st.secrets["apiUrl"]}/waInstance{st.secrets["idInstance"]}/sendMessage/{st.secrets["apiTokenInstance"]}'
    payload = f'{{\r\n\t\"chatId\": \"{st.secrets["groupId"]}\",\r\n\t\"message\": \"{message}\"\r\n}}'
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

def download_image(url, saveDirectory, saveName):
    # Ensure the save directory exists
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)

    # Extract file ID from the sharing URL
    file_id_match = re.search(r'/d/([^/]+)/', url)
    if not file_id_match:
        raise ValueError("Invalid Google Drive URL")
    file_id = file_id_match.group(1)
    # Create a direct download URL
    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(direct_url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if not content_type.startswith('image/'):
            raise ValueError(f"URL does not contain an image. Content-Type: {content_type}")
        
        # Create the full file path
        filePath = os.path.join(saveDirectory, saveName)
        with open(filePath, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {filePath}")
        return filePath
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def main(sheet_link):
    csv_file = 'output.csv'
    download_sheet.download_google_sheet_as_csv(sheet_link, csv_file)
    # Print the variables to verify
    df = pd.read_csv('output.csv')
    for x, row in df.iterrows():
        send_data_to_whatsapp(row)
        
def send_data_to_whatsapp(row):
    print(f"Graphics: {row['graphics']}")
    print(f"Time: {row['time']}")
    print(f"Uploading Date: {row['uploading date']}")
    print(f"Content - Text: {row['content - text']}")
    print(f"Identifier: {row['indentifier']}")
    print('---')

    caption = f"""
    identifier: {row['indentifier']}
    Text: {row['content - text']}
    Date: {row['uploading date']}
    Time:{row['time']}"""

    if row['graphics']:
        url = row['graphics']
        saveDirectory = os.path.join(currentDirectory, 'images')
        fileName = "image.jpeg"
        imagePath = download_image(url, saveDirectory, fileName)
        print('Image Dowloaded')            
        send_image_to_group_byUpload(imagePath, fileName, caption)
    else:
        send_text_message_to_group(caption)

if __name__ == '__main__':
    main("https://docs.google.com/spreadsheets/d/1szP9DLGeWxtQF7F_tVA3s79EjUA0BS1py-Vd5_RnxpE/edit?usp=drive_link")
