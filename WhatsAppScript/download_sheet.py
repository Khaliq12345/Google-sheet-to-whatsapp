import requests

def download_google_sheet_as_csv(sharing_link, output_file):
    # Extract file ID from the sharing link
    file_id = sharing_link.split('/d/')[1].split('/')[0]
    
    # Construct the download URL for the CSV format
    download_url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv'
    
    # Send a request to the download URL
    response = requests.get(download_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to a CSV file
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded the Google Sheet as {output_file}')
    else:
        print(f'Failed to download the Google Sheet. HTTP status code: {response.status_code}')

# sheet_link = 'https://docs.google.com/spreadsheets/d/15_3YOJ7b1OUMHRvUJFWxJEi_YSIx_jpKZXQZ-en0VkQ/edit?usp=sharing'
# csv_file = 'output2.csv'
# download_google_sheet_as_csv(sheet_link, csv_file)