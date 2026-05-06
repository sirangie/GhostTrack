"""Banner and display utilities for GhostTrack."""

import sys
import os

# ANSI color codes
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
DIM     = "\033[2m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

# Fallback for non-color terminals
NO_COLOR = not sys.stdout.isatty() or os.environ.get("NO_COLOR")


def colorize(text: str, color: str) -> str:
    """Wrap text in an ANSI color code, or return plain text if colors are disabled."""
    if NO_COLOR:
        return text
    return f"{color}{text}{RESET}"


ASCII_BANNER = r"""
  ________.__                    __  ___________                     __
 /  _____/|  |__   ____  _______/  |_\__    ___/___________    ____ |  | __
/   \  ___|  |  \ /  _ \/  ___/\   __\|    |  \_  __ \__  \ _/ ___\|  |/ /
\    \_\  \   Y  (  <_> )___ \  |  |  |    |   |  | \// __ \\  \___|    <
 \______  /|___|  /\____/____  > |__|  |____|   |__|  (____  /\___  >__|_ \\n        \/      \/           \/                            \/     \/     \/
"""

VERSION = "1.0.0"
AUTHOR  = "GhostTrack Contributors"


def print_banner() -> None:
    """Print the ASCII art banner with version and author info."""
    # Try to read custom text from asset/text if it exists
    custom_text = _read_asset_text()

    print(colorize(ASCII_BANNER, CYAN))
    print(colorize(f"  Version : {VERSION}", GREEN))
    print(colorize(f"  Author  : {AUTHOR}", GREEN))
    if custom_text:
        print(colorize(f"  {custom_text}", DIM))
    print()


def _read_asset_text() -> str:
    """Read the first non-empty line from asset/text, if available."""
    asset_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "asset", "text"
    )
    try:
        with open(asset_path, "r") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    return line
    except (FileNotFoundError, IOError):
        pass
    return ""


def print_status(message: str, status: str = "info") -> None:
    """
    Print a formatted status message.

    Args:
        message: The message to display.
        status:  One of 'info', 'success', 'warning', 'error'.
    """
    icons = {
        "info":    ("[*]", CYAN),
        "success": ("[+]", GREEN),
        "warning": ("[!]", YELLOW),
        "error":   ("[-]", RED),
    }
    icon, color = icons.get(status, ("[*]", WHITE))
    print(colorize(f"{icon} {message}", color))


def print_result_line(label: str, value: str) -> None:
    """
    Print a single key-value result line with consistent formatting.

    Example output:
        IP Address   : 8.8.8.8
    """
    label_col = colorize(f"  {label:<16}", YELLOW)
    sep       = colorize(":", DIM)
    val_col   = colorize(f" {value}", WHITE)
    print(f"{label_col} {sep}{val_col}")


def print_separator(char: str = "-", width: int = 50) -> None:
    """Print a horizontal separator line."""
    print(colorize(char * width, DIM))
