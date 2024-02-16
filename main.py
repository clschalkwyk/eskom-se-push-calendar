from eskom import publish, sepush
from dotenv import load_dotenv
import os
load_dotenv()

ESKOM_LOCATION = os.getenv('ESKOM_LOCATION', None)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if ESKOM_LOCATION:
        sepush.get_schedule(ESKOM_LOCATION)
        publish.publish_to_calendar()
    else:
        print("Eskom location not set!")
