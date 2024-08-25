import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import threading
import re

paused = False
h,m,s = [0,0,0]
class TimerGUI():
    def __init__(self):
        self.root = tk.Tk()

        #menu bar

        options = ["Timer", "Stopwatch", "Break"]
        var = tk.StringVar()
        drop = tk.OptionMenu(self.root, var, *options, command = self.popup_mode)
        var.set("Change timer mode")
        drop.pack(anchor="nw", padx = 10, pady = 10)

        time_setting_menu = tk.Button(self.root, text = "Time settings", command = self.change_time)
        time_setting_menu.place(x=400, y=10)

        self.label = tk.Label(self.root, text = "Your Pomodoro Timer", font = ("Arial", 18))
        self.label.pack(padx=20, pady=20)

        self.timer_mode = "Timer"
        self.time_total = [0, 25, 0]
        self.timer_display = tk.Label(self.root, text="{:02d}:{:02d}:{:02d}".format(*self.time_total), font=("Arial", 48))
        self.timer_display.pack(padx=20, pady=20)

        self.root.geometry("500x500")
        self.root.title("Pomodoro timer")

        #function buttons row
        self.buttons = tk.Frame(self.root)
        self.buttons.columnconfigure(0, weight = 1)
        self.buttons.columnconfigure(1, weight = 1)
        self.buttons.columnconfigure(2, weight = 1)

        self.start_button = tk.Button(self.buttons, text = "Start", font = ("Arial", 18), command = self.start_timer)
        self.start_button.grid(row = 0, column = 0, sticky = tk.W + tk.E)

        self.stop_button = tk.Button(self.buttons, text = "Stop", font = ("Arial", 18), command = self.stop_timer)
        self.stop_button.grid(row = 0, column = 1, sticky = tk.W + tk.E)

        self.buttons.pack()

        self.running = False
        #default: Timer mode, 25 minute session
        

        self.timer_thread = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


    #mode menu
    def popup_mode(self, value):
        if value == "Timer":
            self.timer_mode = "Timer"
        elif value == "Stopwatch":
            self.timer_mode = "Stopwatch"
        elif value == "Break":
            self.timer_mode = "Break"
        self.reset_timer()

    #time setting
    def change_time(self):
        try:
            self.reset_timer()
            time_input = simpledialog.askstring(title = "Time settings", prompt="Enter the amount of time you want to study for", initialvalue="{:02d}:{:02d}:{:02d}".format(*self.time_total))
            p = r"^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$"
            if not bool(re.fullmatch(p, time_input)):
                raise BaseException
            self.time_total = list(map(int, time_input.split(":")))
            display = "{:02d}:{:02d}:{:02d}".format(*self.time_total)
            self.timer_display.config(text = display)
        except:
            messagebox.showinfo(title="Invalid input", message="Try another input")
            

    #functional buttons
    def start_timer(self):
        if not self.running:
            self.running = True
            self.timer_thread = threading.Thread(target=self.timer)
            self.timer_thread.start()
            
    def stop_timer(self):
        self.running = False
        if self.timer_thread:
            self.timer_thread.join()
        self.start_button.config(text = "Continue", command=self.continue_timer)
        self.stop_button.config(text = "Reset", command=self.reset_timer)

    def continue_timer(self):
        global paused
        paused = True
        self.start_button.config(text = "Start", command=self.start_timer)
        self.stop_button.config(text = "Stop", command=self.stop_timer)
        self.start_timer()

    def reset_timer(self):
        self.running = False
        if self.timer_thread:
            self.timer_thread.join()
        display = "{:02d}:{:02d}:{:02d}".format(*self.time_total)
        self.timer_display.config(text = display)
        self.start_button.config(text = "Start", command=self.start_timer)
        self.stop_button.config(text = "Stop", command=self.stop_timer)

    """
    def time_check(self, b):
        if matches := re.search(r"^([0-9][0-9]):([0-5][0-9]):([0-5][0-9])$", b.strip()):
            return [int(matches.group(1)), int(matches.group(2)), int(matches.group(3))]
        sys.exit("Invalid time")
    # checks if time is valid or not. valid input should be in the range from 00:00:00 to 99:59:59
    # once used for manual input, now no longer needed
    """
    #inner working of the timer
    def timer(self):
        global paused, h, m, s
        
        if not paused:
            h, m, s = self.time_total
        else:
            paused = False
        if self.timer_mode == "Timer":
            for remaining in range(h*3600+m*60+s, -1, -1):
                if not self.running:
                    break
                m, s = divmod(remaining, 60)
                h, m = divmod(m, 60)
                display = "{:02d}:{:02d}:{:02d}".format(h, m, s)
                self.timer_display.config(text = display)
                time.sleep(1)
            if self.running:
                messagebox.showinfo(title="Session done!", message="Good job :)")
                self.timer_display.config(text = "00:00:00")
                self.running = False

        elif self.timer_mode == "Stopwatch":
            for remaining in range(h*3600+m*60+s+1):
                if not self.running:
                    break
                m, s = divmod(remaining, 60)
                h, m = divmod(m, 60)
                display = "{:02d}:{:02d}:{:02d}".format(h, m, s)
                self.timer_display.config(text = display)
                time.sleep(1)
            if self.running:
                messagebox.showinfo(title="Session done!", message="Good job :)")
                self.timer_display.config(text = "00:00:00")
                self.running = False
        
        #exactly the same as Timer mode, except the display message on session completion
        elif self.timer_mode == "Break":
            for remaining in range(h*3600+m*60+s, -1, -1):
                if not self.running:
                    break
                m, s = divmod(remaining, 60)
                h, m = divmod(m, 60)
                display = "{:02d}:{:02d}:{:02d}".format(h, m, s)
                self.timer_display.config(text = display)
                time.sleep(1)
            if self.running:
                messagebox.showinfo(title="Break time over", message="Go back to work!")
                self.timer_display.config(text = "00:00:00")
                self.running = False


    #ask user to be sure of closing app
    def on_closing(self):
        if messagebox.askyesno(title="Are you sure?", message="Do you want to close the application?"):
            self.running = False
            self.root.destroy()

TimerGUI()


