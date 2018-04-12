# coding: utf-8

from flask import Flask

import threading
import time
import subprocess

app = Flask(__name__)
DEFAULT_RUNNING_TIME = 300


class Service(object):

    def __init__(self):
        self.__keep_running = False
        self.__remaining_time = 0
        self.__server_thread = None
        self.__server_subprocess = None

    def server(self):
        print("Entering Server")
        self.__keep_running = True

        print("Process starts running")
        self.__server_subprocess = subprocess.Popen(["eog", "-s", "/home/rpatel/Pictures"])

        while self.__keep_running and self.__remaining_time >= 1:
            print("Server running. Going to sleep now...%ss" % self.__remaining_time)
            time.sleep(1)
            self.__remaining_time -= 1
        print(" Timeout and Stop process")
        self.__server_subprocess.terminate()
        print("Leaving server")
        return "Service"

    def start_server(self):
        if self.__server_thread and self.__server_thread .is_alive():
            print("Server thread already instantiated and running. Nothing to do.")
        else:
            if self.__server_thread and not self.__server_thread.is_alive():
                print("Server thread already instantiated but it is not running. Start it again!")
            else:
                print("Server thread never instantiated. Doing so now.")
            self.__remaining_time = DEFAULT_RUNNING_TIME
            self.__server_thread = threading.Thread(target=self.server, name='server_thread')
            self.__server_thread.start()

    def keep_alive_refresh(self):
        self.__remaining_time = DEFAULT_RUNNING_TIME
        if self.__server_thread and self.__server_thread.is_alive():
            print("Server thread already running timer reset by 10 more seconds. keep it alive. ")
            self.__keep_running = True
            print("Process timeout reset to 10 seconds")
        elif self.__server_thread and not self.__server_thread.is_alive():
            print("Server thread is not instantiated and it is not running. Start the Server.")

    def stop_server(self):
        if self.__server_thread and self.__server_thread.is_alive():
            print("Server thread already instantiated and running. Stopping it.")
            self.__server_subprocess.terminate()
            print("process is  no more running")
            self.__keep_running = False
        elif self.__server_thread and not self.__server_thread.is_alive():
            print("Server thread already instantiated but it is not running. Nothing to do.")


myService = Service()


@app.route('/start')
def start():
    print("Entering start")
    myService.start_server()
    print("Leaving Start")
    return "Start Server\n"


@app.route('/stop')
def stop():
    print("Entering stop")
    myService.stop_server()
    print("Leaving stop")
    return "Stop Server\n"


@app.route('/keep-alive')
def keep_alive():
    print("Entering Keep-alive")
    myService.keep_alive_refresh()
    print("Leaving keep alive")
    return "Keep_alive Server\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
