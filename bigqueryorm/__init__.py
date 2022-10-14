'''
bigqueryorm

A BigQuery ORM
'''

__title__ = 'bigqueryorm'
__version__ = '0.0.1'
__all__ = ("declare_row", "Count", "Client")
__author__ = '__xor__ <dunder.xor.dunder@gmail.com'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2022 __xor__'


from .query import declare_row, Count, Client
