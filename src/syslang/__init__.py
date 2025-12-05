"""
SysLang - DSL for Transdisciplinary Systemic Analysis
"""

__version__ = "1.0.0"
__author__ = "Echopraxium"
__license__ = "MIT"

from .cli import main
from .parser import load_syslang

__all__ = ["main", "load_syslang"]