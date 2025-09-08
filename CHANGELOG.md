# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of audit-packages-tool
- Modular architecture with separate scanner, reporting, and CLI modules
- Support for pip, npm, cargo, and brew package managers
- Intelligent executable vs library detection
- JSON export functionality
- Package search capability
- Comprehensive test suite with 90%+ coverage requirement
- CI/CD pipeline with multi-platform testing
- Professional documentation and README
- Type hints throughout codebase
- Static analysis with ruff and mypy

### Changed
- Migrated from single script to modular package architecture
- Updated CLI to use professional entry point (`audit-packages` command)
- Enhanced error handling and logging

### Security
- Added security scanning in CI/CD pipeline
- Implemented Dependabot for automated dependency updates
