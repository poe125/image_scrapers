import requests
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def main():
    """
    this is the description of the main function
    """
    
    ############## URL ##############
    url = "" 
    key = "cdn"
    
    #get initiators
    image_urls = request_initiators(url)
    cdn_images = clean_initiators(image_urls, key)
    
    #download images as jpg using the initiators
    download_images(cdn_images)

    #make it into pdf file
    image_paths = []
    i=0
    for _ in cdn_images:
        image_paths.append(f"images/{i}.jpg")
        i += 1
        
    ############## THE DEFINITE PATH TO YOUR OUTPUT ##############
    outfile = ""
    images_to_pdf(image_paths, outfile)

    #clean the images in the file
    count=0
    for _ in cdn_images:
        print(f"for {count} in cdn_images: clean images")
        image_path = f"images/{count}.jpg"
        count += 1
        clean_images(image_path)
    
    
def request_initiators(url):
    # Initialize the WebDriver (in this example, using Chrome)
    driver = webdriver.Chrome()
    driver.get(url)

    # Perform some interactions
    try:
        # Wait for an element to be clickable (for demonstration purposes)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )

        # Perform some action (e.g., typing into a search box)
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        
        image_urls = [img.get_attribute("src") for img in img_elements]
        
        return image_urls
    
    finally:
        # Close the WebDriver session
        driver.quit()
    
def clean_initiators(image_urls, key):
    cdn_image_urls = [img_url for img_url in image_urls if key in img_url]
    for image in cdn_image_urls:
        print(image)
    return cdn_image_urls

def download_images(image_urls):
    os.makedirs("images", exist_ok=True)
    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"images/{i}.jpg", "wb") as f:
                f.write(response.content)
                print(f"Downloaded image {i}")
               
def clean_images(file_path):
    print("inside clean images")
    if os.path.exists(file_path):
        print("cleaning images")
        # Delete the file
        os.remove(file_path)

def images_to_pdf(image_paths, output_pdf):
    # Create a canvas
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Get the dimensions of the letter-sized page
    width, height = letter

    # Loop through each image path
    for image_path in image_paths:
        # Open the image using PIL
        img = Image.open(image_path)

        # Calculate scaling factor to fit the image within the page
        scaling_factor = min(width / img.width, height / img.height)

        # Calculate new dimensions of the image
        new_width = img.width * scaling_factor
        new_height = img.height * scaling_factor

        # Calculate position to center the image on the page
        x_offset = (width - new_width) / 2
        y_offset = (height - new_height) / 2

        # Add the image to the canvas
        c.drawImage(image_path, x_offset, y_offset, new_width, new_height)

        # Add a new page for the next image
        c.showPage()
    c.save()
    
main()