
class MyVersionInfo(object):

    def __init__(self, package, version):
        self.package = package
        self.version = version
        self._cached_version = None
        self._semantic = None


version_info = MyVersionInfo('faas-api', '0.1')
