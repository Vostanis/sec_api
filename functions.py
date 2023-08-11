import datetime
import json
import os
import requests
import zipfile


# General Parameters
today       = datetime.date.today()

# Directory Shortcuts
home_dir    = os.getcwd()
zip_dir     = home_dir + "\\zip"
cf_dir     = home_dir + "\\companyfacts"
sbms_dir   = home_dir + "\\submissions"
tikr_dir   = home_dir + "\\tickers"

# General Functions
def clear_screen(): os.system('cls')


# call url; Mozilla user_agent browser by default
def load_url(url, dir=home_dir, user_agent="Mozilla/5.0"):

    request = requests.get(url, headers={"User-Agent": user_agent})
    ### init error checks
    request.raise_for_status() # HTTPError if fails

    ### Compatible File Extensions
    # .json
    if url.endswith(".json"):
        return request.json()
        # return json.loads(request.text())
    
    # .zip
    if url.endswith(".zip"):
        if not os.path.exists(dir):
            raise ValueError("No such directory exists.")
        else:
            print("Writing .zip file to dir ...")
            file_base_name = os.path.basename(url)
            file_path = os.path.join(dir, file_base_name)
            with open(file_path, "wb") as path:
                path.write(request.content)

    ### Error Handling
    # unrecgonised .<file_extension>
    else:
        raise ValueError("Unrecognised file type; this method is only compatible with following file extension types:\n\t.json\n\t.zip\n")


# call file path
def load_file(path):
    # .json
    if path.endswith(".json"):
        with open(path, 'r') as data:
            return json.load(data)
        
    ### Error Handling
    # unrecgonised .<file_extension>
    else:
        raise ValueError("Unrecognised file type; this method is only compatible with following file extension types:\n\t.json\n")
        

# Open the zip file
def unzip(file_path, destination_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Extract all files to a specific directory
        file_name = os.path.basename(file_path)
        print(f"Unzipping {file_name} to {destination_path}")
        zip_ref.extractall(destination_path)