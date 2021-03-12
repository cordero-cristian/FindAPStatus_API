from selfInstall.api.auth.decorators import tokenRequired


@tokenRequired
def work(mac):
    return mac
