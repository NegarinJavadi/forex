import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt

logging.basicConfig(level=logging.DEBUG)

data_keys = [
    'pair_name',
    'S1',
    'S2',
    'S3',
    'Pivot Points',
    'R1',
    'R2',
    'R3'
]

def get_data_object(driver, pair_id, time_frame):
    data = {}
    data['pair_id'] = pair_id
    data['time_frame'] = time_frame
    data['updated'] = dt.datetime.now(dt.timezone.utc)
    
    selectors = {
        'pair_name': '.pair-name',  
        'S1': '.s1',
        'S2': '.s2',
        'S3': '.s3',
        'Pivot Points': '.pivot',
        'R1': '.r1',
        'R2': '.r2',
        'R3': '.r3'
    }
    
    for key in data_keys:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selectors[key]))
            )
            data[key] = element.text.strip()
        except Exception as e:
            logging.error(f"Error fetching {key}: {e}")
            data[key] = None
    
    return data

def scrape_investing_com(pair_id, time_frame):
    url = f"https://www.investing.com/technical/Service/GetStudiesContent?action=get_studies&pair_ID={pair_id}&time_frame={time_frame}"
    logging.info(f"Fetching URL: {url}")
    options = webdriver.FirefoxOptions()  
    options.add_argument('--headless')

    
    driver_path = "/path/to/geckodriver"
    
    try:
        driver = webdriver.Firefox(executable_path=driver_path, options=options)
        driver.set_page_load_timeout(60)  
    except Exception as e:
        logging.error(f"Failed to start WebDriver: {e}")
        return {}

    try:
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pair-name")))
        data = get_data_object(driver, pair_id, time_frame)
    except Exception as e:
        logging.error(f"Error while scraping data for pair_id {pair_id}, time_frame {time_frame}: {e}")
        logging.error(driver.page_source)
        data = {}
    finally:
        driver.quit()

    return data

def investing_com():
    pair_id = 1  
    time_frame = 3600  
    logging.info(f"Fetching data for pair_id: {pair_id}, time_frame: {time_frame}")
    data = scrape_investing_com(pair_id, time_frame)
    if data:
        logging.info(data)
    else:
        logging.info("No data found")

investing_com()


'''
def investing_com():
    all_data = []
    for pair_id in range(1, 12):
        for time_frame in [3600, 86400]:
            print(f"Fetching data for pair_id: {pair_id}, time_frame: {time_frame}")
            data = scrape_investing_com(pair_id, time_frame)
            if data:
                all_data.append(data)
            time.sleep(0.5)
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(all_data)
    print(df)

investing_com()
'''






