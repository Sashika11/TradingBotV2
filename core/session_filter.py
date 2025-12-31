from datetime import datetime
import pytz

def valid_session():
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz).time()
    if (now >= datetime.strptime('03:00','%H:%M').time() and now <= datetime.strptime('07:00','%H:%M').time()) or \
       (now >= datetime.strptime('08:00','%H:%M').time() and now <= datetime.strptime('12:00','%H:%M').time()):
        return True
    return False
