from spreadsheet import get_updates
from emailing import send_update

if __name__ == '__main__':
    updates = get_updates()
    print(len(updates))
    # send_update(updates)
