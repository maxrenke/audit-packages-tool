"""
audit_packages_tool - System Package Auditor

A tool for auditing and listing installed packages from various package managers.
"""

__version__ = "0.1.0"
__author__ = "Max Renke"
__email__ = "info@maxrenke.com"

from .cli import main
from .models import PackageInfo, PackageManager
from .reporting import ConsoleReporter, JSONExporter
from .scanner import PackageAuditor

__all__ = [
    "main",
    "PackageInfo",
    "PackageManager",
    "PackageAuditor",
    "ConsoleReporter",
    "JSONExporter",
]
