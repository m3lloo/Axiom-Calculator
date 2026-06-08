"""Pytest configuration - Add parent directory to path"""
import sys
import os

# Add parent directory to Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
