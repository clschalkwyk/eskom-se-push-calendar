import math
import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

LICENSE_KEY=os.getenv('LICENSE_KEY',None)
ESKOM_LOCATION=os.getenv('ESKOM_LOCATION',None)
CACHE_FILENAME='schedule.json'

headers={
    'token': LICENSE_KEY
}


def cached_file_age_check():
    # no cache file check
    if not os.path.exists(CACHE_FILENAME):
        print("No cached schedule exists.")
        return 0

    # Get the time of the last access time of the file
    last_modified_time = os.path.getmtime(CACHE_FILENAME)
    current_time = time.time()
    file_age_seconds = current_time - last_modified_time
    # Convert file age from seconds to minutes
    file_age_minutes = file_age_seconds / 60
    return math.ceil(file_age_minutes)

def _get_schedule(area):
    if area:
        print(f"Fetching schedule for {area}")
        url =f"https://developer.sepush.co.za/business/2.0/area?id={area}"
        res = requests.get(url, headers=headers)
        print(res.text)
        try:
            if res.status_code == 200:
                if res.json().get('error'):
                    print(res.json().get('error'))
                else:
                    print("api call status 200")
                    with open(CACHE_FILENAME,'w') as fp:
                        fp.write(res.text)
                        print("Schedule saved.")
                    return res.json()

        except:
            print("Unable to pull schedule, try again later")

    print("Eskom location not set.")


def get_schedule(area):
    # fetch schedule data from EskomSePush API
    cache_file_age = cached_file_age_check()
    print(f'Current cache age: {cache_file_age} minutes.')

    if cache_file_age > 15:
        print("Remove cached schedule file")
        os.unlink(CACHE_FILENAME)
        return _get_schedule(area)

    if cache_file_age == 0:
        return _get_schedule(area)


if __name__ == "__main__":
    if ESKOM_LOCATION:
        get_schedule(ESKOM_LOCATION)
    else:
        print('Eskom location not set..')
