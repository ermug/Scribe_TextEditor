##todo##
# Add plus and minus buttons on the tabs bar to quickly open and close them
# Use Placeholder.png as the icon of the app (This should be in the same directory as the main.py file) ✓

# Import tkinter and submodules for GUI elements and dialogs
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import platform
import os

# Create the main application window
root = tk.Tk()  # Initialize the main window using tkinter
root.title("Scribe")  # Set the title of the window to 'Scribe'
root.geometry("800x600")  # Set the default size of the window

# Try to set the application icon (Placeholder.png should be in same directory)
try:
    icon_path = os.path.join(os.path.dirname(__file__), "Placeholder.png")
    if os.path.exists(icon_path):
        root.iconphoto(False, tk.PhotoImage(file=icon_path))  # Set app icon
except Exception:
    pass  # Continue without icon if it fails to load

# Set default font size
font_size = 12  # Starting font size for the text widget

# Track current theme
current_theme = "Light"  # Default theme is Light

# Tab management variables - for multi-tab support
tabs = {}  # Dictionary to store tab data (text widgets, file paths, etc.)
current_tab_id = None  # Currently active tab ID
tab_counter = 0  # Counter for creating unique tab IDs

# Create notebook widget for tabs
notebook = ttk.Notebook(root)  # Notebook widget to hold multiple tabs
notebook.pack(fill="both", expand=True, padx=5, pady=5)  # Fill window and expand


class TabData:
    """Class to store all data for each individual tab"""

    def __init__(self, tab_id):
        self.id = tab_id  # Unique identifier for this tab
        self.file_path = None  # Path to currently open file (None by default)
        self.text_widget = None  # The main text editing widget
        self.line_numbers = None  # Line numbers sidebar widget
        self.scrollbar = None  # Vertical scrollbar widget
        self.text_frame = None  # Frame containing text widget and line numbers
        self.modified = False  # Track if file has unsaved changes


def create_new_tab(file_path=None, content=""):
    """Create a new tab with complete text editor functionality"""
    global tab_counter, current_tab_id

    tab_counter += 1  # Increment counter for unique tab ID
    tab_id = f"tab_{tab_counter}"  # Create unique tab identifier

    # Create tab frame to hold all tab contents
    tab_frame = ttk.Frame(notebook)  # Main frame for this tab

    # Create a frame to hold the line numbers and text widget
    text_frame = tk.Frame(tab_frame)  # Frame to group line numbers and text box
    text_frame.pack(fill="both", expand=True)  # Fill window and expand with resizing

    # Line number sidebar
    line_numbers = tk.Text(text_frame, width=4, padx=4, takefocus=0, border=0,
                           background="#eeeeee", state="disabled", wrap="none",
                           font=("Courier New", font_size))  # Line numbers pane with same font size as text
    line_numbers.pack(side="left", fill="y")  # Attach to the left, fill vertically

    # Scrollbar for the text widget
    scrollbar = tk.Scrollbar(text_frame)  # Vertical scrollbar widget
    scrollbar.pack(side="right", fill="y")  # Attach to the right, fill vertically

    # Create a resizable text box where the user can type text
    text_widget = tk.Text(text_frame, wrap=tk.WORD, undo=True, yscrollcommand=scrollbar.set,
                          font=("Courier New",
                                font_size))  # Add word-wrapped Text widget with undo enabled and custom font size
    text_widget.pack(fill="both", expand=True)  # Fill entire frame with expanding

    scrollbar.config(command=text_widget.yview)  # Connect scrollbar to text widget scrolling

    # Create tab data object to store all tab information
    tab_data = TabData(tab_id)
    tab_data.text_widget = text_widget
    tab_data.line_numbers = line_numbers
    tab_data.scrollbar = scrollbar
    tab_data.text_frame = text_frame
    tab_data.file_path = file_path

    # Store tab data in global dictionary
    tabs[tab_id] = tab_data

    # Set up text widget events for this tab (scrolling, line numbers, etc.)
    setup_tab_events(tab_data)

    # Insert content if provided (for opening existing files)
    if content:
        text_widget.insert("1.0", content)  # Insert file content at beginning

    # Determine tab title based on file path or create default name
    if file_path:
        tab_title = os.path.basename(file_path)  # Use filename as tab title
    else:
        tab_title = f"Untitled {tab_counter}"  # Default name for new files

    # Add tab to notebook widget
    notebook.add(tab_frame, text=tab_title)  # Add tab with title
    notebook.select(tab_frame)  # Select the newly created tab

    # Set as current active tab
    current_tab_id = tab_id

    # Apply current theme to new tab
    apply_theme_to_tab(tab_data, current_theme)

    # Update line numbers for the new tab
    update_line_numbers_for_tab(tab_data)

    return tab_id  # Return tab ID for reference


def setup_tab_events(tab_data):
    """Set up all event handlers for a tab's text widget"""
    text_widget = tab_data.text_widget

    # Synchronize scrolling between text widget and line numbers
    def sync_scroll(*args):
        """Synchronize scrolling between the main text widget and line numbers"""
        tab_data.line_numbers.yview_moveto(args[0])  # Move line numbers to same position
        tab_data.scrollbar.set(*args)  # Update scrollbar position

    text_widget.config(yscrollcommand=sync_scroll)  # Set scroll synchronization

    # Bind line number updates to relevant events
    text_widget.bind("<KeyRelease>",
                     lambda e: update_line_numbers_for_tab(tab_data))  # Update line numbers when keys released
    text_widget.bind("<MouseWheel>",
                     lambda e: update_line_numbers_for_tab(tab_data))  # Update line numbers on scroll wheel (Windows)
    text_widget.bind("<Button-4>", lambda e: update_line_numbers_for_tab(tab_data))  # Linux scroll up
    text_widget.bind("<Button-5>", lambda e: update_line_numbers_for_tab(tab_data))  # Linux scroll down
    text_widget.bind("<Button-1>", lambda e: update_line_numbers_for_tab(tab_data))  # Update on mouse click

    # Track modifications to show unsaved changes
    def on_text_change(event):
        """Mark tab as modified when text changes"""
        tab_data.modified = True  # Mark as having unsaved changes
        update_tab_title(tab_data)  # Update tab title to show modification

    text_widget.bind("<KeyPress>", on_text_change)  # Track any key press as modification


def update_line_numbers_for_tab(tab_data):
    """Update line numbers in the sidebar for a specific tab"""
    if not tab_data or not tab_data.line_numbers or not tab_data.text_widget:
        return  # Exit if tab data is invalid

    tab_data.line_numbers.config(state="normal")  # Enable editing to update line numbers
    tab_data.line_numbers.delete("1.0", "end")  # Clear current line numbers
    line_count = int(tab_data.text_widget.index('end-1c').split('.')[0])  # Get number of lines in text widget
    line_content = "\n".join(str(i) for i in range(1, line_count + 1))  # Prepare line numbers string
    tab_data.line_numbers.insert("1.0", line_content)  # Insert line numbers
    tab_data.line_numbers.config(state="disabled")  # Disable editing again


def get_current_tab():
    """Get the currently active tab data object"""
    try:
        current_frame = notebook.nametowidget(notebook.select())  # Get currently selected tab frame
        # Find matching tab data by comparing frames
        for tab_id, tab_data in tabs.items():
            if tab_data.text_frame.master == current_frame:
                return tab_data  # Return the matching tab data
    except:
        pass  # Handle any errors gracefully
    return None  # Return None if no current tab found


def update_tab_title(tab_data, saved=False):
    """Update the title of a tab to show filename and modification status"""
    try:
        # Find the tab frame
        tab_frame = tab_data.text_frame.master
        tab_index = None

        # Find the index of this tab in the notebook
        for i in range(notebook.index("end")):
            if notebook.nametowidget(notebook.tabs()[i]) == tab_frame:
                tab_index = i
                break

        if tab_index is not None:
            # Determine title based on file path
            if tab_data.file_path:
                title = os.path.basename(tab_data.file_path)  # Use filename
                if not saved:
                    root.title(f"Scribe - {title}")  # Update main window title
            else:
                title = f"Untitled {tab_data.id.split('_')[1]}"  # Use default name
                root.title(f"Scribe - {title}")  # Update main window title

            # Add asterisk if modified and not saved
            if tab_data.modified and not saved:
                title += "*"  # Indicate unsaved changes

            notebook.tab(tab_index, text=title)  # Update tab title in notebook
    except Exception:
        pass  # Handle errors gracefully


def close_tab():
    """Close the current tab with save confirmation if needed"""
    current_tab = get_current_tab()
    if not current_tab:
        return  # Exit if no current tab

    # Check if file is modified and ask to save
    if current_tab.modified:
        title = "Untitled" if not current_tab.file_path else os.path.basename(current_tab.file_path)
        response = messagebox.askyesnocancel("Save Changes", f"Save changes to {title}?")
        if response is True:  # Yes, save
            save_current_tab()
        elif response is None:  # Cancel
            return  # Don't close tab

    # Remove tab from notebook and tabs dictionary
    try:
        tab_frame = current_tab.text_frame.master
        notebook.forget(tab_frame)  # Remove tab from notebook
        del tabs[current_tab.id]  # Remove from tabs dictionary

        # If no tabs left, create a new one
        if len(tabs) == 0:
            create_new_tab()  # Always have at least one tab open
        else:
            # Update current tab reference
            current_tab = get_current_tab()
    except Exception:
        pass  # Handle errors gracefully


def save_current_tab():
    """Save the content of the current tab to its file"""
    current_tab = get_current_tab()
    if not current_tab:
        return  # Exit if no current tab

    if current_tab.file_path:  # If a file is already associated with this tab
        try:
            content = current_tab.text_widget.get("1.0", "end-1c")  # Get all text from the text widget
            with open(current_tab.file_path, "w", encoding="utf-8") as file:  # Open the file in write mode
                file.write(content)  # Write the current text to the file
            current_tab.modified = False  # Mark as saved
            update_tab_title(current_tab, saved=True)  # Update tab title
            messagebox.showinfo("Save", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
    else:
        saveas_current_tab()  # If no file associated, prompt for "Save As"


def saveas_current_tab():
    """Save current tab as a new file"""
    current_tab = get_current_tab()
    if not current_tab:
        return  # Exit if no current tab

    file_path = filedialog.asksaveasfilename(  # Prompt the user to choose a save location
        defaultextension=".txt",  # Default file extension is .txt
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]  # Allow .txt and all file types
    )
    if file_path:  # If user didn't cancel the dialog
        try:
            current_tab.file_path = file_path  # Store the selected path
            content = current_tab.text_widget.get("1.0", "end-1c")  # Get current text content
            with open(file_path, "w", encoding="utf-8") as file:  # Open file for writing
                file.write(content)  # Write text to file
            current_tab.modified = False  # Mark as saved
            update_tab_title(current_tab, saved=True)  # Update tab title with new filename
            messagebox.showinfo("Save As", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")


# Function to open a file and load its contents in a new tab
def open_file():
    """Open a file and load its contents into a new tab"""
    file_path = filedialog.askopenfilename(  # Prompt user to choose a file to open
        filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
    )
    if file_path:  # If user selected a file
        try:
            with open(file_path, "r", encoding="utf-8") as file:  # Open the file in read mode
                content = file.read()  # Read the file content
            create_new_tab(file_path, content)  # Create new tab with file content
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")


def new_file():
    """Create a new file in a new tab"""
    create_new_tab()  # Create a new empty tab


# Wrapper functions for current tab operations - these maintain compatibility with original code

# Function to save the content to the currently open file
def save():
    """Save the current tab (wrapper for backward compatibility)"""
    save_current_tab()


# Function to save the content as a new file
def saveas():
    """Save current tab as new file (wrapper for backward compatibility)"""
    saveas_current_tab()


# Function to undo the last change
def undo():
    """Undo the last change in current tab"""
    current_tab = get_current_tab()
    if current_tab:
        try:
            current_tab.text_widget.event_generate("<<Undo>>")  # Trigger the built-in undo event
        except tk.TclError:
            pass  # Nothing to undo


# Function to redo the last undone change
def redo():
    """Redo the last undone change in current tab"""
    current_tab = get_current_tab()
    if current_tab:
        try:
            current_tab.text_widget.event_generate("<<Redo>>")  # Trigger the built-in redo event
        except tk.TclError:
            pass  # Nothing to redo


# Function to cut selected text
def cut():
    """Cut selected text from current tab"""
    current_tab = get_current_tab()
    if current_tab:
        try:
            current_tab.text_widget.event_generate("<<Cut>>")  # Trigger the built-in cut event
        except tk.TclError:
            pass  # Nothing selected


# Function to copy selected text
def copy():
    """Copy selected text from current tab"""
    current_tab = get_current_tab()
    if current_tab:
        try:
            current_tab.text_widget.event_generate("<<Copy>>")  # Trigger the built-in copy event
        except tk.TclError:
            pass  # Nothing selected


# Function to paste text from clipboard
def paste():
    """Paste text from clipboard into current tab"""
    current_tab = get_current_tab()
    if current_tab:
        try:
            current_tab.text_widget.event_generate("<<Paste>>")  # Trigger the built-in paste event
            update_line_numbers_for_tab(current_tab)  # Update line numbers after paste
        except tk.TclError:
            pass  # Nothing to paste


# Function to select all text in the text box
def select_all():
    """Select all text in current tab"""
    current_tab = get_current_tab()
    if current_tab:
        current_tab.text_widget.tag_add(tk.SEL, "1.0", tk.END)  # Select text from start to end
        current_tab.text_widget.mark_set(tk.INSERT, "1.0")  # Set cursor at start
        current_tab.text_widget.see(tk.INSERT)  # Ensure selected area is visible


# Function to find and replace text in the document
def find_replace():
    """Find and replace text in the current tab"""
    current_tab = get_current_tab()
    if not current_tab:
        return  # Exit if no current tab

    find_text = simpledialog.askstring("Find", "Text to find:")  # Ask user what to find
    if find_text is None or find_text == "":
        return  # Cancel if input is empty
    replace_text = simpledialog.askstring("Replace", "Replace with:")  # Ask what to replace with
    if replace_text is None:
        return  # Cancel if input is empty

    content = current_tab.text_widget.get("1.0", "end-1c")  # Get full text content
    if find_text in content:
        new_content = content.replace(find_text, replace_text)  # Replace all occurrences
        current_tab.text_widget.delete("1.0", tk.END)  # Clear old text
        current_tab.text_widget.insert("1.0", new_content)  # Insert updated text
        update_line_numbers_for_tab(current_tab)  # Update line numbers
        count = content.count(find_text)
        messagebox.showinfo("Find & Replace", f"Replaced {count} occurrence(s) of '{find_text}'.")
    else:
        messagebox.showinfo("Find & Replace", f"Text '{find_text}' not found.")


# Function to jump to a specific line number
def goto_line():
    """Jump to a specific line number in current tab"""
    current_tab = get_current_tab()
    if not current_tab:
        return  # Exit if no current tab

    line = simpledialog.askinteger("Go To Line", "Enter line number:")  # Ask for line number
    if line and line > 0:  # If a valid positive number is entered
        try:
            index = f"{line}.0"  # Format it as a text index
            current_tab.text_widget.mark_set(tk.INSERT, index)  # Move cursor to that line
            current_tab.text_widget.see(index)  # Scroll to show that line
        except tk.TclError:
            messagebox.showerror("Error", f"Line {line} does not exist.")


# Function to find and highlight text in the document
def find_text():
    """Find and highlight text in the current tab"""
    current_tab = get_current_tab()
    if not current_tab:
        return  # Exit if no current tab

    # Ask the user for the text they want to search for
    query = simpledialog.askstring("Find", "Enter text to find:")
    if not query:
        return  # Exit if user cancels or provides no input

    text_widget = current_tab.text_widget
    text_widget.tag_remove("highlight", "1.0", tk.END)  # Clear previous highlights

    # Start from the top and search forward
    start_pos = "1.0"
    count = 0
    while True:
        start_pos = text_widget.search(query, start_pos, stopindex=tk.END, nocase=True)
        if not start_pos:
            break  # No more matches
        end_pos = f"{start_pos}+{len(query)}c"  # Calculate the end position of the match
        text_widget.tag_add("highlight", start_pos, end_pos)  # Highlight the matched text
        start_pos = end_pos  # Move past the last match
        count += 1

    # Define highlight appearance (yellow background)
    text_widget.tag_config("highlight", background="yellow", foreground="black")

    # Show message with count
    if count == 0:
        messagebox.showinfo("Find", "No matches found.")
    else:
        messagebox.showinfo("Find", f"Found {count} match(es).")


# --- View Features ---

# Increase font size for zoom in
def zoom_in():
    """Increase font size for zoom in across all tabs"""
    global font_size
    if font_size < 72:  # Maximum font size limit
        font_size += 1  # Increase font size
        apply_font_size_to_all_tabs()  # Apply to all open tabs


# Decrease font size for zoom out
def zoom_out():
    """Decrease font size for zoom out across all tabs"""
    global font_size
    if font_size > 6:  # Minimum font size limit
        font_size -= 1  # Decrease font size
        apply_font_size_to_all_tabs()  # Apply to all open tabs


# Reset zoom to default size
def reset_zoom():
    """Reset zoom to default size across all tabs"""
    global font_size
    font_size = 12  # Reset to default font size
    apply_font_size_to_all_tabs()  # Apply to all open tabs


def apply_font_size_to_all_tabs():
    """Apply current font size to all open tabs"""
    for tab_data in tabs.values():
        tab_data.text_widget.config(font=("Courier New", font_size))  # Apply new font size to text
        tab_data.line_numbers.config(font=("Courier New", font_size))  # Update line numbers font to match
        update_line_numbers_for_tab(tab_data)  # Update line numbers display


def apply_theme_to_tab(tab_data, theme):
    """Apply theme colors to a specific tab"""
    # Determine actual theme (resolve "Auto" to specific theme)
    actual_theme = theme
    if theme == "Auto":
        if platform.system() == "Darwin":  # macOS
            actual_theme = "Dark"  # Simple heuristic - could be improved with actual system detection
        else:
            actual_theme = "Light"  # Default light theme for others

    # Apply theme colors
    if actual_theme == "Dark":
        tab_data.text_frame.config(bg="#2d2d2d")  # Set frame background
        tab_data.text_widget.config(bg="#1e1e1e", fg="#dcdcdc",
                                    insertbackground="white")  # Dark background and light text
        tab_data.line_numbers.config(bg="#2d2d2d", fg="#aaa")  # Dark line number background
    else:
        tab_data.text_frame.config(bg="SystemButtonFace")  # Default frame background
        tab_data.text_widget.config(bg="white", fg="black", insertbackground="black")  # Light theme colors
        tab_data.line_numbers.config(bg="#eeeeee", fg="black")  # Light line number background


# Apply light, dark or automatic theme
def apply_theme(theme):
    """Apply theme to entire application and all tabs"""
    global current_theme
    current_theme = theme

    # Determine actual theme (resolve "Auto" to specific theme)
    actual_theme = theme
    if theme == "Auto":
        if platform.system() == "Darwin":  # macOS
            # Simple heuristic - could be improved with actual system detection
            actual_theme = "Dark"
        else:
            actual_theme = "Light"  # Default light theme for others

    # Apply to root window
    if actual_theme == "Dark":
        root.config(bg="#2d2d2d")  # Set root background
    else:
        root.config(bg="SystemButtonFace")  # Default system background

    # Apply to all open tabs
    for tab_data in tabs.values():
        apply_theme_to_tab(tab_data, theme)


# --- Menu Bar Setup ---

menu_bar = tk.Menu(root)  # Create the menu bar

# Create the "File" drop-down menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # Create a submenu under File
file_menu.add_command(label="New Tab", command=new_file, accelerator="Ctrl+N")  # Add 'New' option
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")  # Add accelerator
file_menu.add_separator()  # Add separator line
file_menu.add_command(label="Save", command=save, accelerator="Ctrl+S")  # Add accelerator
file_menu.add_command(label="Save As...", command=saveas)  # Add 'Save As' option
file_menu.add_separator()  # Add separator line
file_menu.add_command(label="Close Tab", command=close_tab, accelerator="Ctrl+W")  # Add 'Close Tab' option
file_menu.add_separator()  # Add separator line
file_menu.add_command(label="Exit", command=root.quit)  # Add 'Exit' option
menu_bar.add_cascade(label="File", menu=file_menu)  # Add File menu to the menu bar

# Create the "Edit" drop-down menu
edit_menu = tk.Menu(menu_bar, tearoff=0)  # Create a submenu under Edit
edit_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")  # Undo option
edit_menu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")  # Redo option
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")  # Cut option
edit_menu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")  # Copy option
edit_menu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")  # Paste option
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text, accelerator="Ctrl+F")  # Find text
edit_menu.add_command(label="Find & Replace", command=find_replace, accelerator="Ctrl+H")  # Find & Replace
edit_menu.add_command(label="Go To Line...", command=goto_line, accelerator="Ctrl+G")  # Go to specific line
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")  # Select all
menu_bar.add_cascade(label="Edit", menu=edit_menu)  # Add Edit menu to menu bar

# Create the "View" drop-down menu
view_menu = tk.Menu(menu_bar, tearoff=0)  # Create submenu for View
view_menu.add_command(label="Zoom In", command=zoom_in, accelerator="Ctrl++")  # Zoom in option
view_menu.add_command(label="Zoom Out", command=zoom_out, accelerator="Ctrl+-")  # Zoom out option
view_menu.add_command(label="Reset Zoom", command=reset_zoom, accelerator="Ctrl+0")  # Reset zoom option

# Submenu for themes under View
theme_menu = tk.Menu(view_menu, tearoff=0)  # Create theme submenu
theme_menu.add_command(label="Light", command=lambda: apply_theme("Light"))  # Light theme
theme_menu.add_command(label="Dark", command=lambda: apply_theme("Dark"))  # Dark theme
theme_menu.add_command(label="Auto", command=lambda: apply_theme("Auto"))  # Automatic theme
view_menu.add_cascade(label="Theme", menu=theme_menu)  # Add theme submenu to View

menu_bar.add_cascade(label="View", menu=view_menu)  # Add View menu to the menu bar

# Attach menu bar to the root window
root.config(menu=menu_bar)

# Apply the default theme at startup
apply_theme("Light")

# Keyboard shortcuts for common actions
root.bind("<Control-n>", lambda e: new_file())  # Ctrl+N for new file
root.bind("<Control-o>", lambda e: open_file())  # Ctrl+O for open
root.bind("<Control-s>", lambda e: save())  # Ctrl+S for save
root.bind("<Control-w>", lambda e: close_tab())  # Ctrl+W for close tab
root.bind("<Control-f>", lambda e: find_text())  # Ctrl+F for find
root.bind("<Control-h>", lambda e: find_replace())  # Ctrl+H for find & replace
root.bind("<Control-g>", lambda e: goto_line())  # Ctrl+G for go to line
root.bind("<Control-a>", lambda e: select_all())  # Ctrl+A for select all
root.bind("<Control-z>", lambda e: undo())  # Ctrl+Z for undo
root.bind("<Control-y>", lambda e: redo())  # Ctrl+Y for redo
root.bind("<Control-plus>", lambda e: zoom_in())  # Ctrl + to zoom in
root.bind("<Control-minus>", lambda e: zoom_out())  # Ctrl - to zoom out
root.bind("<Control-0>", lambda e: reset_zoom())  # Ctrl+0 to reset zoom

# Create initial tab to start with
create_new_tab()

# Start the main event loop of the application
root.mainloop()