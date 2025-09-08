"""
Console output formatting for audit_packages_tool.

Handles printing formatted output to the console.
"""

from datetime import datetime
from typing import Optional

from ..models import PackageInfo
from ..scanner.executable_detector import ExecutableDetector


class ConsoleReporter:
    """Formats and prints audit results to the console."""

    def __init__(self) -> None:
        """Initialize the console reporter."""
        self.detector = ExecutableDetector()

    def print_summary(
        self, results: dict[str, list[PackageInfo]], filter_executables: bool = True
    ) -> None:
        """Print a formatted summary of scan results."""
        print("\n" + "=" * 80)
        print("SYSTEM PACKAGE AUDIT SUMMARY")
        print("=" * 80)

        filtered_results = {}
        for manager, packages in results.items():
            if filter_executables:
                filtered = [
                    pkg for pkg in packages if self.detector.is_executable_package(pkg)
                ]
            else:
                filtered = packages

            if filtered:
                filtered_results[manager] = filtered

        total_packages = sum(len(packages) for packages in filtered_results.values())
        print(f"Total packages found: {total_packages}")
        print(f"Package managers detected: {len(filtered_results)}")
        print(f"Audit completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for manager, packages in filtered_results.items():
            print(f"\n{manager.upper()} ({len(packages)} packages):")
            print("-" * 50)

            sorted_packages = sorted(packages, key=lambda p: p.name.lower())
            for pkg in sorted_packages:
                desc_info = self._format_description(pkg.description)
                print(f"  {pkg.name:<30} {pkg.version:<15}{desc_info}")

    def print_search_results(
        self, packages: list[PackageInfo], search_term: str
    ) -> None:
        """Print formatted search results."""
        if packages:
            print(f"\nFound {len(packages)} package(s) matching '{search_term}':")
            print("-" * 50)
            for pkg in packages:
                print(f"  {pkg.name} ({pkg.version}) - {pkg.manager}")
        else:
            print(f"\nNo packages found matching '{search_term}'")

    def _format_description(self, description: Optional[str]) -> str:
        """Format package description for display."""
        if not description:
            return ""

        if len(description) > 50:
            return f" - {description[:50]}..."
        else:
            return f" - {description}"
