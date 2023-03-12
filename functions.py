import datetime
import json
import os
import requests
import zipfile


# General Parameters
home_dir    = os.getcwd()
db_dir      = home_dir + "\\db"
zip_dir     = home_dir + "\\zip"
today       = datetime.date.today()


# General Functions
def clear_screen():         os.system('cls')
def file_name(file_path):   os.path.basename(file_path)[0]


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
            raise ValueError("No such directory exists")
        else:
            print("Writing .zip file to dir ...")
            file_base_name = os.path.basename(url)
            with open(dir + "\\" + file_base_name, "wb") as path:
                path.write(request.content)

    ### Error Handling
    # unrecgonised .<file_extension>
    else:
        raise ValueError("Unrecognised file type; this method is only compatible with following file extension types:\n\t.json\n\t.zip\n")


# Download bulk .zip of all SEC submission files and company facts
# # If the file already exists & is modified today: do not redownload
def download_gateway(file_path, download):

    file_name = file_name(file_path)
    
    if os.path.exists(file_path) and (datetime.date.fromtimestamp(os.path.getmtime(file_path)) == today):
        pass
    else:
        download_dir = os.path.dirname(file_path)
        if not os.path.exists(download_dir):
            print("Making directory ...")
            os.makedirs(download_dir)
        print(f"Downloading {file_name} ...")
        return download

    # if os.path.exists(home_dir + "\\companyfacts.zip") and (datetime.date.fromtimestamp(os.path.getmtime("companyfacts.zip")) == today): 
    #     print("Company fact data has already been downloaded today - passing request ...")
    #     pass
    # else:
    #     print("Requesting url data ...")
    #     bulk_facts          = load_url("https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip")


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
        zip_ref.extractall(destination_path)