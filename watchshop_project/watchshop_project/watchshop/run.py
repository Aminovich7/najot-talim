#!/usr/bin/env python
"""Quick start script"""
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchshop.settings')

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])
