"""Processor modules for different data sources"""
from .gyg_processor import process_gyg
from .tiqets_processor import process_tiqets
from .viator_processor import process_viator

__all__ = ['process_gyg', 'process_tiqets', 'process_viator']
