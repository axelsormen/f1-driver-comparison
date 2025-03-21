def time_to_milliseconds(time_str):
    try:
        if time_str == "N/A" or time_str == "" or time_str is None:
            return float('inf')  # Set to infinity to ensure invalid times are ignored in comparisons

        # Split the time by the first ':'
        minutes, sec_ms = time_str.split(":")

        # Split the seconds.milliseconds part by '.'
        seconds, milliseconds = sec_ms.split(".")

        # Convert to milliseconds
        minutes = int(minutes) * 60000  # Convert minutes to milliseconds
        seconds = int(seconds) * 1000  # Convert seconds to milliseconds
        milliseconds = int(milliseconds)  # Already in milliseconds

        # Return total time in milliseconds
        return minutes + seconds + milliseconds
    except Exception as e:
        # If there's an error in parsing, return infinity as a fallback
        print(f"Error parsing time {time_str}: {e}")
        return float('inf')
