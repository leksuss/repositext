#!/usr/bin/env python

import importlib
import os
import sys

try:    
    from local import project_settings as project_settings
    os.environ['DJANGO_SETTINGS_MODULE'] = project_settings
    settings = importlib.import_module(project_settings, package=None)
except ModuleNotFoundError:
    project_settings = 'repositext.settings'
    os.environ['DJANGO_SETTINGS_MODULE'] = project_settings
    import repositext.settings as settings # noqa E402


class ProjectSettingsExtractor:

    def __init__(self, debug=False):
        self.debug = debug

    def show_valid_keys(self):
        info = self._get_settings()
        for key in info:
            print(key)
            print('  |-', info[key])
            print('\n')

    def _get_settings(self):
        return settings.__dict__

    def _get_info(self, info):
        for arg in sys.argv[1:]:
            try:
                info = info[arg]
                if self.debug:
                    print(info)
            except KeyError:
                print('invalid key: ', arg)
                print('The following keys are valid:')
                self.show_valid_keys()
                sys.exit(1)
        return info

    def run(self):
        print(
            self._get_info(
                self._get_settings()
            )
        )


if __name__ == '__main__':
    pse = ProjectSettingsExtractor()
    pse.run()
