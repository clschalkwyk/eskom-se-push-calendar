from . import google
import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# for your primary calendar on Google [default = primary]
CALENDAR_ID=os.getenv('CALENDAR_ID','primary')


def collect_events():
    schedules = json.load(open('schedule.json'))
    schedule_name = schedules.get('info').get('name')
    schedule_region = schedules.get('info').get('region')
    found = []

    for event in schedules.get('events'):
        evt = {
            'summary': f'[ESP] {schedule_name}',
            'description': schedule_region,
            'start': {
                'dateTime': event['start'],
                # 'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': event['end'],
                # 'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'colorId': 4
        }
        found.append(evt)
    return found

def publish_to_calendar():
    service = google.login()

    # Call the Calendar API
    now = datetime.datetime.now(datetime.UTC).isoformat()
    # datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = (service
                     .events()
                     .list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute())
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    for event in events:
        if str(event['summary'])[0:5] == '[ESP]':
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            event_id = event['id']
            service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()

    events = collect_events()
    if events.__len__() > 0:
        for evt in events:
            event = service.events().insert(calendarId=CALENDAR_ID, body=evt).execute()
            print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    publish_to_calendar()
