import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import pandas as pd
from .models import ScrapeData




# Scroll until "You've reached the end of the list." appears
def scroll_until_end(driver, max_attempts=30):
    feed_selector = 'div[role="feed"]'
    for attempt in range(max_attempts):
        driver.execute_script(f"document.querySelector('{feed_selector}').scrollBy(0, 1000)")
        time.sleep(1)
        try:
            end_text = driver.find_element(By.XPATH, "//p[contains(., \"You've reached the end of the list.\")]")
            if end_text:
                break
        except NoSuchElementException:
            # print("End text not found")
            continue

# Main Script
def run_scraper(keyword: str, starting_point_given: str) -> str:
    try:
        # Setup
        options = uc.ChromeOptions()
        options.headless = False
        driver = uc.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        final_data = {}
        
        # Clear db data before scraping
        ScrapeData.objects.all().delete()
        
        # Open Google Maps
        driver.get("https://www.google.com/maps")

        # Search with keyword
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        #Scroll
        scroll_until_end(driver)

        # Extract each result card
        results = driver.find_elements(By.CLASS_NAME, "Nv2PK")

        for card in results:
            # Name
            try:
                name = card.find_element(By.CLASS_NAME, "qBF1Pd").text
            except:
                name = "N/A"
                # print("Failed to fetch name")
            # Rating
            try:
                rating = card.find_element(By.CLASS_NAME, "MW4etd").text
            except:
                rating = "N/A"
                # print(f"Failed to fetch rating of {name}")
            # Review count
            try:
                if rating != "N/A":
                    review_count = card.find_element(By.CLASS_NAME, "UY7F9").text
                    review_count = review_count.strip("()")
                else:
                    review_count = "N/A"
            except:
                review_count = "N/A"
                # print(f"Failed to fetch review count of {name}")

            try:
                w4_blocks = card.find_elements(By.CLASS_NAME, "W4Efsd")
                if len(w4_blocks) >= 2:
                    # Extract category + phone from the first W4Efsd
                    category_spans = w4_blocks[1].find_elements(By.TAG_NAME, "span")
                    category = category_spans[0].text if len(category_spans) > 0 else "N/A"
                    # Extract phone from the second W4Efsd
                    try:
                        phone = w4_blocks[1].find_element(By.CLASS_NAME, "UsdlK").text
                    except:
                        phone = "N/A"
                        # print(f"Failed to fetch phone of {name}")
            except:
                category, phone = "N/A", "N/A"
                # print(f"Failed to fetch category and phone of {name}")
                
                
            # Opening status
            try:
                status_span = w4_blocks[3].find_elements(By.TAG_NAME, "span")
                status = status_span[2].text
            except:
                status = "N/A"
                # print(f"Failed to fetch status of {name}")

            # Store in dict
            final_data[name] = {
                "rating": rating,
                "review_count": review_count,
                "category": category,
                "phone": phone,
                "status": status,
                # Add placeholders for fields to be added later
                "address": "",
                "starting_point": "",
                "distance": "",
                "time_req": "",
                "location_url": ""
            }
            
        # Fetching address, distance and url
        # Search for each name
        for name in final_data.keys():
            search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
            search_box.clear()
            search_box.send_keys(name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # Handle if the suggestion box appears
            try:
                correction_div = driver.find_element(By.CLASS_NAME, "UsUSKc")
                if correction_div: 
                    try:
                        correction_button = correction_div.find_element(By.CSS_SELECTOR, "button.C9cOMe")
                        driver.execute_script("arguments[0].click();", correction_button)
                        print(f"Clicked the 'Search instead for...' button for {name}")
                        time.sleep(3) 
                    except :
                        print(f"failed to click on suggesion button for {name}")
            except:
                pass
            
            # If more than one result shows
            multi_result = driver.find_elements(By.CLASS_NAME, "Nv2PK")   
            # print(f"multi_result found for {name}")     
            if multi_result:
                for card in multi_result:
                    try:
                        name_div = card.find_element(By.CLASS_NAME, "qBF1Pd")
                        if name_div.text.strip().lower() == name.lower():
                            try:
                                link = card.find_element(By.CLASS_NAME, "hfpxzc")
                                driver.execute_script("arguments[0].click();", link)
                                # print(f"clicked for {name}")
                                time.sleep(3)
                            except:
                                print(f"failed to click on multiple results") 
                            break
                    except NoSuchElementException:
                        print(f"failed to find same name on multiple results")
                        continue                 

            # Extract address
            try:
                address_div_block = driver.find_elements(By.CLASS_NAME, "Io6YTe")
                address = address_div_block[0].text
            except:
                address = "N/A"
                print(f"Failed to fetch address of {name}")

            # Extract link
            # Click share button
            try:
                share_button = driver.find_element(By.XPATH, "//button[@aria-label='Share']")
                driver.execute_script("arguments[0].click();", share_button)
                time.sleep(2)
            except NoSuchElementException:
                print(f"Failed to find share button of {name}")
            # fetch location url
            try:
                input_element = driver.find_element(By.XPATH, "//input[@class='vrsrZe']")
                location_url = input_element.get_attribute("value")
            except NoSuchElementException:
                location_url = "N/A"
                print(f"Failed to fetch location url of {name}")
            # Close share window    
            try:
                close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1)
            except NoSuchElementException:
                print(f"failed to find share close button of {name}")
                
            # Finding Distance
            # Click direction button
            try:
                direction_button = driver.find_element(By.XPATH, "//button[@aria-label='Directions']")
                driver.execute_script("arguments[0].click();", direction_button)
                time.sleep(2)
            except NoSuchElementException:
                print(f"Failed to find direction button of {name}")
            # Selecting driving using car
            try:
                driving_button = driver.find_element(By.XPATH, "//button[@data-tooltip='Driving']")
                driver.execute_script("arguments[0].click();", driving_button)
                time.sleep(1)
            except NoSuchElementException:
                print(f"failed to click drive button of {name}")
            # Search starting point input
            # Wait for both input fields to appear
            input_boxes = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "tactile-searchbox-input"))
            )
            if len(input_boxes) >= 1:
                start_input_box = input_boxes[0]  # First input is starting point
                start_input_box.clear()
                start_input_box.send_keys(starting_point_given)
                start_input_box.send_keys(Keys.RETURN)
            else:
                print("Starting point input box not found.")
            # Destination
            if len(input_boxes) >= 2:
                destination_input_box = input_boxes[1]  # Second one is destination
                if destination_input_box.get_attribute("aria-label") == "Choose destination...":
                    try:    
                        destination_input_box.clear()
                        destination_input_box.send_keys(name)
                        destination_input_box.send_keys(Keys.RETURN)
                    except :
                        print(f"destination input already filled")
            # Wait for loading            
            time.sleep(2)
            
            # Fetching distance and time
            try:
                starting_point = start_input_box.get_attribute("value")
                time_req = driver.find_element(By.CLASS_NAME, "Fk3sm").text
                distance = driver.find_element(By.CLASS_NAME, "ivN21e").text
                # Converting distance into km if it is in meter
                if "km" in distance:
                    distance = float(distance.replace("km", "").strip())
                elif "m" in distance:
                    distance_in_meters = float(distance.replace("m", "").strip())
                    distance = round(distance_in_meters / 1000, 3)
                else:
                    distance = 0.0
            except:
                starting_point, time_req, distance = "N/A", "N/A", 0.0
                print(f"failed to fetch starting point, distance and time of {name}")
            # Closing direction window
            try:
                direction_close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close directions']")
                driver.execute_script("arguments[0].click();", direction_close_button)
            except NoSuchElementException:
                print(f"failed to find direction close button of {name}")
                
            # Storing remaining data into dict
            final_data[name]["starting_point"] = starting_point
            final_data[name]["address"] = address
            final_data[name]["distance"] = distance
            final_data[name]["time_req"] = time_req
            final_data[name]["location_url"] = location_url
            
            # Save to database after each entry
            ScrapeData.objects.create(
                keyword = keyword,
                name=name,
                rating=final_data[name]["rating"],
                review_count=final_data[name]["review_count"],
                category=final_data[name]["category"],
                address=final_data[name]["address"],
                phone=final_data[name]["phone"],
                status=final_data[name]["status"],
                starting_point_given = starting_point_given,
                starting_point=final_data[name]["starting_point"],
                distance=final_data[name]["distance"],
                time_req=final_data[name]["time_req"],
                location_url=final_data[name]["location_url"] 
            )
        
        driver.quit()
        print("Scrapping succesfully completed")
    except:
        print("Session expired or browser was closed")
        pass
    
    
def sorting_and_saving(keyword):
        # Sorting final data by distance accending order
    sorted_data = sorted(final_data.items(), key=lambda x: float(x[1]["distance"]))

    # Save final data into csv
    safe_keyword = keyword.replace(" ", "_")
    csv_file_name = f"google_maps_{safe_keyword}_final_data.csv"
    with open(csv_file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "rating", "review_count", "category", "address", "phone", "status", "starting_point", "distance", "distance_unit", "time_req", "location_url"])
        for name, info in sorted_data:
            writer.writerow([
                name,
                info["rating"], info["review_count"], info["category"], info["address"], info["phone"], info["status"],
                info["starting_point"], info["distance"], info["time_req"], info["location_url"]
            ])
    print(f"Final csv data saved in {csv_file_name}")
            
    # Save as excel
    excel_file_name = f"google_maps_{safe_keyword}_final_data.xlsx"
    df = pd.DataFrame([
        [
            name, info["rating"], info["review_count"], info["category"], info["address"],
            info["phone"], info["status"], info["starting_point"],
            info["distance"], info["time_req"], info["location_url"]
        ] for name, info in sorted_data
    ], columns=[
        "name", "rating", "review_count", "category", "address",
        "phone", "status", "starting_point", "distance", "time_req", "location_url"
    ])
    df.to_excel(excel_file_name, index=False)
    print(f"Final excel data saved in {excel_file_name}")
    