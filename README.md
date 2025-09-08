# Audit Packages Tool 🔍

[![CI/CD Pipeline](https://github.com/maxrenke/audit-packages-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/maxrenke/audit-packages-tool/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/audit-packages-tool.svg)](https://badge.fury.io/py/audit-packages-tool)
[![Python versions](https://img.shields.io/pypi/pyversions/audit-packages-tool.svg)](https://pypi.org/project/audit-packages-tool/)
[![Coverage](https://codecov.io/gh/maxrenke/audit-packages-tool/branch/main/graph/badge.svg)](https://codecov.io/gh/maxrenke/audit-packages-tool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Professional system package auditor for multiple package managers - Built with modern Python practices and enterprise-grade tooling.**

Built by [**Max Renke**](https://www.maxrenke.com) | *Following the same engineering excellence demonstrated in [osv-vulnerability-scanner](https://github.com/maxrenke/osv-vulnerability-scanner)*

## 🚀 Quick Start

### Professional Installation
```bash
pip install audit-packages-tool
```

### Usage
```bash
# Scan all executable packages (default)
audit-packages

# Export results to JSON
audit-packages --json

# Search for specific packages
audit-packages search pytest

# Include all packages (not just executables)
audit-packages --all
```

## ✨ Enterprise Features

- **🏗️ Modular Architecture** - Clean separation of scanner, reporting, and CLI logic
- **📦 Multi-Manager Support** - pip, npm, cargo, brew, and more
- **🎯 Smart Detection** - Intelligent executable vs library classification
- **📊 Professional Output** - Human-readable summaries with JSON export
- **🔍 Search Capability** - Find packages by name or description
- **⚡ Modern Packaging** - Installable via pip with proper entry points
- **🧪 Comprehensive Testing** - 90%+ test coverage with CI/CD pipeline

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/maxrenke/audit-packages-tool
cd audit_packages_tool

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting and formatting
ruff check --fix
ruff format
mypy src/
```

## 📚 Package Manager Support

| Manager | Status | Description |
|---------|--------|--------------|
| **pip** | ✅ Full | Python packages with detailed metadata |
| **npm** | ✅ Full | Node.js global packages |
| **cargo** | ✅ Full | Rust packages via `cargo install` |
| **brew** | ✅ macOS | Homebrew packages (macOS only) |
| **winget** | 🚧 Planned | Windows Package Manager |
| **apt** | 🚧 Planned | Debian/Ubuntu packages |
| **yum** | 🚧 Planned | RHEL/CentOS packages |
| **snap** | 🚧 Planned | Universal Linux packages |
| **flatpak** | 🚧 Planned | Linux application distribution |

## 🏛️ Architecture

```
src/audit_packages_tool/
├── models/          # Data structures (PackageInfo, enums)
├── scanner/         # Package detection and auditing logic
├── reporting/       # Output formatting (console, JSON)
└── cli.py          # Command-line interface
```

## 🧪 Quality Assurance

- **Static Analysis**: ruff, mypy with strict typing
- **Testing**: pytest with 90%+ coverage requirement
- **CI/CD**: Multi-platform testing (Linux, Windows, macOS)
- **Security**: Dependabot, security scanning
- **Code Quality**: Pre-commit hooks, automated formatting

## 🤝 Contributing

We welcome contributions! This project follows modern Python development practices:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes with tests
4. **Ensure** all checks pass (`pytest`, `ruff`, `mypy`)
5. **Submit** a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 About the Developer

**Max Renke** | Software Engineer  
🌐 **Portfolio**: [maxrenke.com](https://www.maxrenke.com)  
🛡️ **Expertise**: Security tooling, API integration, modern Python architecture

> *"This tool demonstrates the same attention to engineering excellence and modern Python practices used in production security tools. It showcases professional development workflows, comprehensive testing, and maintainable architecture."*
