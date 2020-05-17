from prometheus_async import aio
from prometheus_client import Gauge
import asyncio
import aa_prometheus.quota


class AAPrometheus:
    def __init__(self):
        self.metrics = []

        self.add_quota_remaining()

    def add_quota_remaining(self):
        g = Gauge("aa_quota_remaining_bytes", "AAISP quota remaining (bytes)")
        g.set_function(aa_prometheus.quota.remaining)

        self.metrics.append(g)

    def start_web_server(self):
        aio.web.start_http_server_in_thread(port=8000)
        asyncio.get_event_loop().run_forever()


def main():
    prom = AAPrometheus()
    prom.start_web_server()


if __name__ == "__main__":
    main()
