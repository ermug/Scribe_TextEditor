# Roadmap
# Multi-Tab support
# Change app icon

# Import tkinter and submodules for GUI elements and dialogs
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import platform
import os

# Create the main application window
root = tk.Tk()  # Initialize the main window using tkinter
root.title("Scribe")  # Set the title of the window to 'Scribe'
root.geometry("800x600")  # Set the default size of the window

# Set default font size
font_size = 12  # Starting font size for the text widget

# Store the path to the currently open file
current_file_path = None  # Keep track of which file is currently open (None by default)

# Track current theme
current_theme = "Light"  # Default theme is Light

# Create a frame to hold the line numbers and text widget
text_frame = tk.Frame(root)  # Frame to group line numbers and text box
text_frame.pack(fill="both", expand=True)  # Fill window and expand with resizing

# Line number sidebar
line_numbers = tk.Text(text_frame, width=4, padx=4, takefocus=0, border=0,
                       background="#eeeeee", state="disabled", wrap="none")  # Line numbers pane, disabled for editing
line_numbers.pack(side="left", fill="y")  # Attach to the left, fill vertically

# Scrollbar for the text widget
scrollbar = tk.Scrollbar(text_frame)  # Vertical scrollbar widget
scrollbar.pack(side="right", fill="y")  # Attach to the right, fill vertically

# Create a resizable text box where the user can type text
text = tk.Text(text_frame, wrap=tk.WORD, undo=True, yscrollcommand=scrollbar.set,
               font=("Courier New", font_size))  # Add word-wrapped Text widget with undo enabled and custom font size
text.pack(fill="both", expand=True)  # Fill entire frame with expanding

scrollbar.config(command=text.yview)  # Connect scrollbar to text widget scrolling


# Synchronize scrolling between text widget and line numbers
def sync_scroll(*args):
    """Synchronize scrolling between the main text widget and line numbers"""
    line_numbers.yview_moveto(args[0])
    scrollbar.set(*args)


text.config(yscrollcommand=sync_scroll)


# Update line numbers in the sidebar
def update_line_numbers(event=None):
    if not show_line_numbers.get():  # Only update if line numbers are enabled
        return
    line_numbers.config(state="normal")  # Enable editing to update line numbers
    line_numbers.delete("1.0", "end")  # Clear current line numbers
    line_count = int(text.index('end-1c').split('.')[0])  # Get number of lines in text widget
    line_content = "\n".join(str(i) for i in range(1, line_count + 1))  # Prepare line numbers string
    line_numbers.insert("1.0", line_content)  # Insert line numbers
    line_numbers.config(state="disabled")  # Disable editing again


# Bind line number updates to relevant events
text.bind("<KeyRelease>", update_line_numbers)  # Update line numbers when keys released
text.bind("<MouseWheel>", update_line_numbers)  # Update line numbers on scroll wheel (Windows)
text.bind("<Button-4>", update_line_numbers)  # Linux scroll up
text.bind("<Button-5>", update_line_numbers)  # Linux scroll down
text.bind("<Button-1>", update_line_numbers)  # Update on mouse click


# Function to save the content to the currently open file
def save():
    global current_file_path  # Access the global variable to modify it
    if current_file_path:  # If a file is already open
        try:
            content = text.get("1.0", "end-1c")  # Get all text from the text widget
            with open(current_file_path, "w", encoding="utf-8") as file:  # Open the file in write mode
                file.write(content)  # Write the current text to the file
            messagebox.showinfo("Save", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
    else:
        saveas()  # If no file open, prompt the user to "Save As"


# Function to save the content as a new file
def saveas():
    global current_file_path  # Access the global variable to modify it
    file_path = filedialog.asksaveasfilename(  # Prompt the user to choose a save location
        defaultextension=".txt",  # Default file extension is .txt
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]  # Allow .txt and all file types
    )
    if file_path:  # If user didn't cancel the dialog
        try:
            current_file_path = file_path  # Store the selected path
            content = text.get("1.0", "end-1c")  # Get current text content
            with open(file_path, "w", encoding="utf-8") as file:  # Open file for writing
                file.write(content)  # Write text to file
            root.title(f"Scribe - {os.path.basename(file_path)}")  # Update window title to show file name
            messagebox.showinfo("Save As", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")


# Function to open a file and load its contents
def open_file():
    global current_file_path  # Access the global variable to modify it
    file_path = filedialog.askopenfilename(  # Prompt user to choose a file to open
        filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
    )
    if file_path:  # If user selected a file
        try:
            with open(file_path, "r", encoding="utf-8") as file:  # Open the file in read mode
                content = file.read()  # Read the file content
                text.delete("1.0", tk.END)  # Clear the current text widget
                text.insert("1.0", content)  # Insert the loaded content into the widget (fixed: was tk.END)
            current_file_path = file_path  # Save current file path
            root.title(f"Scribe - {os.path.basename(file_path)}")  # Update the window title
            update_line_numbers()  # Update line numbers after loading file
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")


# Function to undo the last change
def undo():
    try:
        text.event_generate("<<Undo>>")  # Trigger the built-in undo event
    except tk.TclError:
        pass  # Nothing to undo


# Function to redo the last undone change
def redo():
    try:
        text.event_generate("<<Redo>>")  # Trigger the built-in redo event
    except tk.TclError:
        pass  # Nothing to redo


# Function to cut selected text
def cut():
    try:
        text.event_generate("<<Cut>>")  # Trigger the built-in cut event
    except tk.TclError:
        pass  # Nothing selected


# Function to copy selected text
def copy():
    try:
        text.event_generate("<<Copy>>")  # Trigger the built-in copy event
    except tk.TclError:
        pass  # Nothing selected


# Function to paste text from clipboard
def paste():
    try:
        text.event_generate("<<Paste>>")  # Trigger the built-in paste event
        update_line_numbers()  # Update line numbers after paste
    except tk.TclError:
        pass  # Nothing to paste


# Function to select all text in the text box
def select_all():
    text.tag_add(tk.SEL, "1.0", tk.END)  # Select text from start to end
    text.mark_set(tk.INSERT, "1.0")  # Set cursor at start
    text.see(tk.INSERT)  # Ensure selected area is visible


# Function to find and replace text in the document
def find_replace():
    find_text = simpledialog.askstring("Find", "Text to find:")  # Ask user what to find
    if find_text is None or find_text == "":
        return  # Cancel if input is empty
    replace_text = simpledialog.askstring("Replace", "Replace with:")  # Ask what to replace with
    if replace_text is None:
        return  # Cancel if input is empty

    content = text.get("1.0", "end-1c")  # Get full text content (fixed: was tk.END)
    if find_text in content:
        new_content = content.replace(find_text, replace_text)  # Replace all occurrences
        text.delete("1.0", tk.END)  # Clear old text
        text.insert("1.0", new_content)  # Insert updated text
        update_line_numbers()  # Update line numbers
        count = content.count(find_text)
        messagebox.showinfo("Find & Replace", f"Replaced {count} occurrence(s) of '{find_text}'.")
    else:
        messagebox.showinfo("Find & Replace", f"Text '{find_text}' not found.")


# Function to jump to a specific line number
def goto_line():
    line = simpledialog.askinteger("Go To Line", "Enter line number:")  # Ask for line number
    if line and line > 0:  # If a valid positive number is entered
        try:
            index = f"{line}.0"  # Format it as a text index
            text.mark_set(tk.INSERT, index)  # Move cursor to that line
            text.see(index)  # Scroll to show that line
        except tk.TclError:
            messagebox.showerror("Error", f"Line {line} does not exist.")


# Function to find and highlight text in the document
def find_text():
    # Ask the user for the text they want to search for
    query = simpledialog.askstring("Find", "Enter text to find:")
    if not query:
        return  # Exit if user cancels or provides no input

    text.tag_remove("highlight", "1.0", tk.END)  # Clear previous highlights

    # Start from the top and search forward
    start_pos = "1.0"
    count = 0
    while True:
        start_pos = text.search(query, start_pos, stopindex=tk.END, nocase=True)
        if not start_pos:
            break  # No more matches
        end_pos = f"{start_pos}+{len(query)}c"  # Calculate the end position of the match
        text.tag_add("highlight", start_pos, end_pos)  # Highlight the matched text
        start_pos = end_pos  # Move past the last match
        count += 1

    # Define highlight appearance (yellow background)
    text.tag_config("highlight", background="yellow", foreground="black")

    # Show message with count
    if count == 0:
        messagebox.showinfo("Find", "No matches found.")
    else:
        messagebox.showinfo("Find", f"Found {count} match(es).")


# --- View Features ---

# Boolean variable to track if line numbers are shown
show_line_numbers = tk.BooleanVar(value=True)  # Default is to show line numbers


# Toggle line numbers visibility
def toggle_line_numbers():
    if show_line_numbers.get():
        line_numbers.pack(side="left", fill="y")  # Show line numbers
        update_line_numbers()  # Update line numbers display
    else:
        line_numbers.pack_forget()  # Hide line numbers


# Increase font size for zoom in
def zoom_in():
    global font_size
    if font_size < 72:  # Maximum font size limit
        font_size += 1  # Increase font size
        text.config(font=("Courier New", font_size))  # Apply new font size
        line_numbers.config(font=("Courier New", font_size))  # Update line numbers font too
        update_line_numbers()  # Update line numbers


# Decrease font size for zoom out
def zoom_out():
    global font_size
    if font_size > 6:  # Minimum font size limit
        font_size -= 1  # Decrease font size
        text.config(font=("Courier New", font_size))  # Apply new font size
        line_numbers.config(font=("Courier New", font_size))  # Update line numbers font too
        update_line_numbers()  # Update line numbers


# Apply light, dark or automatic theme
def apply_theme(theme):
    global current_theme
    current_theme = theme

    # Automatic: detect system preference (basic implementation)
    if theme == "Auto":
        if platform.system() == "Darwin":  # macOS
            # Simple heuristic - could be improved with actual system detection
            theme = "Dark"
        else:
            theme = "Light"  # Default light theme for others

    if theme == "Dark":
        root.config(bg="#2d2d2d")  # Set root background
        text_frame.config(bg="#2d2d2d")  # Set frame background
        text.config(bg="#1e1e1e", fg="#dcdcdc", insertbackground="white")  # Dark background and light text
        line_numbers.config(bg="#2d2d2d", fg="#aaa")  # Dark line number background
    else:
        root.config(bg="SystemButtonFace")  # Default system background
        text_frame.config(bg="SystemButtonFace")  # Default frame background
        text.config(bg="white", fg="black", insertbackground="black")  # Light theme colors
        line_numbers.config(bg="#eeeeee", fg="black")  # Light line number background


# --- Menu Bar Setup ---

menu_bar = tk.Menu(root)  # Create the menu bar

# Create the "File" drop-down menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # Create a submenu under File
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")  # Add accelerator
file_menu.add_command(label="Save", command=save, accelerator="Ctrl+S")  # Add accelerator
file_menu.add_command(label="Save As...", command=saveas)  # Add 'Save As' option
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
#view_menu.add_checkbutton(label="Show Line Numbers", variable=show_line_numbers,
#                          command=toggle_line_numbers)  # Toggle line numbers
#view_menu.add_separator()
view_menu.add_command(label="Zoom In", command=zoom_in, accelerator="Ctrl++")  # Zoom in option
view_menu.add_command(label="Zoom Out", command=zoom_out, accelerator="Ctrl+-")  # Zoom out option

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
root.bind("<Control-o>", lambda e: open_file())  # Ctrl+O for open
root.bind("<Control-s>", lambda e: save())  # Ctrl+S for save
root.bind("<Control-f>", lambda e: find_text())  # Ctrl+F for find
root.bind("<Control-h>", lambda e: find_replace())  # Ctrl+H for find & replace
root.bind("<Control-g>", lambda e: goto_line())  # Ctrl+G for go to line
root.bind("<Control-a>", lambda e: select_all())  # Ctrl+A for select all
root.bind("<Control-z>", lambda e: undo())  # Ctrl+Z for undo
root.bind("<Control-y>", lambda e: redo())  # Ctrl+Y for redo
root.bind("<Control-plus>", lambda e: zoom_in())  # Ctrl + to zoom in
root.bind("<Control-minus>", lambda e: zoom_out())  # Ctrl - to zoom out

# Initialize line numbers display
update_line_numbers()

# Start the main event loop of the application
root.mainloop()