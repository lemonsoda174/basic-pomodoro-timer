import sys, re, time

def main():
    print("Pomodoro timer!")
    mode = mode_check(input("Choose mode (Stopwatch/Timer)\n"))
    time_total = time_check(input("How long do you want to study? (AA:BB:CC, where AA-hours, BB-minutes, CC-seconds)\n"))
    timer(mode, time_total)

def mode_check(a):
    if a.lower().strip() == "timer":
        return "Timer"
    elif a.lower().strip() == "stopwatch":
        return "Stopwatch"
    sys.exit("Invalid mode")
#checks if mode is valid or not. valid input should be in the form of "timer" or "stopwatch", case-insensitively

def time_check(b):
    if matches := re.search(r"^([0-9][0-9]):([0-5][0-9]):([0-5][0-9])$", b.strip()):
        return [int(matches.group(1)), int(matches.group(2)), int(matches.group(3))]
    sys.exit("Invalid time")
#checks if time is valid or not. valid input should be in the range from 00:00:00 to 99:59:59

def timer(mode, time_total):
    h, m, s = time_total
    if mode == "Timer":
        for remaining in range(h*3600+m*60+s, -1, -1):
            m, s = divmod(remaining, 60)
            h, m = divmod(m, 60)
            display = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            print("\rTime remaining: {}".format(display), end="")
            time.sleep(1)
        print("\nSession completed!")

    elif mode == "Stopwatch":
        for remaining in range(h*3600+m*60+s+1):
            m, s = divmod(remaining, 60)
            h, m = divmod(m, 60)
            display = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            print("\rTime: {}".format(display), end="")
            time.sleep(1)
        print("\nSession completed!")
    
    else:
        sys.exit("Invalid input")
    return True
"""
timer counts down from the desired study time to 00:00:00
stopwatch counts up from 00:00:00 to the desired study time
"""

if __name__ == "__main__":
    main()
