#!/usr/bin/env python
import os
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ninformes.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
