# -*- coding: utf-8 -*-

"""Package class"""

from src.core import sys, process, filesystem, helper
from src.core import SystemError, FileSystemError

from .config import Config
from ...lib.exceptions import LibError

class Package:
    """Package class"""

    remote_version = None

    @staticmethod
    def examples():
        """ load usage examples """

        sys.exit(Config.params['examples'])

    @staticmethod
    def banner():
        """ load application banner """

        try:

            banner = Config.params['banner'].format(
                'Directories: {0}'.format(Package.__directories_count()),
                'Subdomains: {0}'.format(Package.__subdomains_count()),
                'Browsers: {0}'.format(Package.__browsers_count()),
                'Proxies: {0}'.format(Package.__proxies_count()),
                Package.__license(), 'yellow')

            sys.writeln(banner)
        except (FileSystemError, SystemError, LibError) as e:
            raise LibError(e)

    @staticmethod
    def version():
        """ load application version """

        try:

            banner = Config.params['version'].format(
            Package.__app_name(),
            Package.__current_version(),
            Package.__remote_version(),
            Package.__repo(),
            Package.__license(),
            'yellow')

            sys.writeln(banner)
        except (FileSystemError, SystemError, LibError) as e:
            raise LibError(e)

    @staticmethod
    def update():
        """ check for update"""

        try:
            # Log.success('Checking for updates...')
            status = process.open(Config.params['cvsupdate'])

            sys.writeln(str(status[0]).rstrip())
            sys.writeln(str(status[1]).rstrip())
            # sys.stdout.write(Log.success(str(out).rstrip()))
            # sys.stdout.write(Log.info(str(error).rstrip()))

            status = process.open(Config.params['cvslog'])
            sys.exit(str(status[0]).rstrip())
            # sys.stdout.write(Log.info(str(out).strip()))

        except SystemError as e:
            raise LibError(e)


    @staticmethod
    def local_version():
        """ get local version """

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            return config.get('info', 'version')
        except FileSystemError as e:
            raise LibError(e)

    @staticmethod
    def __app_name():
        """ get app name """

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            return config.get('info', 'name')
        except FileSystemError as e:
            raise LibError(e)


    @staticmethod
    def __remote_version():
        """ get remote version """

        if None is Package.remote_version:

            try:
                config = filesystem.readcfg(Config.params['cfg'])
                request_uri = config.get('info', 'setup')
                result = process.open('curl -sb GET {uri}'.format(uri=request_uri))
                raw = filesystem.readraw(result[0])
                Package.remote_version = raw.get('info', 'version')
                return Package.remote_version
            except (FileSystemError, SystemError) as e:
                raise LibError(e)
        else:
            return Package.remote_version

    @staticmethod
    def __current_version():
        """ get current version """

        try :
            local = Package.local_version()
            remote = Package.__remote_version()

            if True is helper.is_less(local, remote):
                # @TODO red
                version = local
            else:
                # @TODO green
                version = local
            return version

        except (FileSystemError, SystemError, LibError) as e:
            raise LibError(e)

    @staticmethod
    def __repo():
        """ get repo """

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            return config.get('info', 'repository')
        except FileSystemError as e:
            raise LibError(e)

    @staticmethod
    def __license():
        """ get license """

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            return config.get('info', 'license')
        except FileSystemError as e:
            raise LibError(e)

    @staticmethod
    def __directories_count():
        """ get number of directories in basic wordlist"""

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            filename = config.get('opendoor', 'directories')
            count = filesystem.read(filename).__len__()
            return count

        except FileSystemError as e:
            raise LibError(e)

    @staticmethod
    def __subdomains_count():
        """ get number of subdomains in basic wordlist"""

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            filename = config.get('opendoor', 'subdomains')
            count = filesystem.read(filename).__len__()

            return count

        except FileSystemError as e:
            raise LibError(e)

    @staticmethod
    def __browsers_count():
        """ get number of browsers in basic wordlist"""

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            filename = config.get('opendoor', 'useragents')
            count = filesystem.read(filename).__len__()

            return count

        except FileSystemError as e:
            raise LibError(e)

    @staticmethod
    def __proxies_count():
        """ get number of proxy servers in basic wordlist"""

        try :
            config = filesystem.readcfg(Config.params['cfg'])
            filename = config.get('opendoor', 'proxy')
            count = filesystem.read(filename).__len__()

            return count

        except FileSystemError as e:
            raise LibError(e)

