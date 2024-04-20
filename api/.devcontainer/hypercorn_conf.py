import json
import multiprocessing
import os

# utils

truly = ["yes", "y", "1", "true"]


# ssl opts
use_ssl = (os.getenv("USE_SSL", "False")).lower() in truly
use_tcp = (os.getenv("USE_TCP", "True")).lower() in truly
# assert any([use_ssl, use_tcp]), "At least one of USE_SSL and USE_TCP must be set"

use_certfile = os.getenv("CERTFILE", None)
use_ca_certs = os.getenv("CA_CERTS", None)
use_ciphers = os.getenv("CIPHERS", "ECDHE+AESGCM")
use_keyfile = os.getenv("KEYFILE", None)
# assert not(use_ssl and any([use_certfile, use_keyfile, use_ca_certs])), "USE_SSL Requires CERTFILE/KEYFILE/CA_CERTS"


# binding
host = os.getenv("HOST", "0.0.0.0")  # nosec # noqa
ssl_port = os.getenv("SSL_PORT", "4443")
tcp_port = os.getenv("TCP_PORT", "8000")
if use_ssl:
    assert ssl_port != tcp_port, "SSL_PORT Must be different than TCP_PORT"  # nosec # noqa

use_quic_bind = os.getenv("QUIC_BIND", None)

use_insecure_bind = os.getenv("INSECURE_BIND", None)

# assert not(bool(use_insecure_bind) != all([use_ssl, use_tcp])), "INSECURE_BIND Must be used only when USE_SSL and USE_TCP are both set"
if use_ssl and use_tcp:
    if not use_insecure_bind:
        use_insecure_bind = "{}:{}".format(host, tcp_port)

use_bind = os.getenv("BIND", None)
if not use_bind:
    use_bind = "{}:{}".format(host, ssl_port if use_ssl else tcp_port)


# workers
cores = multiprocessing.cpu_count()
workers_multiplier = float(os.getenv("WORKERS_PER_CORE", "1"))
workers_max = os.getenv("MAX_WORKERS", None)
if workers_max:
    workers_max = int(workers_max)

default_web_concurrency = cores * workers_multiplier
web_concurrency = web_concurrency = os.getenv("WEB_CONCURRENCY", None)

if web_concurrency:
    use_web_concurrency = int(web_concurrency)
    assert use_web_concurrency > 0, "WEB_CONCURRENCY Must be non zero"  # nosec # noqa
else:
    use_web_concurrency = max(int(default_web_concurrency), 2)
    if workers_max:
        use_web_concurrency = min(use_web_concurrency, workers_max)
        # fmt: off
        assert use_web_concurrency > 0, "MAX_WORKERS and WORKERS_PER_CORE Must be non zero"  # nosec # noqa

use_worker_class = os.getenv("WORKER_CLASS", "asyncio")
# fmt: off
assert use_worker_class in ["asyncio", "uvloop", "trio"], "WORKER_CLASS Must be asyncio, uvloop or trio"  # nosec # noqa


# others
use_graceful_timeout = os.getenv("GRACEFUL_TIMEOUT", "120")
use_errorlog = os.getenv("ERROR_LOG", "-")
use_accesslog = os.getenv("ACCESS_LOG", "-")
use_keepalive_timeout = os.getenv("KEEP_ALIVE", "5")


# conf
keep_alive_timeout = int(use_keepalive_timeout)
worker_class = use_worker_class
workers = use_web_concurrency
loglevel = os.getenv("LOG_LEVEL", "INFO")
accesslog = use_accesslog or None
errorlog = use_errorlog or None
graceful_timeout = int(use_graceful_timeout)
backlog = int(os.getenv("BACKLOG", "100"))

certfile = use_certfile
ca_certs = use_ca_certs
ciphers = use_ciphers
keyfile = use_keyfile
insecure_bind = None
quic_bind = None
websocket_ping_interval = int(os.getenv("WEBSOCKET_PING_INTERVAL", "10"))
access_log_format = "%(L)s %(h)s %(S)s %(l)s %(r)s %(s)s %(b)s %(f)s %(a)s"
bind = use_bind
if use_ssl and use_tcp:
    insecure_bind = use_insecure_bind
if use_quic_bind:
    quic_bind = use_quic_bind


# conf/env data
conf_data = {
    "accesslog": accesslog,
    "errorlog": errorlog,
    "loglevel": loglevel,
    "backlog": backlog,
    "bind": bind,
    "insecure_bind": insecure_bind if use_tcp and use_ssl else None,
    "quic_bind": quic_bind if use_quic_bind else None,
    "graceful_timeout": graceful_timeout,
    "keep_alive_timeout": keep_alive_timeout,
    "workers": workers,
    "worker_class": worker_class,
    "websocket_ping_interval": websocket_ping_interval,
    "access_log_format": access_log_format,
    "env": {
        "host": host,
        "ssl_port": ssl_port if use_ssl else None,
        "tcp_port": tcp_port if use_tcp else None,
        "use_ssl": use_ssl,
        "use_tcp": use_tcp,
        "workers_multiplier": workers_multiplier,
        "cores": cores,
    },
}

print(json.dumps(conf_data, indent=4), flush=True)
