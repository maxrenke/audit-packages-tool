"""
Main package auditor for audit_packages_tool.

Contains the core scanning logic for different package managers.
"""

import json
import subprocess
import sys

from ..models import PackageInfo
from .executable_detector import ExecutableDetector


class PackageAuditor:
    """Main auditor that scans system packages across different package managers."""

    def __init__(self) -> None:
        """Initialize the package auditor."""
        self.detector = ExecutableDetector()

    def audit_system(self) -> dict[str, list[PackageInfo]]:
        """Audit all supported package managers on the system."""
        results: dict[str, list[PackageInfo]] = {}

        # Define all possible package manager getters
        all_managers = {
            "pip": self._get_pip_packages,
            "npm": self._get_npm_packages,
            "cargo": self._get_cargo_packages,
            "brew": self._get_brew_packages,
        }

        # Determine which managers to run based on the platform
        managers_to_run = {
            "pip",
            "npm",
            "cargo",  # Cross-platform
        }
        if sys.platform == "darwin":
            managers_to_run.update(["brew"])
        # Future platforms can be added here

        for manager_name in managers_to_run:
            getter = all_managers[manager_name]
            try:
                packages = getter()
                if packages:
                    results[manager_name] = packages
            except FileNotFoundError:
                # This is expected if the package manager isn't installed
                pass
            except Exception as e:
                print(f"Error auditing {manager_name}: {e}", file=sys.stderr)

        # Add system alias
        if sys.platform == "darwin" and "brew" in results:
            results["system"] = results["brew"]

        return results

    def find_packages(
        self,
        results: dict[str, list[PackageInfo]],
        search_term: str,
        filter_executables: bool = True,
    ) -> list[PackageInfo]:
        """Find packages matching a search term."""
        found = []
        search_term = search_term.lower()

        for _manager, packages in results.items():
            for pkg in packages:
                if filter_executables and not self.detector.is_executable_package(pkg):
                    continue

                if search_term in pkg.name.lower() or (
                    pkg.description and search_term in pkg.description.lower()
                ):
                    found.append(pkg)

        return found

    def _get_pip_packages(self) -> list[PackageInfo]:
        """Get packages installed via pip."""
        packages = []
        try:
            # Get the list of all installed packages
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                check=True,
            )
            installed_packages = json.loads(result.stdout)

            # Get details for all packages at once
            package_names = [pkg["name"] for pkg in installed_packages]
            show_result = subprocess.run(
                [sys.executable, "-m", "pip", "show"] + package_names,
                capture_output=True,
                text=True,
                check=True,
            )

            # Process the output of pip show
            all_details = show_result.stdout.split("---\\n")
            for details_str in all_details:
                if not details_str.strip():
                    continue

                details = dict(
                    line.split(": ", 1)
                    for line in details_str.splitlines()
                    if ": " in line
                )

                if "Name" in details and "Version" in details:
                    packages.append(
                        PackageInfo(
                            name=details.get("Name", ""),
                            version=details.get("Version", ""),
                            manager="pip",
                            location=details.get("Location"),
                            description=details.get("Summary"),
                        )
                    )

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not run pip command: {e}", file=sys.stderr)
        except json.JSONDecodeError as e:
            print(f"Could not parse pip list output: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

        return packages

    def _get_npm_packages(self) -> list[PackageInfo]:
        """Get packages installed via npm."""
        packages = []
        try:
            result = subprocess.run(
                ["npm", "list", "-g", "--json"],
                capture_output=True,
                text=True,
                check=True,
                shell=True,
            )
            data = json.loads(result.stdout)

            if "dependencies" in data:
                for name, details in data["dependencies"].items():
                    packages.append(
                        PackageInfo(
                            name=name,
                            version=details.get("version", ""),
                            manager="npm",
                            description=details.get("description"),
                        )
                    )
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            json.JSONDecodeError,
        ) as e:
            print(f"Could not get npm packages: {e}", file=sys.stderr)

        return packages

    def _get_cargo_packages(self) -> list[PackageInfo]:
        """Get packages installed via cargo."""
        packages = []
        try:
            result = subprocess.run(
                ["cargo", "install", "--list"],
                capture_output=True,
                text=True,
                check=True,
            )

            for line in result.stdout.splitlines():
                if not line.startswith(" "):
                    parts = line.split()
                    if len(parts) >= 2:
                        name = parts[0]
                        version = parts[1].strip(":")
                        packages.append(
                            PackageInfo(name=name, version=version, manager="cargo")
                        )

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not get cargo packages: {e}", file=sys.stderr)

        return packages

    def _get_brew_packages(self) -> list[PackageInfo]:
        """Get packages installed via brew (macOS)."""
        packages = []
        try:
            result = subprocess.run(
                ["brew", "list", "--versions"],
                capture_output=True,
                text=True,
                check=True,
            )

            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    version = parts[1]
                    packages.append(
                        PackageInfo(name=name, version=version, manager="brew")
                    )

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not get brew packages: {e}", file=sys.stderr)

        return packages
