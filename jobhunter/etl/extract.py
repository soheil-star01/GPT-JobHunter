
import logging
import json
import datetime
import pprint
import os
import yaml
import time
from tqdm import tqdm
from utils.search_linkedin_jobs import search_linkedin_jobs

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(level=logging.DEBUG)

FILE_PATH="/Users/jjespinoza/Documents/jobhunter"

# Get the absolute path of the config file
config_file = f"{FILE_PATH}/jobhunter/config.yaml"

# Open the configuration file
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

def save_raw_data(data, source):
    """
    Saves a list of dictionaries to a JSON file locally in the ../data/raw directory.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    file_path = os.path.join(FILE_PATH, "data", "raw", f"{source}-{timestamp}.json")
    with open(file_path, "w") as f:
        json.dump(data, f)
    logging.debug("Saved data to %s", file_path)
    return None

def get_all_jobs(search_term, location, pages):
    all_jobs = []
    for page in range(0,pages):
        time.sleep(.1)
        jobs = search_linkedin_jobs(
                search_term=search_term, location=location, page=page
                )
        all_jobs.append(jobs)
    return all_jobs

def save_jobs(search_term, location, pages):
    jobs = get_all_jobs(search_term=search_term, location=location, pages=pages)
    for job in jobs:
        for item in job:
            save_raw_data(item, source="linkedinjobs")

def extract():
    positions = config['positions']
    locations = config['locations']
    for position in tqdm(positions):
        for location in locations:
            save_jobs(search_term=position, location=location, pages=20)

    pass

if __name__ == "__main__": 
    extract()



