#import libraries

from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime
from google.colab import files

#Connecting with the website


url = 'https://techcrunch.com/2024/04/30/sams-clubs-ai-powered-exit-tech-reaches-20-of-stores/'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "close"
}

page = requests.get(url, headers=headers)
soup1 = BeautifulSoup(page.content, "html.parser")

print(soup1) #prints all of the html data of the website

#better format
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

print(soup2)


# **Scraping** 

1] scraping text data

def scrape_article(url):
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Extracting the title of the article
            title_element = soup.find('h1')
            if title_element:
                article_title = title_element.get_text(strip=True)
                print("Title of the article:", article_title)
            else:
                print("Oops! Couldn't find the title. Setting it as 'N/A'.")
                article_title = "N/A"

            # extracting paragraphs for the content
            paragraphs = soup.find_all('p')
            if paragraphs:
                article_content = "\n".join([para.get_text(strip=True) for para in paragraphs])
                print("\nFull article content:\n")
                print(article_content)

                article_summary = article_content[:200] + "..." if len(article_content) > 200 else article_content
            else:
                print("No paragraphs found! Setting summary and content to 'N/A'.")
                article_summary = "N/A"
                article_content = "N/A"

            # Capturing today's date to log when we scraped the article
            today_date = datetime.now().strftime("%Y-%m-%d")

            
            
            print("\n🌟🎉 Scraping Success! 🎉🌟")
            print(f"Title: {article_title}\n")
            print(f"Summary: {article_summary}\n")
            print(f"Scraped on: {today_date}\n")

            # store the data and write it in a CSV file
            csv_filename = 'TechCrunch_SamsClubAI.csv'

            with open(csv_filename, 'a+', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(['Title', 'Summary', 'Full Content', 'Date'])
                writer.writerow([article_title, article_summary, article_content.replace('\n', ' ').replace('"', '""'), today_date])

            print(f"💾 Data saved to {csv_filename}!")

            # Download the CSV file 
            files.download(csv_filename)

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"😬 Uh-oh! An error occurred: {e}")

scrape_article(url)



scraping image data

from IPython.display import Image, display

def scrape_images(url):
    response = requests.get(url)  
    soup = BeautifulSoup(response.content, "html.parser")

   
    images = soup.find_all('img')

    for img in images:
        img_url = img.get('src') 
        if img_url: 
            if img_url.startswith('http'):  
                display(Image(url=img_url))  
            else:
                print("Image URL not valid:", img_url)  
        





scrape_images(url)

