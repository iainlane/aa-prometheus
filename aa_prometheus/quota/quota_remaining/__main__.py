from prometheus_async import aio
from prometheus_client import Gauge
import asyncio
import aa_prometheus.quota


def start_web_server():

    g = Gauge("aa_quota_remaining_bytes", "AAISP quota remaining (bytes)")
    g.set_function(aa_prometheus.quota.remaining)

    aio.web.start_http_server_in_thread(port=8000)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    start_web_server()
