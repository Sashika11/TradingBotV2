from datetime import datetime, time as dtime
import pytz

def valid_session():
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz).time()

    london_open = dtime(3,0)
    london_close = dtime(7,0)
    ny_open = dtime(8,0)
    ny_close = dtime(12,0)

    return (london_open <= now <= london_close) or (ny_open <= now <= ny_close)
