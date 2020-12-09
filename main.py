"""
Created by Epic at 12/9/20
"""

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge
from waitress import serve
from speedtest import Speedtest
from threading import Thread

upload_monitor = Gauge("speed_upload", "Upload speed", unit="MiB")
download_monitor = Gauge("speed_download", "Download speed", unit="MiB")

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


def monitor():
    s = Speedtest()
    while True:
        print("Starting speedtest")
        upload = s.upload()
        download = s.download()

        upload_monitor.set(upload)
        download_monitor.set(download)
        print("Speedtest completed")


Thread(target=monitor).start()
serve(app, port=5050)
