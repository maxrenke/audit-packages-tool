import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class PackageInfo:
    name: str
    version: str
    manager: str
    location: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None

class PackageAuditor:
    def _is_executable_package(self, pkg: PackageInfo) -> bool:
        """Heuristic to determine if a package is likely an executable/CLI tool."""
        if pkg.manager and any(
            kw in pkg.manager.lower()
            for kw in ['go', 'cargo', 'npm', 'brew', 'snap', 'flatpak']
        ):
            return True
        if pkg.location and (
            '/bin/' in pkg.location or r'\\bin\\' in pkg.location or pkg.location.endswith('/bin') or pkg.location.endswith(r'\\bin')
        ):
            return True
        if pkg.manager and 'pip' in pkg.manager.lower():
            if pkg.name and shutil.which(pkg.name):
                return True
        return False

    def print_summary(self, results: Dict[str, List[PackageInfo]], filter_executables: bool = True):
        print("\n" + "="*80)
        print("SYSTEM PACKAGE AUDIT SUMMARY")
        print("="*80)

        filtered_results = {}
        for manager, packages in results.items():
            if filter_executables:
                filtered = [pkg for pkg in packages if self._is_executable_package(pkg)]
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
                desc_info = f" - {pkg.description[:50]}..." if pkg.description and len(pkg.description) > 50 else f" - {pkg.description}" if pkg.description else ""
                print(f"  {pkg.name:<30} {pkg.version:<15}{desc_info}")

    def export_to_json(self, results: Dict[str, List[PackageInfo]], filename: str = "system_packages.json", filter_executables: bool = True):
        export_data = {}
        for manager, packages in results.items():
            if filter_executables:
                filtered = [pkg for pkg in packages if self._is_executable_package(pkg)]
            else:
                filtered = packages
            if filtered:
                export_data[manager] = [
                    {
                        'name': pkg.name,
                        'version': pkg.version,
                        'manager': pkg.manager,
                        'location': pkg.location,
                        'size': pkg.size,
                        'description': pkg.description
                    }
                    for pkg in filtered
                ]
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"\nResults exported to {filename}")

    def find_package(self, results: Dict[str, List[PackageInfo]], search_term: str, filter_executables: bool = True):
        found = []
        search_term = search_term.lower()
        for manager, packages in results.items():
            for pkg in packages:
                if filter_executables and not self._is_executable_package(pkg):
                    continue
                if search_term in pkg.name.lower() or (pkg.description and search_term in pkg.description.lower()):
                    found.append(pkg)
        if found:
            print(f"\nFound {len(found)} package(s) matching '{search_term}':")
            print("-" * 50)
            for pkg in found:
                print(f"  {pkg.name} ({pkg.version}) - {pkg.manager}")
        else:
            print(f"\nNo packages found matching '{search_term}'")

    def audit_system(self) -> Dict[str, List[PackageInfo]]:
        results = {}
        # Define all possible package manager getters
        all_managers = {
            "pip": self._get_pip_packages,
            "npm": self._get_npm_packages,
            "cargo": self._get_cargo_packages,
            "brew": self._get_brew_packages,
        }

        # Determine which managers to run based on the platform
        managers_to_run = {
            "pip", "npm", "cargo" # Cross-platform
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
                # This is expected if the package manager isn't installed, so we don't print an error.
                pass
            except Exception as e:
                print(f"Error auditing {manager_name}: {e}", file=sys.stderr)
        
        # Add system alias
        if sys.platform == "darwin" and "brew" in results:
            results["system"] = results["brew"]

        return results

    def _get_pip_packages(self) -> List[PackageInfo]:
        packages = []
        try:
            # Get the list of all installed packages
            result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=json"], capture_output=True, text=True, check=True)
            installed_packages = json.loads(result.stdout)
            
            # Get details for all packages at once
            package_names = [pkg['name'] for pkg in installed_packages]
            show_result = subprocess.run([sys.executable, "-m", "pip", "show"] + package_names, capture_output=True, text=True, check=True)
            
            # Process the output of pip show
            all_details = show_result.stdout.split('---\n')
            for details_str in all_details:
                if not details_str.strip():
                    continue
                details = dict(line.split(': ', 1) for line in details_str.splitlines() if ': ' in line)
                packages.append(PackageInfo(
                    name=details.get("Name"),
                    version=details.get("Version"),
                    manager="pip",
                    location=details.get("Location"),
                    description=details.get("Summary"),
                ))

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not run pip command: {e}", file=sys.stderr)
        except json.JSONDecodeError as e:
            print(f"Could not parse pip list output: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

        return packages

    def _get_system_packages(self) -> List[PackageInfo]:
        packages = []
        if sys.platform == "win32":
            # Using winget for system packages on Windows
            return self._get_winget_packages()
        elif sys.platform == "darwin":
            # Using brew for system packages on macOS
            return self._get_brew_packages()
        else: # Linux
            # This is a placeholder for linux package managers like apt, yum, etc.
            pass
        return packages

    def _get_npm_packages(self) -> List[PackageInfo]:
        packages = []
        try:
            result = subprocess.run(["npm", "list", "-g", "--json"], capture_output=True, text=True, check=True, shell=True)
            data = json.loads(result.stdout)
            if 'dependencies' in data:
                for name, details in data['dependencies'].items():
                    packages.append(PackageInfo(
                        name=name,
                        version=details.get('version'),
                        manager='npm',
                        description=details.get('description')
                    ))
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Could not get npm packages: {e}", file=sys.stderr)
        return packages

    def _get_cargo_packages(self) -> List[PackageInfo]:
        packages = []
        try:
            result = subprocess.run(["cargo", "install", "--list"], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                if not line.startswith(" "):
                    parts = line.split()
                    name = parts[0]
                    version = parts[1].strip(":")
                    packages.append(PackageInfo(name=name, version=version, manager='cargo'))
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not get cargo packages: {e}", file=sys.stderr)
        return packages

    def _get_brew_packages(self) -> List[PackageInfo]:
        packages = []
        try:
            result = subprocess.run(["brew", "list", "--versions"], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                parts = line.split()
                name = parts[0]
                version = parts[1]
                packages.append(PackageInfo(name=name, version=version, manager='brew'))
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Could not get brew packages: {e}", file=sys.stderr)
        return packages

    

def main():
    auditor = PackageAuditor()
    filter_executables = True

    args = sys.argv[1:]
    if '--all' in args:
        filter_executables = False
        args.remove('--all')
    if '--executables' in args:
        filter_executables = True
        args.remove('--executables')

    if args:
        if args[0] == '--help':
            print("System Package Auditor - Find out WTF you've installed")
            print("\nUsage:")
            print("  python audit_packages.py                   # Audit executables only (default)")
            print("  python audit_packages.py --all             # Audit all packages")
            print("  python audit_packages.py --json            # Export executables to JSON")
            print("  python audit_packages.py --json --all      # Export all packages to JSON")
            print("  python audit_packages.py search <term>     # Search executables")
            print("  python audit_packages.py search <term> --all # Search all packages")
            print("  python audit_packages.py --help            # Show this help")
            return

        if args[0] == '--json':
            results = auditor.audit_system()
            auditor.print_summary(results, filter_executables=filter_executables)
            auditor.export_to_json(results, filter_executables=filter_executables)
            return

        if args[0] == 'search' and len(args) > 1:
            search_term = ' '.join(args[1:])
            results = auditor.audit_system()
            auditor.find_package(results, search_term, filter_executables=filter_executables)
            return

    results = auditor.audit_system()
    auditor.print_summary(results, filter_executables=filter_executables)

    # Ask if user wants to export
    # try:
    #     export = input("\nExport results to JSON? (y/n): ").lower().strip()
    #     if export == 'y':
    #         auditor.export_to_json(results, filter_executables=filter_executables)
    # except KeyboardInterrupt:
    #     print("\n\nAudit complete!")

if __name__ == "__main__":
    main()