"""
Package models for audit_packages_tool.

Contains data structures for representing package information.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PackageManager(Enum):
    """Supported package managers."""

    PIP = "pip"
    NPM = "npm"
    CARGO = "cargo"
    BREW = "brew"
    WINGET = "winget"
    APT = "apt"
    YUM = "yum"
    SNAP = "snap"
    FLATPAK = "flatpak"


@dataclass
class PackageInfo:
    """Information about an installed package."""

    name: str
    version: str
    manager: str
    location: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the package info after initialization."""
        if not self.name:
            raise ValueError("Package name cannot be empty")
        if not self.version:
            raise ValueError("Package version cannot be empty")
        if not self.manager:
            raise ValueError("Package manager cannot be empty")

    @property
    def is_executable(self) -> bool:
        """Heuristic to determine if package is likely an executable/CLI tool."""
        # This will be moved to the scanner logic later
        return True  # Placeholder for now
