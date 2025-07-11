# System Package Auditor

`audit_packages.py` is a Python script designed to audit and list installed packages from various package managers on your system. It provides a summary of packages, focusing on those that are likely executable or CLI tools.

This is a starter script and we welcome contributions to expand its functionality to other package managers.

## Contributing

We welcome contributions to this project! If you're interested in helping, please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to get started.

## Usage

To run the script, navigate to its directory in your terminal and execute:

```bash
python audit_packages.py
```

By default, the script will audit and display only executable packages. You can use the following flags to modify its behavior:

-   `python audit_packages.py --all`: Audit and display all packages, regardless of whether they are considered executable.
-   `python audit_packages.py --json`: Export the audit results (executables only by default) to a JSON file (`system_packages.json`).
-   `python audit_packages.py --json --all`: Export all packages to a JSON file.
-   `python audit_packages.py search <term>`: Search for a specific package by name or description among executables.
-   `python audit_packages.py search <term> --all`: Search for a specific package among all installed packages.
-   `python audit_packages.py --help`: Display the help message.

## Current Supported Package Managers

-   `pip` (Python packages)
-   `npm` (Node.js packages)
-   `cargo` (Rust packages)

## Possible Improvements

-   **Expand Package Manager Support:** Implement robust parsing for `brew`, `scoop`, `winget`, `apt`, `yum`, `snap`, `flatpak`, and other relevant package managers.
-   **Enhanced Package Details:** Extract more comprehensive information (e.g., installation date, dependencies, license) for all supported package types.
-   **Improved Executable Detection:** Develop more sophisticated methods for identifying executable packages, possibly by checking common installation paths or manifest files.
-   **Configuration File:** Allow users to configure which package managers to audit and define custom executable heuristics via a configuration file.
-   **Interactive Mode:** Reintroduce an interactive mode for easier navigation and filtering of results.
-   **GUI/Web Interface:** Develop a graphical user interface or a simple web interface for better usability and visualization of audit results.
