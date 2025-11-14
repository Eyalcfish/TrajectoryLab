# 🎨 Core Colors (Visual Studio Dark Theme inspired)

PRIMARY_BLUE = "#007ACC"  # Visual Studio's signature blue
PRIMARY_LIGHT = "#008ACC" # Slightly lighter for hover
PRIMARY_DARK = "#005C99"  # Darker for pressed or accents
PRIMARY_BLUE_HOVER = "#008CFF"
PRIMARY_BLUE_PRESSED = "#006BB3"

PRIMARY_RED = "#D13438"
PRIMARY_RED_HOVER = "#E8484C"
PRIMARY_RED_PRESSED = "#A4262C"

# ⚫ Neutrals / Background

REALLY_DARK = "#1A1A1A"  # Very dark background
BACKGROUND_DARK = "#1E1E1E" # Main background, slightly lighter than current
CARD_SURFACE = "#252526"   # Card/panel background
BORDER_DIVIDER = "#333337" # Borders and dividers, slightly softer

# ⚪ Text & Highlights

PRIMARY_TEXT = "#F0F0F0" # Near-white for main text
SECONDARY_TEXT = "#AAAAAA" # Muted gray for secondary text
ACCENT_WHITE = "#FFFFFF" # Pure white for strong highlights

# 🔵 Optional Accent Shades

INFO_HIGHLIGHT = "#007ACC" # Using primary blue for info highlights
SUCCESS = "#388A34" # Green for success, adjusted for VS theme
SUCCESS_LIGHT = "#4CAF50"
ERROR = "#D13438" # Red for errors, adjusted for VS theme
ERROR_LIGHT = "#E8484C"
ERROR_DARK = "#A4262C"
RED = ERROR # Alias for ERROR
TRANSPARENT = "transparent"


JSON_NUMBER_COLOR = "#B5CEA8"      # Light green (for numbers, 123)
JSON_STRING_COLOR = "#CE9178"      # Rust/Orange (for "text in quotes")
JSON_PUNCTUATION_COLOR = "#569CD6" # Light blue (for {, }, [, ], :, ,)

# 🟡 Amber/Warning
WARNING = "#CC9900" # Amber for warnings

# 🟣 Purple/Accent 2
ACCENT_2 = "#6441A4" # A secondary accent color


# === UI Element Style Definitions ===

# Button Styles
BUTTON_STYLES = {
    "primary": {
        "background": PRIMARY_BLUE,
        "text": ACCENT_WHITE,
        "hover": PRIMARY_LIGHT,
        "pressed": PRIMARY_DARK,
        "border": PRIMARY_BLUE,
    },
    "secondary": {
        "background": CARD_SURFACE,
        "text": PRIMARY_TEXT,
        "hover": BORDER_DIVIDER, # Use border color for hover background
        "pressed": BACKGROUND_DARK,
        "border": BORDER_DIVIDER,
    },
    "danger": {
        "background": ERROR,
        "text": PRIMARY_TEXT,
        "hover": ERROR_LIGHT,
        "pressed": ERROR_DARK,
        "border": ERROR,
    },
    "success": {
        "background": SUCCESS,
        "text": ACCENT_WHITE,
        "hover": SUCCESS_LIGHT,
        "pressed": SUCCESS,
        "border": SUCCESS,
    }
}

# Background Styles
BACKGROUND_STYLES = {
    "main_window": {
        "color": BACKGROUND_DARK,
    },
    "card": {
        "color": CARD_SURFACE,
        "border": BORDER_DIVIDER,
    },
    "sidebar": {
        "color": "#252526", # Same as CARD_SURFACE for consistency with VS
    }
}