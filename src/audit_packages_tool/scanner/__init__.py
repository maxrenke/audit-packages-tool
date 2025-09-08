"""
Scanner module for audit_packages_tool.

This module contains the package scanning functionality.
"""

from .auditor import PackageAuditor
from .executable_detector import ExecutableDetector

__all__ = ["PackageAuditor", "ExecutableDetector"]
