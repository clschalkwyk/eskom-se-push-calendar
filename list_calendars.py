from eskom import google
from tabulate import tabulate
def list_calendars():

    service = google.login()

    # Call the Calendar API
    print('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])


    if not calendars:
        print('No calendars found.')
    else:
        print('Calendars:')
        headers = ['Id', 'Summary']
        found=[]

        for calendar in calendars:
            summary = calendar['summary']
            id = calendar['id']
            found.append([id, summary])

        print(tabulate(found, headers=headers, tablefmt='grid'))

if __name__ == '__main__':
    list_calendars()
