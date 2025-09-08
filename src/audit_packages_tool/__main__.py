"""
Allow audit_packages_tool to be executed as a module with -m flag.

Usage: python -m audit_packages_tool
"""

from .cli import main

if __name__ == "__main__":
    main()
