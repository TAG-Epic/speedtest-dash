"""
Created by Epic at 12/9/20
"""

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge
from waitress import serve
from speedtest import Speedtest
from threading import Thread
from time import sleep
from os import getenv
upload_monitor = Gauge("speedtest_upload", "Upload speed")
download_monitor = Gauge("speedtest_download", "Download speed")
ping_monitor = Gauge("speedtest_ping", "Ping")

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


def monitor():
    s = Speedtest()
    while True:
        try:
            print("Taking speedtest...")
            s.get_servers()
            ping = s.results.ping
            upload = s.upload()
            download = s.download()

            upload_monitor.set(upload)
            download_monitor.set(download)
            ping_monitor.set(ping)
            print("Speedtest done!")
        except:
            print("Speedtest failed!")
        sleep(int(getenv("INTERVAL", 60)))


Thread(target=monitor).start()
serve(app, host="0.0.0.0", port=5050)
