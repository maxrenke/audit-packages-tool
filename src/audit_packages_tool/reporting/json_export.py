"""
JSON export functionality for audit_packages_tool.

Handles exporting scan results to JSON format.
"""

import json

from ..models import PackageInfo
from ..scanner.executable_detector import ExecutableDetector


class JSONExporter:
    """Exports audit results to JSON format."""

    def __init__(self) -> None:
        """Initialize the JSON exporter."""
        self.detector = ExecutableDetector()

    def export_to_json(
        self,
        results: dict[str, list[PackageInfo]],
        filename: str = "system_packages.json",
        filter_executables: bool = True,
    ) -> None:
        """Export results to JSON file."""
        export_data = {}

        for manager, packages in results.items():
            if filter_executables:
                filtered = [
                    pkg for pkg in packages if self.detector.is_executable_package(pkg)
                ]
            else:
                filtered = packages

            if filtered:
                export_data[manager] = [self._package_to_dict(pkg) for pkg in filtered]

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"\nResults exported to {filename}")

    def _package_to_dict(self, pkg: PackageInfo) -> dict:
        """Convert a PackageInfo object to a dictionary."""
        return {
            "name": pkg.name,
            "version": pkg.version,
            "manager": pkg.manager,
            "location": pkg.location,
            "size": pkg.size,
            "description": pkg.description,
        }
