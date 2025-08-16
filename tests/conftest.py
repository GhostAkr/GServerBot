"""
Pytest configuration file for the GServerBot project.
This file helps pytest find and import modules correctly.
"""

import sys
import os

# Add the src directory to the Python path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
