"""
Executable detection logic for audit_packages_tool.

Contains heuristics to determine if a package is likely an executable/CLI tool.
"""

import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import PackageInfo


class ExecutableDetector:
    """Detects whether packages are likely executable/CLI tools."""

    def is_executable_package(self, pkg: "PackageInfo") -> bool:
        """Heuristic to determine if a package is likely an executable/CLI tool."""
        # Check package manager type - some managers are more likely to have executables
        if pkg.manager and any(
            kw in pkg.manager.lower()
            for kw in ["go", "cargo", "npm", "brew", "snap", "flatpak"]
        ):
            return True

        # Check installation location for bin directories
        if pkg.location and (
            "/bin/" in pkg.location
            or r"\\bin\\" in pkg.location
            or pkg.location.endswith("/bin")
            or pkg.location.endswith(r"\\bin")
        ):
            return True

        # For pip packages, check if the package name is available as a command
        if pkg.manager and "pip" in pkg.manager.lower():
            if pkg.name and shutil.which(pkg.name):
                return True

        return False
