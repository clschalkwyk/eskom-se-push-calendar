from eskom import publish, sepush

ESKOM_LOCATION = 'eskme-14-sunningdalecityofcapetownwesterncape'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sepush.get_schedule(ESKOM_LOCATION)
    publish.publish_to_calendar()
