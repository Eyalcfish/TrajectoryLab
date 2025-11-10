# 🎨 Core Colors

PRIMARY_BLUE = "#3B82F6" # strong, modern blue (like Tailwind’s)
PRIMARY_LIGHT = "#60A5FA" # hover/highlight version
PRIMARY_DARK = "#1E40AF" # pressed or dark-theme accent

# ⚫ Neutrals / Background

BACKGROUND_DARK = "#0D0D0D" # near-black, not pure (#000) to avoid harsh contrast
CARD_SURFACE = "#1A1A1A" # slightly lighter for UI separation
BORDER_DIVIDER = "#2C2C2C" # border / divider color

# ⚪ Text & Highlights

PRIMARY_TEXT = "#FFFFFF" # pure white for clarity
SECONDARY_TEXT = "#B0B0B0" # muted gray for lower emphasis
ACCENT_WHITE = "#E6F0FF" # softer white that blends well with blue

# 🔵 Optional Accent Shades

INFO_HIGHLIGHT = "#38BDF8" # light cyan tint for hover effects
SUCCESS = "#22C55E" # green that fits blue contrast
SUCCESS_LIGHT = "#32D56E" # lighter green for hover
ERROR = "#EF4444" # bright red for alerts
ERROR_LIGHT = "#FF6B6B"
ERROR_DARK = "#D92A2A"
RED = ERROR # Alias for ERROR
TRANSPARENT = "transparent"

# 🟡 Amber/Warning
WARNING = "#FBBF24" # for non-critical alerts

# 🟣 Purple/Accent 2
ACCENT_2 = "#8B5CF6" # a secondary accent color


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
        "hover": BORDER_DIVIDER,
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
        "color": "#1F1F1F", # slightly different from card
    }
}