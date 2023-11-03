from datetime import datetime
from typing import Callable

debug = True
info = True
warning = True
error = True

def log_with_date(log: str):
    now = datetime.now()
    print_log(f'[{now.hour}:{now.minute}:{now.second}:{now.microsecond}] {log}')

def print_log(log: str):
    print(log)

destination_function: Callable[[str], None] = log_with_date

def logging_debug(log: str):
    if debug:
        destination_function(f'[D] : {log}')

def logging_info(log: str):
    if info:
        destination_function(f'[I] : {log}')

def logging_warning(log: str):
    if warning:
        destination_function(f'[W] : {log}')

def logging_error(log: str):
    if error:
        destination_function(f'[E] : {log}')