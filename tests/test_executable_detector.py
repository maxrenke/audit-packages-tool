"""Tests for audit_packages_tool.scanner.executable_detector."""

from unittest.mock import patch

from audit_packages_tool.models import PackageInfo
from audit_packages_tool.scanner.executable_detector import ExecutableDetector


class TestExecutableDetector:
    """Tests for the ExecutableDetector class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = ExecutableDetector()

    def test_cargo_package_is_executable(self):
        """Test that cargo packages are considered executable."""
        pkg = PackageInfo(name="ripgrep", version="1.0.0", manager="cargo")
        assert self.detector.is_executable_package(pkg) is True

    def test_npm_package_is_executable(self):
        """Test that npm packages are considered executable."""
        pkg = PackageInfo(name="webpack", version="5.0.0", manager="npm")
        assert self.detector.is_executable_package(pkg) is True

    def test_brew_package_is_executable(self):
        """Test that brew packages are considered executable."""
        pkg = PackageInfo(name="git", version="2.30.0", manager="brew")
        assert self.detector.is_executable_package(pkg) is True

    def test_snap_package_is_executable(self):
        """Test that snap packages are considered executable."""
        pkg = PackageInfo(name="code", version="1.60.0", manager="snap")
        assert self.detector.is_executable_package(pkg) is True

    def test_flatpak_package_is_executable(self):
        """Test that flatpak packages are considered executable."""
        pkg = PackageInfo(name="org.firefox.Firefox", version="90.0", manager="flatpak")
        assert self.detector.is_executable_package(pkg) is True

    def test_package_in_bin_directory(self):
        """Test that packages in bin directories are considered executable."""
        pkg = PackageInfo(
            name="python-package",
            version="1.0.0",
            manager="pip",
            location="/usr/local/bin/some-tool",
        )
        assert self.detector.is_executable_package(pkg) is True

    def test_package_in_windows_bin_directory(self):
        """Test that packages in Windows bin directories are considered executable."""
        pkg = PackageInfo(
            name="python-package",
            version="1.0.0",
            manager="pip",
            location="C:\\\\Program Files\\\\Python\\\\Scripts\\\\bin\\\\tool.exe",
        )
        assert self.detector.is_executable_package(pkg) is True

    def test_package_ending_with_bin(self):
        """Test that packages with locations ending in bin are considered executable."""
        pkg = PackageInfo(
            name="python-package",
            version="1.0.0",
            manager="pip",
            location="/usr/local/bin",
        )
        assert self.detector.is_executable_package(pkg) is True

    @patch("shutil.which")
    def test_pip_package_available_in_path(self, mock_which):
        """Test that pip packages available in PATH are considered executable."""
        mock_which.return_value = "/usr/local/bin/pytest"

        pkg = PackageInfo(name="pytest", version="6.0.0", manager="pip")
        assert self.detector.is_executable_package(pkg) is True
        mock_which.assert_called_once_with("pytest")

    @patch("shutil.which")
    def test_pip_package_not_available_in_path(self, mock_which):
        """Test that pip packages not available in PATH are not considered executable."""
        mock_which.return_value = None

        pkg = PackageInfo(name="requests", version="2.25.1", manager="pip")
        assert self.detector.is_executable_package(pkg) is False
        mock_which.assert_called_once_with("requests")

    def test_regular_library_package(self):
        """Test that regular library packages are not considered executable."""
        pkg = PackageInfo(
            name="requests",
            version="2.25.1",
            manager="pip",
            location="/usr/local/lib/python3.9/site-packages",
        )

        with patch("shutil.which", return_value=None):
            assert self.detector.is_executable_package(pkg) is False

    def test_unknown_manager(self):
        """Test that packages from unknown managers are not considered executable."""
        pkg = PackageInfo(name="unknown-package", version="1.0.0", manager="unknown")

        with patch("shutil.which", return_value=None):
            assert self.detector.is_executable_package(pkg) is False
