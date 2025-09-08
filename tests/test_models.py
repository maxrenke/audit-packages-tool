"""Tests for audit_packages_tool.models."""

import pytest

from audit_packages_tool.models import PackageInfo, PackageManager


class TestPackageInfo:
    """Tests for the PackageInfo dataclass."""

    def test_package_info_creation(self):
        """Test creating a valid PackageInfo instance."""
        pkg = PackageInfo(
            name="test-package",
            version="1.0.0",
            manager="pip",
            location="/some/path",
            description="A test package",
        )

        assert pkg.name == "test-package"
        assert pkg.version == "1.0.0"
        assert pkg.manager == "pip"
        assert pkg.location == "/some/path"
        assert pkg.description == "A test package"

    def test_package_info_minimal(self):
        """Test creating a PackageInfo with minimal required fields."""
        pkg = PackageInfo(name="minimal-package", version="2.0.0", manager="npm")

        assert pkg.name == "minimal-package"
        assert pkg.version == "2.0.0"
        assert pkg.manager == "npm"
        assert pkg.location is None
        assert pkg.size is None
        assert pkg.description is None

    def test_package_info_validation_empty_name(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            PackageInfo(name="", version="1.0.0", manager="pip")

    def test_package_info_validation_empty_version(self):
        """Test that empty version raises ValueError."""
        with pytest.raises(ValueError, match="Package version cannot be empty"):
            PackageInfo(name="test", version="", manager="pip")

    def test_package_info_validation_empty_manager(self):
        """Test that empty manager raises ValueError."""
        with pytest.raises(ValueError, match="Package manager cannot be empty"):
            PackageInfo(name="test", version="1.0.0", manager="")


class TestPackageManager:
    """Tests for the PackageManager enum."""

    def test_package_manager_values(self):
        """Test that all expected package managers are available."""
        expected_managers = {
            "pip",
            "npm",
            "cargo",
            "brew",
            "winget",
            "apt",
            "yum",
            "snap",
            "flatpak",
        }

        actual_managers = {pm.value for pm in PackageManager}
        assert actual_managers == expected_managers

    def test_package_manager_access(self):
        """Test accessing specific package managers."""
        assert PackageManager.PIP.value == "pip"
        assert PackageManager.NPM.value == "npm"
        assert PackageManager.CARGO.value == "cargo"
        assert PackageManager.BREW.value == "brew"
