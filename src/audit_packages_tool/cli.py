"""
Command-line interface for audit_packages_tool.

Provides a clean, user-friendly CLI for package auditing.
"""

import sys

from .reporting import ConsoleReporter, JSONExporter
from .scanner import PackageAuditor


def main() -> None:
    """Main entry point for the CLI."""
    auditor = PackageAuditor()
    console_reporter = ConsoleReporter()
    json_exporter = JSONExporter()

    filter_executables = True

    args = sys.argv[1:]
    if "--all" in args:
        filter_executables = False
        args.remove("--all")
    if "--executables" in args:
        filter_executables = True
        args.remove("--executables")

    if args:
        if args[0] == "--help":
            print_help()
            return

        if args[0] == "--json":
            results = auditor.audit_system()
            console_reporter.print_summary(
                results, filter_executables=filter_executables
            )
            json_exporter.export_to_json(results, filter_executables=filter_executables)
            return

        if args[0] == "search" and len(args) > 1:
            search_term = " ".join(args[1:])
            results = auditor.audit_system()
            found_packages = auditor.find_packages(
                results, search_term, filter_executables=filter_executables
            )
            console_reporter.print_search_results(found_packages, search_term)
            return

    # Default: run audit and print summary
    results = auditor.audit_system()
    console_reporter.print_summary(results, filter_executables=filter_executables)


def print_help() -> None:
    """Print help information."""
    print("System Package Auditor - Find out WTF you've installed")
    print("\nUsage:")
    print(
        "  python -m audit_packages_tool                   # Audit executables only (default)"
    )
    print("  python -m audit_packages_tool --all             # Audit all packages")
    print(
        "  python -m audit_packages_tool --json            # Export executables to JSON"
    )
    print(
        "  python -m audit_packages_tool --json --all      # Export all packages to JSON"
    )
    print("  python -m audit_packages_tool search <term>     # Search executables")
    print("  python -m audit_packages_tool search <term> --all # Search all packages")
    print("  python -m audit_packages_tool --help            # Show this help")


if __name__ == "__main__":
    main()
