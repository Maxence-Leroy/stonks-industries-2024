from typing import Callable

debug = True
info = True
warning = True
error = True

destination_function: Callable[[str], None] = print

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
