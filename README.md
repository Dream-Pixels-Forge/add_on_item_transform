# Item Transform Pro v2.0.0

A professional-grade Blender extension providing a comprehensive transform toolkit for 3D artists. Align, distribute, stack, randomize, and quick-transform objects with precision.

**Compatible with Blender 4.2+ and 5.x** (Extension system / manifest-based)

![Blender](https://img.shields.io/badge/Blender-4.2%2B%20%7C%205.x-orange)
![License](https://img.shields.io/badge/License-GPL--3.0-blue)

---

## What's New in v2.0.0

- **Full Blender 5.x compatibility** — Extension manifest-only (no legacy `bl_info`)
- **Multi-module architecture** — Clean, maintainable codebase
- **N-Panel (3D Viewport Sidebar)** — Fast access without leaving the viewport
- **Align Objects** — Align to min/max/center/cursor/active on any axis
- **Distribute Objects** — Even spacing or even centers along any axis
- **Randomize Transforms** — Seed-based randomization for location/rotation/scale
- **Copy Transform** — Copy transforms from active to selected
- **Mirror Placement** — Mirror objects across any axis
- **Stack with Gap** — Configurable gap between stacked objects
- **Improved operators** — Proper poll methods, EnumProperty, undo support
- **Addon Preferences** — Configurable pie menu key and panel location

---

## Features

### Quick Transform
- **Move** objects in 6 directions (±X, ±Y, ±Z) with configurable step
- **Rotate** around any axis with configurable angle
- **Scale** uniformly up/down with configurable percentage
- Intuitive button layout in the sidebar

### Align Objects
- Align to **Min**, **Max**, or **Center** of bounding boxes
- Align to **3D Cursor** or **Active Object**
- Works on X, Y, or Z axis independently

### Distribute Objects
- **Even Spacing** — Equal gaps between object bounds
- **Even Centers** — Equal distance between object centers
- Works with 3+ selected objects

### Stack Objects
- Stack objects along any axis (±X, ±Y, ±Z)
- Configurable **gap** between stacked items
- Automatic bounding-box-aware placement

### Randomize Transforms
- Randomize **location**, **rotation**, and/or **scale**
- **Seed-based** for reproducible results
- Per-axis control for location and rotation ranges
- Uniform or per-axis scale randomization

### Pivot / Origin Tools
- Set origin to **Center**, **Bottom**, **Top**, **3D Cursor**, or **Geometry Mass**
- Quick-access buttons in both panel and pie menu

### Utility Operations
- **Move to Ground** — Snap lowest point to Z=0
- **Move to Center** — Move to world origin (with optional "Keep Z")
- **Reset Transforms** — Selectively reset location/rotation/scale
- **Apply Transforms** — Selectively apply location/rotation/scale
- **Copy Transform** — Clone transform from active to all selected
- **Mirror Placement** — Mirror position across any axis
- **Purge Unused Data** — Clean orphaned data-blocks
- **Delete Hierarchy** — Remove objects and all children recursively
- **Duplicate Linked** — Create instanced duplicates

### Pie Menu
- Press **Shift+Alt+T** for quick access to all major features
- Organized into logical sections: Move, Rotate, Scale, Stack, Pivot, Utils

---

## Installation

### As Blender Extension (Recommended — Blender 4.2+)

1. Download the latest release `.zip` file
2. Open Blender → Edit → Preferences → Get Extensions
3. Drop-down menu → "Install from Disk..."
4. Select the `.zip` file
5. Enable the extension

### From Source

1. Clone or download this repository
2. Copy the `add_on_item_transform` folder to your Blender extensions directory
3. Enable in Preferences

---

## Usage

### N-Panel (3D Viewport Sidebar)
1. Press **N** in the 3D Viewport to open the sidebar
2. Find the **"Item Transform"** tab
3. Expand sub-panels: Quick Transform, Align & Distribute, Stack, Randomize, Pivot, Utilities

### Properties Panel
- Properties Editor → Object Properties → "Item Transform Pro" panel
- Shows active object info and quick action buttons

### Pie Menu
- **Shift+Alt+T** in Object Mode opens the pie menu
- Contains the most-used operations for fast workflow

### Preferences
- Edit → Preferences → Add-ons → Item Transform Pro
- Configure pie menu shortcut key
- Choose panel display location

---

## Project Structure

```
add_on_item_transform/
├── __init__.py              # Extension entry point
├── blender_manifest.toml    # Extension manifest (metadata)
├── properties.py            # All PropertyGroup definitions
├── preferences.py           # Addon preferences
├── panels.py                # UI panels (N-Panel + Properties)
├── pie_menu.py              # Pie menu + keymap registration
└── operators/
    ├── __init__.py          # Operators package
    ├── quick_transform.py   # Move/Rotate/Scale step operators
    ├── align.py             # Object alignment
    ├── distribute.py        # Object distribution
    ├── stack.py             # Object stacking
    ├── randomize.py         # Transform randomization
    ├── pivot.py             # Origin/pivot manipulation
    └── utilities.py         # Ground, center, reset, apply, etc.
```

---

## Requirements

- Blender 4.2.0 or newer (Extension system required)
- Fully compatible with Blender 5.0 and 5.1

---

## Author

**Dimona Patrick** — [Dream Pixels Forge](https://github.com/Dream-Pixels-Forge)

## License

[GPL-3.0-or-later](LICENSE)

## Contributing

Issues and pull requests are welcome! Please test with the latest Blender LTS and development builds.
