import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import csv
import pandas as pd

# Setup
options = uc.ChromeOptions()
options.headless = False
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 15)

final_data = {}

def fetch_business_data():
    # Open Google Maps
    driver.get("https://www.google.com/maps")

    # Search with keyword
    search_keyword = "pg near chevayoor"
    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    search_box.clear()
    search_box.send_keys(search_keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

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
                continue

    scroll_until_end(driver)

    # Extract each result card
    results = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    for card in results:
        # Name
        try:
            name = card.find_element(By.CLASS_NAME, "qBF1Pd").text
        except:
            name = "N/A"
        # Rating
        try:
            rating = card.find_element(By.CLASS_NAME, "MW4etd").text
        except:
            rating = "N/A"
        # Review count
        try:
            if rating != "N/A":
                review_count = card.find_element(By.CLASS_NAME, "UY7F9").text
                review_count = review_count.strip("()")
            else:
                review_count = "N/A"
        except:
            review_count = "N/A"

        try:
            w4_blocks = card.find_elements(By.CLASS_NAME, "W4Efsd")
            category, phone = "N/A", "N/A"

            if len(w4_blocks) >= 2:
                # Extract category + address from the first W4Efsd
                category_spans = w4_blocks[1].find_elements(By.TAG_NAME, "span")
                category = category_spans[0].text if len(category_spans) > 0 else "N/A"

                # Extract phone from the second W4Efsd
                try:
                    phone = w4_blocks[1].find_element(By.CLASS_NAME, "UsdlK").text
                except:
                    phone = "N/A"
        except:
            category, phone = "N/A", "N/A"
            
        # Opening status
        try:
            status_span = w4_blocks[3].find_elements(By.TAG_NAME, "span")
            status = status_span[2].text
        except:
            status = "N/A"

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
        time.sleep(1)
        
        # If more than one result shows
        multi_result = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        clicked = False
        
        if multi_result:
            for card in multi_result:
                try:
                    name_div = card.find_element(By.CLASS_NAME, "qBF1Pd")
                    if name_div.text.strip().lower() == name.lower():
                        try:
                            link = card.find_element(By.CLASS_NAME, "hfpxzc")
                            driver.execute_script("arguments[0].click();", link)
                            clicked = True
                        except Exception as e:
                            print(e) 
                        break
                except NoSuchElementException:
                    print(NoSuchElementException)
                    continue                 

        # Extract address
        if clicked:
            try:
                # Wait for the detailed view to load — look for the address class
                address_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "Io6YTe"))
                )
                address = address_element.text
            except TimeoutException:
                address = "N/A"
        else:
            try:
                address_div_block = driver.find_elements(By.CLASS_NAME, "Io6YTe")
                address = address_div_block[0].text
            except:
                address = "N/A"

        # Extract link
        # Click share button
        try:
            share_button = driver.find_element(By.XPATH, "//button[@aria-label='Share']")
            driver.execute_script("arguments[0].click();", share_button)
            time.sleep(1)
        except NoSuchElementException:
            print(NoSuchElementException)
        # fetch location url
        try:
            input_element = driver.find_element(By.XPATH, "//input[@class='vrsrZe']")
            location_url = input_element.get_attribute("value")
        except NoSuchElementException:
            location_url = "N/A"
        # Close share window    
        try:
            close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
            driver.execute_script("arguments[0].click();", close_button)
            time.sleep(1)
        except NoSuchElementException:
            print(NoSuchElementException)
            
        # Finding Distance
        # Click direction button
        try:
            direction_button = driver.find_element(By.XPATH, "//button[@aria-label='Directions']")
            driver.execute_script("arguments[0].click();", direction_button)
            time.sleep(1)
        except NoSuchElementException:
            print(NoSuchElementException)   
        # Selecting driving using car
        try:
            driving_button = driver.find_element(By.XPATH, "//button[@data-tooltip='Driving']")
            driver.execute_script("arguments[0].click();", driving_button)
            time.sleep(1)
        except NoSuchElementException:
            print(NoSuchElementException)
        # Search starting point input
        my_location = 'chevayur'
        start_input_box = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@aria-label='Choose starting point, or click on the map...']")
            )
        )
        start_input_box.clear()
        start_input_box.send_keys(my_location)
        start_input_box.send_keys(Keys.RETURN)
        time.sleep(1)
        # Fetching distance and time
        try:
            starting_point = start_input_box.get_attribute("value")
            time_req = driver.find_element(By.CLASS_NAME, "Fk3sm").text
            distance = driver.find_element(By.CLASS_NAME, "ivN21e").text
            # Converting distance into km if it is in meter
            if "m" in distance.lower() and "km" not in distance.lower():
                numeric_value = float(distance.lower().replace("m", "").replace(",", "").strip())
                distance = round(numeric_value / 1000, 3)
        except:
            starting_point, time_req, distance = "N/A", "N/A", "N/A"
        # Closing direction window
        try:
            direction_close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close directions']")
            driver.execute_script("arguments[0].click();", direction_close_button)
            time.sleep(1)
        except NoSuchElementException:
            print(NoSuchElementException)
            
        # Storing remaining data into dict
        final_data[name]["starting_point"] = starting_point
        final_data[name]["address"] = address
        final_data[name]["distance"] = distance
        final_data[name]["time_req"] = time_req
        final_data[name]["location_url"] = location_url
    
    # Sorting final data by distance accending order
    sorted_data = sorted(final_data.items(), key=lambda x: float(x[1]["distance"]))

    # Save final data into csv
    safe_keyword = search_keyword.replace(" ", "_")
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
    
    
    driver.quit()
    print("Scrapping succesfully completed")


# fetch_business_data()









# Fetching address and url
# Load already fetched data
names = []

with open("google_maps_dance_places.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        names.append(row["name"])


# Open Google Maps
driver.get("https://www.google.com/maps")



# Search for each name
for name in names:
    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    search_box.clear()
    search_box.send_keys(name)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(5)
    
    # Handle if the suggestion box appears
    correction_div = driver.find_element(By.CLASS_NAME, "UsUSKc")
    if correction_div: 
        try:
            correction_button = correction_div.find_element(By.CSS_SELECTOR, "button.C9cOMe")
            driver.execute_script("arguments[0].click();", correction_button)
            print("Clicked the 'Search instead for...' button")
            time.sleep(2) 
        except :
            print("failed to click on suggesion button")
    
    # If more than one result shows
    multi_result = driver.find_elements(By.CLASS_NAME, "Nv2PK")    
    if multi_result:
        for card in multi_result:
            try:
                name_div = card.find_element(By.CLASS_NAME, "qBF1Pd")
                if name_div.text.strip().lower() == name.lower():
                    try:
                        link = card.find_element(By.CLASS_NAME, "hfpxzc")
                        driver.execute_script("arguments[0].click();", link)
                    except: 
                        print("Failed to click on multiple link")
                    break
            except NoSuchElementException:
                print(NoSuchElementException)
                continue                 

    # Extract address
    data = []

    # if clicked:
    #     try:
    #         # Wait for the detailed view to load — look for the address class
    #         address_div_block = WebDriverWait(driver, 5).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, "Io6YTe"))
    #         )
    #         address = address_div_block.text
    #         print(address)
    #     except TimeoutException:
    #         address = "N/A"
    # else:
    #     try:
    #         address_div_block = driver.find_elements(By.CLASS_NAME, "Io6YTe")
    #         address = address_div_block[0].text
    #     except:
    #         address = "N/A"

    # Extract link
    # Click share button
    try:
        share_button = driver.find_element(By.XPATH, "//button[@aria-label='Share']")
        driver.execute_script("arguments[0].click();", share_button)
        time.sleep(1)
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
        time.sleep(1)
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
    my_location = "nit calicut"
    input_boxes = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "tactile-searchbox-input"))
    )
    if len(input_boxes) >= 1:
        start_input_box = input_boxes[0]  # First input is starting point
        start_input_box.clear()
        start_input_box.send_keys(my_location)
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
                time.sleep(2)
            except :
                print(f"destination input already filled")
        
        else:
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
    
    
    print(name, "|", starting_point, "|", time_req, "|", distance, "|", location_url)
    # print(search_keyword, "|", address, "|", location_url)
    # data.append([search_keyword, address, location_url])

driver.quit()
print("Scrapping Completed")

