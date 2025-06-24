# Scribe Text Editor

A lightweight, multi-tab text editor built with Python and Tkinter, featuring a clean interface and essential text editing capabilities.

## Features

### Core Functionality
- **Multi-tab support** - Work with multiple files simultaneously
- **File operations** - New, Open, Save, Save As
- **Text editing** - Cut, Copy, Paste, Undo, Redo
- **Search capabilities** - Find text, Find & Replace
- **Navigation** - Go to specific line numbers
- **Line numbers** - Sidebar showing line numbers for easy reference

### View Options
- **Zoom controls** - Zoom in, zoom out, and reset zoom
- **Theme support** - Light, Dark, and Auto themes
- **Font customization** - Adjustable font sizes (6-72pt)

### User Interface
- Clean, intuitive tabbed interface
- Synchronized scrolling between text and line numbers
- Visual indicators for unsaved changes (asterisk in tab title)
- Keyboard shortcuts for common operations

## Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included with Python)

### Setup
1. Clone or download the project files
2. Ensure `Main.py` is in your project directory
3. (Optional) Add `Placeholder.png` in the same directory for a custom app icon

### Running the Application
```bash
python Main.py
```

## Usage

### File Operations
- **New Tab**: `Ctrl+N` or File → New Tab
- **Open File**: `Ctrl+O` or File → Open...
- **Save**: `Ctrl+S` or File → Save
- **Save As**: File → Save As...
- **Close Tab**: `Ctrl+W` or File → Close Tab

### Editing
- **Undo**: `Ctrl+Z` or Edit → Undo
- **Redo**: `Ctrl+Y` or Edit → Redo
- **Cut**: `Ctrl+X` or Edit → Cut
- **Copy**: `Ctrl+C` or Edit → Copy
- **Paste**: `Ctrl+V` or Edit → Paste
- **Select All**: `Ctrl+A` or Edit → Select All

### Search & Navigation
- **Find**: `Ctrl+F` or Edit → Find
- **Find & Replace**: `Ctrl+H` or Edit → Find & Replace
- **Go to Line**: `Ctrl+G` or Edit → Go To Line...

### View Options
- **Zoom In**: `Ctrl++` or View → Zoom In
- **Zoom Out**: `Ctrl+-` or View → Zoom Out
- **Reset Zoom**: `Ctrl+0` or View → Reset Zoom
- **Change Theme**: View → Theme → [Light/Dark/Auto]

## Supported File Types

- Text files (`.txt`)
- Python files (`.py`)
- All file types (`*.*`)

## Themes

- **Light Theme**: Traditional light background with dark text
- **Dark Theme**: Dark background with light text for reduced eye strain
- **Auto Theme**: Automatically selects theme based on system (currently defaults to Dark on macOS, Light on other systems)

## Technical Details

### Architecture
- Built with Python's Tkinter GUI framework
- Object-oriented design with `TabData` class for managing individual tabs
- Event-driven architecture for real-time updates

### Key Components
- **Tab Management**: Dynamic creation and management of multiple tabs
- **Line Numbers**: Synchronized sidebar showing current line numbers
- **Theme System**: Configurable color schemes
- **Font Management**: Scalable font sizing across all tabs

## Planned Features (TODO)

- [ ] Plus and minus buttons on tab bar for quick tab creation/closing
- [ ] Custom app icon integration (Placeholder.png → .ico conversion)
- [ ] Enhanced auto-theme detection for better system integration

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.6+
- **Memory**: Minimal (typical text editor usage)
- **Storage**: ~50KB for application files

## Keyboard Shortcuts Reference

| Action | Shortcut |
|--------|----------|
| New Tab | `Ctrl+N` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Close Tab | `Ctrl+W` |
| Find | `Ctrl+F` |
| Find & Replace | `Ctrl+H` |
| Go to Line | `Ctrl+G` |
| Select All | `Ctrl+A` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Zoom In | `Ctrl++` |
| Zoom Out | `Ctrl+-` |
| Reset Zoom | `Ctrl+0` |

## Contributing

This is a personal project, but suggestions and improvements are welcome. The code is well-commented and structured for easy modification and extension.

## License

This project is provided as-is for educational and personal use.

---
