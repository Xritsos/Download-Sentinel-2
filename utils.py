import datetime

def dt_to_shortstr(dt_obj):
    """
    Take a datetime object and convert it to string keeping only year, month, date
    
    Args:
        dt_obj (datetime.datetime):
    
    Returns:
        str with a format 'YYYY-mm-dd'
        
    """
    return dt_obj.strftime('%Y-%m-%d')

def dt_to_longstr(dt_obj):
    """
    Take a datetime object and convert it to string keeping year, month, date, hour, minutes, seconds
    
    Args:
        dt_obj (datetime.datetime):
    
    Returns:
        str with a format 'YYYY-mm-ddTHH:MM:ss.ssssZ'
    """
    isoformat = dt_obj.isoformat()
    if isoformat[-1] == '+00:00':
        return isoformat.replace("+00:00", "Z")
    else:
        return ''.join([isoformat, 'Z'])

def dt_now_utc():
    """
    Returns current UTC time as datetime.datetime
    """
    return datetime.datetime.now(datetime.timezone.utc)
    