from os import getenv

from uvicorn.workers import UvicornWorker


class Worker(UvicornWorker):
    CONFIG_KWARGS = {
        "proxy_headers": True,
        "forwarded_allow_ips": "*",
        "root_path": getenv("ROOT_PATH", ""),
    }

    def __init__(self, *args, **kwargs):
        self._set_proxy_headers = kwargs.pop("set_proxy_headers", True)
        super().__init__(*args, **kwargs)

    def get_environ(self):
        environ = super().get_environ()
        if self._set_proxy_headers:
            self._set_proxy_headers = False
            # Set the HTTP_X_FORWARDED_* headers
            forwarded_proto = environ.get("HTTP_X_FORWARDED_PROTO", "")
            if forwarded_proto:
                environ["wsgi.url_scheme"] = forwarded_proto
            forwarded_host = environ.get("HTTP_X_FORWARDED_HOST", "")
            if forwarded_host:
                environ["HTTP_HOST"] = forwarded_host
            forwarded_port = environ.get("HTTP_X_FORWARDED_PORT", "")
            if forwarded_port:
                environ["SERVER_PORT"] = forwarded_port
            forwarded_for = environ.get("HTTP_X_FORWARDED_FOR", "")
            if forwarded_for:
                environ["REMOTE_ADDR"] = forwarded_for.split(",")[0]
        return environ
