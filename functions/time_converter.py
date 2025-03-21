def time_to_milliseconds(time_str):
    if time_str == 'N/A' or not time_str:
        return None
    
    if ':' not in time_str:
        raise ValueError(f"Invalid time format: {time_str}")
    
    minutes, sec_milli = time_str.split(":")
    seconds, milliseconds = sec_milli.split(".")
    
    minutes = int(minutes) * 60000
    seconds = int(seconds) * 1000
    milliseconds = float(milliseconds)
    
    total_milliseconds = minutes + seconds + milliseconds
    
    return total_milliseconds
