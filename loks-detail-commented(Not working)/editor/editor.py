# Import necessary modules from the tkinter library
from tkinter import filedialog, messagebox
import tkinter as tk
import tkinter.ttk as ttk
import os
import platform
import subprocess
import math
import json

# Check the operating system to determine the control key (Ctrl or Command)
if platform.system() == "Darwin":
    ctrl_key = "Command"
else:
    ctrl_key = "Control"

# The imported modules:
# - filedialog: Provides dialogs for file selection.
# - messagebox: Provides dialogs for displaying messages.
# - tkinter: The main Tkinter module.
# - ttk: Tkinter themed widgets, which are enhanced versions of the standard Tkinter widgets.
# - os: Provides a way of interacting with the operating system, like working with file paths.
# - platform: Allows retrieving information about the platform (operating system).
# - subprocess: Allows spawning new processes and interacting with them.
# - math: Provides mathematical functions.
# - json: Provides functions for working with JSON data.

# Define a class with an __init__ method that initializes the class instance.
class PreferencesScreen:
    def __init__(self, p) -> None:
        # Create a Toplevel widget (a new window) for preferences.
        self.wnd = tk.Toplevel()

        # Set the title of the preferences window.
        self.wnd.title("Preferences")

        # Set a default font for the entire window.
        self.wnd.option_add("*Font", "18")

        # Set a minimum size for the preferences window.
        self.wnd.minsize(300, 200)

        # Configure a default style for ttk widgets.
        self._defStyle = ttk.Style()
        self._defStyle.configure("editor.TButton", font=("Courier", 11))

        # Initialize variables for font, theme, PyOption textbox, and Apply Changes button.
        self._fontVar = None
        self._themeVar = None
        self._pyOptionTextbox = None
        self._applyButton = ttk.Button(self.wnd, text="Apply Changes", style="editor.TButton")

        # Create an empty dictionary to store theme-related information.
        self._themeDict = dict()

        # Store the preferences parameter passed to the constructor.
        self._preferences = p


    # Method to display the preferences window and start the Tkinter main loop.
    def showWindow(self) -> None:
        # Create and set up the UI for the preferences window.
        self._makeUI()

        # Start the Tkinter main loop to display the preferences window.
        self.wnd.mainloop()


    # Method to configure the command for the Apply Changes button.
    def getSettingsCommand(self, editor) -> None:
        # Configure the command for the Apply Changes button to call the editor's applySettings method
        # with the specified settings obtained from the UI elements.

        # The lambda function captures the current state of the UI elements when the command is created.
        self._applyButton.config(command=lambda: editor.applySettings(
            {
                "fontSize": int(self._fontVar.get()),              # Get and convert font size to an integer.
                "theme": self._themeDict[self._themeVar.get()],   # Get the selected theme from the theme dictionary.
                "pyinterp": self._pyOptionTextbox.get()            # Get the value from the PyOption textbox.
            }
        ))


    # Method to create and configure a frame for selecting the font size.
    def _makeFontFrame(self) -> None:
        # Create a new frame within the preferences window for font-related options.
        fontFrame = tk.Frame(self.wnd)

        # Define a list of font size options.
        fontOptions = ["12", "14", "16", "18", "20", "24"]

        # Create a StringVar to store the selected font size.
        self._fontVar = tk.StringVar(self.wnd)
        # Set the initial value of the StringVar to the font size from preferences.
        self._fontVar.set(str(self._preferences["fontSize"]))

        # Create a label to display "Font Size" within the font frame.
        fontLabel = tk.Label(fontFrame, text="Font Size: ")

        # Create an OptionMenu (dropdown menu) to select the font size.
        fontMenu = ttk.OptionMenu(fontFrame, self._fontVar, str(self._preferences["fontSize"]), *fontOptions)

        # Pack the label and OptionMenu widgets within the font frame.
        fontLabel.pack(side="left")
        fontMenu.pack(side="right")

        # Pack the font frame within the preferences window with specified padding.
        fontFrame.pack(padx=30, pady=20)
# Method to create and configure a frame for selecting a theme.
    def _makeThemeFrame(self) -> None:
        # Create a new frame within the preferences window for theme-related options.
        themeFrame = tk.Frame(self.wnd)

        # Initialize an empty list to store theme options.
        themeOptions = []

        # Get the list of theme files from the 'editor/theme' directory.
        files = tuple(os.walk(f"{os.getcwd().replace(os.sep, '/')}/editor/theme"))[0][-1]

        # Iterate through each theme file and extract its name.
        for i in files:
            # Open each theme file to read its content.
            f = open(f"{os.getcwd().replace(os.sep, '/')}/editor/theme/{i}")
            # Extract the 'name' field from the JSON content and append it to the themeOptions list.
            name = json.loads(f.read())["name"]
            themeOptions.append(name)
            # Store the mapping of theme name to file name in the theme dictionary.
            self._themeDict[name] = i
            # Close the file.
            f.close()

        # Create a StringVar to store the selected theme.
        self._themeVar = tk.StringVar(self.wnd)
        # Set the initial value of the StringVar to the theme from preferences.
        self._themeVar.set(str(self._preferences["theme"]))

        # Open the theme file corresponding to the selected theme and extract its name.
        f = open(f'{os.getcwd().replace(os.sep, "/")}/editor/theme/{self._preferences["theme"]}')
        # Create a label with text "Theme:" to display above the theme selection dropdown.
        themeLabel = tk.Label(themeFrame, text="Theme: ")
        # Create an OptionMenu (dropdown menu) to select the theme.
        themeMenu = ttk.OptionMenu(themeFrame, self._themeVar, json.loads(f.read())["name"], *themeOptions)
        # Close the file.
        f.close()

        # Pack the label and OptionMenu widgets within the theme frame.
        themeLabel.pack(side="left")
        themeMenu.pack(side="right")

        # Pack the theme frame within the preferences window with specified padding.
        themeFrame.pack(padx=50, pady=20)

    # Method to create and configure a frame for specifying the Python interpreter option.
    def _makePyInterpreterOptionFrame(self) -> None:
        # Create a new frame within the preferences window for Python interpreter-related options.
        pyOptionFrame = tk.Frame(self.wnd)
        
        # Create a label with text "Python interpreter:" to display above the Python interpreter option textbox.
        pyOptionLabel = tk.Label(pyOptionFrame, text="Python interpreter: ")

        # Create an entry widget for entering the Python interpreter option.
        self._pyOptionTextbox = tk.Entry(pyOptionFrame)
        # Clear the current content of the entry widget.
        self._pyOptionTextbox.delete(0, tk.END)
        # Insert the Python interpreter option from preferences into the entry widget.
        self._pyOptionTextbox.insert(0, self._preferences["pyinterp"])

        # Pack the label and entry widgets within the Python interpreter option frame.
        pyOptionLabel.pack()
        self._pyOptionTextbox.pack(ipady=5, ipadx=5)
        pyOptionFrame.pack(pady=20)


    # Method to create and configure the entire UI for the preferences window.
    def _makeUI(self) -> None:
        # Call the methods to create frames for font, theme, and Python interpreter options.
        self._makeFontFrame()
        self._makeThemeFrame()
        self._makePyInterpreterOptionFrame()
        
        # Pack the Apply Changes button with specified internal and external padding.
        self._applyButton.pack(ipady=5, ipadx=5, pady=20)


    # Method to set up a function to handle the closing of the preferences window.
    def handleCloseFunction(self, f) -> None:
        # Set up a function to be called when the preferences window is closed.
        self.wnd.protocol("WM_DELETE_WINDOW", lambda: f(self.wnd))

# Class representing a simple text editor.
class Editor:
    def __init__(self) -> None:
        # Initialize the main Tkinter window.
        self._rootWnd = tk.Tk()
        # Set the title of the editor window.
        self._rootWnd.title("untitled")
        # Set the current open file to "untitled".
        self._curOpenFile = "untitled"
        # Flag to track whether the current file is saved.
        self._curFileIsSaved = False

        # Default preferences for the editor.
        self._preferences = {
            "fontSize": 16,
            "pyinterp": "python",
            "theme": "defaultDark.json"
        }
        # Load preferences from storage.
        self._loadPreferences()
        # Flag to track whether the preferences window is open.
        self._prefWindowIsOpen = False

        # Default dark theme for the editor.
        self._theme = {
            "name": "default dark",
            "background": "#030d22",
            "foreground": "#ffffff",
            "selectBackground": "#35008b",
            "inactiveselectbackground": "#310072",
            "cursorColor": "#ee0077",
            "keywords": "#ff2cf1",
            "functionName": "#ffd400",
            "strings": "#0ef3ff",
            "comments": "#0098df"
        }
        # Load the theme settings.
        self._loadTheme()

        # Create a menu bar for the editor.
        self._menuBar = tk.Menu(self._rootWnd)

        # Create a Text widget for the editor area.
        self._textArea = tk.Text(
            self._rootWnd,
            borderwidth=0,
            insertbackground=self._theme["cursorColor"],
            bg=self._theme["background"],
            fg=self._theme["foreground"],
            font=("Consolas", self._preferences["fontSize"]),
            selectbackground=self._theme["selectBackground"],
            inactiveselectbackground=self._theme["inactiveselectbackground"]
        )

        # Bind event handlers for specific key combinations.
        self._textArea.bind("<KeyRelease>", self._handleKeyRelease)
        self._textArea.bind(f"<{ctrl_key}-Key-s>", self._saveFile)
        self._textArea.bind(f"<{ctrl_key}-Key-o>", self._openFile)
        self._textArea.bind("<Tab>", self._tab)
        self._textArea.bind("<Shift-Tab>", self._shiftTab)

        # Define a set of tokens for syntax highlighting.
        self._colorTokens = {
            "fun", "if", "else", "elsif", "for", "while",
            "return",  "var", "true", "false", "continue", "break",
            "=",  "==", ">", ">=", "<", "<=", "!", "!=", "+", "-", "*", "/"
        }

# Method to handle the Tab key press event.
    def _tab(self, e) -> str:
        try:
            # Get the start index of the selected text.
            start = self._textArea.index(tk.SEL_FIRST)
            start = f"{start[:start.index('.')]}.0"

            # Get the end index of the selected text.
            end = self._textArea.index(tk.SEL_LAST)
            end = f"{end[:end.index('.')]}.250"

            # Extract the selected text and split it into lines.
            selected = self._textArea.get(start, end)
            selected = selected.split('\n')
        except:
            # Handle the case when there is no selected text.
            selected = None

        if selected:        
            # Indent each line of the selected text by adding spaces.
            for k, line in enumerate(selected):
                i = 0
                while i <= len(line):
                    if i >= 4:
                        break
                    selected[k] = ' ' + selected[k]
                    i += 1
                
            # Combine the modified lines back into a single string.
            output = ''
            for line in selected:
                output += line + '\n'

            # Delete the original selected text and insert the modified text.
            self._textArea.delete(start, end)
            self._textArea.insert(start, output)
            # Set the cursor position to the start of the modified text.
            self._textArea.mark_set(tk.INSERT, start)
            # Add the "sel" tag to the modified text to indicate selection.
            self._textArea.tag_add("sel", start, end)
        else:
            # If no text is selected, insert four spaces at the cursor position.
            self._textArea.insert(tk.INSERT, " "*4)

        # Return "break" to prevent default behavior of the Tab key.
        return "break"

    # Method to handle the Shift-Tab key press event.
    def _shiftTab(self, e) -> str:
        try:
            # Get the start index of the selected text.
            start = self._textArea.index(tk.SEL_FIRST)
            start = f"{start[:start.index('.')]}.0"

            # Get the end index of the selected text.
            end = self._textArea.index(tk.SEL_LAST)
            end = f"{end[:end.index('.')]}.250"

            # Extract the selected text and split it into lines.
            selected = self._textArea.get(start, end)
            selected = selected.split('\n')
        except:
            # Handle the case when there is no selected text.
            selected = None

        if selected:
            # Remove four leading spaces from each line of the selected text.
            for k, line in enumerate(selected):
                i = 0
                while i <= len(line):
                    if i >= 4:
                        break
                    # Check if the line starts with a space, and remove it.
                    if len(selected[k]) > 0 and selected[k][0] == ' ':
                        selected[k] = selected[k][1:]
                    i += 1
                
            # Combine the modified lines back into a single string.
            output = ''
            for line in selected:
                output += line + '\n'

            # Delete the original selected text and insert the modified text.
            self._textArea.delete(start, end)
            self._textArea.insert(start, output)
            # Set the cursor position to the start of the modified text.
            self._textArea.mark_set(tk.INSERT, start)
            # Add the "sel" tag to the modified text to indicate selection.
            self._textArea.tag_add("sel", start, end)
        else:
            # If no text is selected, determine the range to delete (four characters before the cursor position).
            end = self._textArea.index(tk.INSERT)
            start = f"{end[:end.index('.')]}.{int(end[end.index('.')+1:])-4}"
            # Delete the determined range.
            self._textArea.delete(start, end)

        # Return "break" to prevent default behavior of the Shift-Tab key.
        return "break"

    # Method to display the main window of the text editor.
    def showWindow(self) -> None:
        # Call the method to create the user interface.
        self._makeUI()
        # Start the main event loop to display the window.
        self._rootWnd.mainloop()

    # Method to create the user interface components.
    def _makeUI(self) -> None:
        # Call methods to create the menu and text area.
        self._makeMenu()
        self._makeTextArea()

    # Method to create the menu bar and menu items.
    def _makeMenu(self) -> None:
        # Create a "File" menu with commands for file-related actions.
        fileMenu = tk.Menu(self._menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=self._openFile)
        fileMenu.add_command(label="Save", command=self._saveFile)
        fileMenu.add_command(label="Save As", command=self._saveAsFile)
        
        # Add the "File" menu to the menu bar.
        self._menuBar.add_cascade(label="File", menu=fileMenu)

        # Create a "Run" menu with commands for program execution.
        runMenu = tk.Menu(self._menuBar, tearoff=0)
        runMenu.add_command(label="Run", command=self._runProgram)
        runMenu.add_command(label="Run (debug)", command=self._runDebug)
        runMenu.add_command(label="Visualize AST", command=self._visualize)

        # Add the "Run" menu to the menu bar.
        self._menuBar.add_cascade(label="Run", menu=runMenu)

        # Create an "Options" menu with commands for preferences.
        settingsMenu = tk.Menu(self._menuBar, tearoff=0)
        settingsMenu.add_command(label="Preferences", command=self._showPreferences)

        # Add the "Options" menu to the menu bar.
        self._menuBar.add_cascade(label="Options", menu=settingsMenu)

        # Set the menu bar for the main window.
        self._rootWnd.config(menu=self._menuBar)

    # Method to configure and display the text area in the main window.
    def _makeTextArea(self) -> None:
        # Pack the text area widget to fill the available space in the main window.
        self._textArea.pack(expand=True, fill=tk.BOTH)

    # Method to handle the closing of the preferences window.
    def _prefWindowIsClosed(self, w) -> None:
        # Destroy the preferences window and update the flag.
        w.destroy()
        self._prefWindowIsOpen = False

    # Method to show the preferences window.
    def _showPreferences(self) -> None:
        # Check if the preferences window is not already open.
        if not self._prefWindowIsOpen:
            # Set the flag to indicate that the preferences window is open.
            self._prefWindowIsOpen = True
            # Load preferences and create a PreferencesScreen instance.
            self._loadPreferences()
            p = PreferencesScreen(self._preferences)
            
            # Configure the preferences screen with commands and handlers.
            p.getSettingsCommand(self)
            p.handleCloseFunction(self._prefWindowIsClosed)
            # Show the preferences window.
            p.showWindow()
    # Method to save preferences to a JSON file.
    def _savePreferences(self, s) -> None:
        # Update the editor's preferences with the provided settings.
        self._preferences = s

        # Check if the "data" directory exists in the editor directory.
        if "data" not in list(os.walk(f"{os.getcwd().replace(os.sep, '/')}/editor"))[0][1]:
            # If not, create the "data" directory.
            os.mkdir(f"{os.getcwd().replace(os.sep, '/')}/editor/data")

        # Write the preferences to a JSON file.
        with open(f"{os.getcwd().replace(os.sep, '/')}/editor/data/preferences.json", "w+") as f:
            # Convert the preferences dictionary to a formatted JSON string and write it to the file.
            f.write(json.dumps(
                s,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
        ))

    # Method to load preferences from a JSON file.
    def _loadPreferences(self) -> None:
        # Check if the "data" directory exists in the editor directory.
        if "data" not in list(os.walk(f"{os.getcwd().replace(os.sep, '/')}/editor"))[0][1]:
            # If not, create the "data" directory.
            os.mkdir(f"{os.getcwd().replace(os.sep, '/')}/editor/data")
        
        try:
            # Try to open and read the preferences from the existing JSON file.
            with open(f"{os.getcwd().replace(os.sep, '/')}/editor/data/preferences.json") as f:
                # Load the preferences from the file into the editor's preferences.
                self._preferences = json.loads(f.read())
        except FileNotFoundError:
            # If the file is not found, create a new file with default preferences.
            with open(f"{os.getcwd().replace(os.sep, '/')}/editor/data/preferences.json", "w+") as f:
                # Write default preferences to the new file.
                f.write(json.dumps(
                    self._preferences,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                ))

    # Method to load the editor theme from a JSON file.
    def _loadTheme(self) -> None:
        # Check if the "theme" directory exists in the editor directory.
        if "theme" not in list(os.walk(f"{os.getcwd().replace(os.sep, '/')}/editor"))[0][1]:
            # If not, create the "theme" directory.
            os.mkdir(f"{os.getcwd().replace(os.sep, '/')}/editor/theme")

        # Construct the path to the JSON file for the selected theme.
        path: str = f'{os.getcwd().replace(os.sep, "/")}/editor/theme/{self._preferences["theme"]}'
        
        # Open and read the selected theme from the JSON file.
        with open(path) as f:
            # Load the theme from the file into the editor's theme settings.
            self._theme = json.loads(f.read())

    # Method to apply a theme to the text area.
    def _applyTheme(self, theme) -> None:
        # Configure the text area with the colors from the provided theme.
        self._textArea.config(
            insertbackground=theme["cursorColor"],
            bg=theme["background"],
            fg=theme["foreground"],
            selectbackground=theme["selectBackground"],
            inactiveselectbackground=theme["inactiveselectbackground"]
        )
        
        # Call the _highlight method to update syntax highlighting based on the new theme.
        self._highlight()


    # Method to apply settings to the editor.
    def applySettings(self, s) -> None:
        # Save the provided settings to preferences.
        self._savePreferences(s)
        
        # Configure the font of the text area based on the new font size.
        self._textArea.config(font=("Consolas", s["fontSize"]))

        # Load the current theme and apply it to the text area.
        self._loadTheme()
        self._applyTheme(self._theme)

    # Method to handle key release events in the text area.
    def _handleKeyRelease(self, e) -> None:
        # Perform auto-complete and format operations based on the key release event.
        self._autoCompleteAndFormat(e)
        
        # Change the title of the editor window when the content is modified.
        self._changeTitleOnSave()
        
        # Highlight the syntax in the text area.
        self._highlight()

    # Method to perform auto-complete and format code operations.
    def _autoCompleteAndFormat(self, e) -> None:
        # Call the _autoComplete and _autoformat methods.
        self._autoComplete(e)
        self._autoformat(e)

    # Method to perform auto-complete operations. 
    def _autoComplete(self, e) -> None:
        # Check if the pressed key is one of the characters triggering auto-complete.
        if e.char in ['(', '{', '[', "'", '"']:
            # Get the current cursor position.
            p = self._textArea.index(tk.INSERT)

            # Insert the corresponding closing character after the pressed key.
            if e.char == '(':
                self._textArea.insert(tk.INSERT, ')')
            elif e.char == '{':
                self._textArea.insert(tk.INSERT, '}')
            elif e.char == '[':
                self._textArea.insert(tk.INSERT, ']')
            elif e.char == '"':
                self._textArea.insert(tk.INSERT, '"')
            elif e.char == "'":
                self._textArea.insert(tk.INSERT, "'")

            # Set the cursor position back to the original position.
            self._textArea.mark_set(tk.INSERT, p)

    # Method to automatically format code based on specific key events.
    def _autoformat(self, e) -> None:
        # Check if the pressed key is the Enter key ('\r').
        if e.char == '\r':
            # Get the current cursor position.
            cur = self._textArea.index(tk.INSERT)
            # Extract the line number from the cursor position.
            line = math.floor(float(cur))

            # Get the full text content of the text area and split it into lines.
            fulltxt = self._textArea.get("1.0", tk.END).split('\n')

            # Remove trailing empty lines.
            while fulltxt[-1] == '':
                fulltxt.pop()
                if len(fulltxt) == 0:
                    return

            # Count leading spaces of the line above the current cursor position.
            spaceCount = 0
            if not (line-2) >= len(fulltxt):
                for c in fulltxt[line-2]:
                    if c == ' ':
                        spaceCount += 1
                    else:
                        break
                
            # Insert the same number of leading spaces on the new line.
            for _ in range(spaceCount):
                self._textArea.insert(tk.INSERT, ' ')
                
            # If the line above the cursor ends with '{', auto-indent and close the block.
            if (line-2) >= len(fulltxt):
                return
            try:
                if fulltxt[line-2][-1] == '{':
                    # Delete the current line.
                    cur = self._textArea.index(tk.INSERT)
                    line = int(float(cur))
                    char = int(cur[cur.index('.')+1:])
                    self._textArea.delete(f"{line}.{char}")
                    cur = self._textArea.index(tk.INSERT)
                    
                    # Prepare the string to insert for indentation and closing the block.
                    insertStr = ""
                    for _ in range(spaceCount):
                        insertStr += ' '
                    insertStr += "    \n"
                    
                    for _ in range(spaceCount):
                        insertStr += ' '
                    insertStr += '}'

                    # Insert the formatted string at the cursor position.
                    self._textArea.insert(cur, insertStr)

                    # Move the cursor to the indented position after the inserted block.
                    line = int(float(cur))
                    char = int(cur[cur.index('.')+1:])
                    self._textArea.mark_set(tk.INSERT, f"{line}.{char+4}")
            except:
                # Handle exceptions (e.g., if the line above is too short).
                pass


    # Method to change the title of the editor window based on the save state.
    def _changeTitleOnSave(self) -> None:
        # Change title and set state if the file is not saved.
        if not self._curFileIsSaved:
            # Append '*' to the title to indicate unsaved changes.
            self._rootWnd.title(self._curOpenFile + '*')

        # Check if the file is saved.
        if self._curFileIsSaved:
            # Open the current file in read mode.
            f = open(self._curOpenFile)
            # Read the content of the file.
            s = f.read()
            # Close the file.
            f.close()

            # Get the current content of the text area.
            text = self._textArea.get("1.0", tk.END)

            # Compare the content of the file and the text area.
            if s != text:
                # If they are different, set the file state to unsaved.
                self._curFileIsSaved = False

    # Method to perform syntax highlighting.
    def _highlight(self) -> None:
        # Call various methods to highlight different elements of the code.
        self._highlightTokens()
        self._highlightStrings()
        self._highlightFuncName()
        self._highlightComments()

    # Method to highlight language keywords.
    def _highlightTokens(self) -> None:
        # Iterate through each language keyword.
        for i in self._colorTokens:
            try:
                # Find the position of the keyword in the text area.
                pos = self._textArea.search(i, "1.0", stopindex="end")
                line = int(float(pos))
                char = int(pos[pos.index('.')+1:])
                
                # Configure the tag for the keyword with the corresponding color.
                self._textArea.tag_configure(i, foreground=self._theme["keywords"])

                # Define the end position of the keyword.
                end = f"{line}.{char+len(i)}"

                # Apply the tag to all occurrences of the keyword in the text area.
                while pos:
                    self._textArea.tag_add(i, pos, end)
                    pos = self._textArea.search(i, end, stopindex="end")
                    line = int(float(pos))
                    char = int(pos[pos.index('.')+1:])
                    end = f"{line}.{char+len(i)}"

            except:
                pass


    # Method to highlight strings in the code.
    def _highlightStrings(self) -> None:
        # Try to highlight strings using a regular expression.
        try:
            # Create an IntVar to store the count of characters in the matched string.
            cVar = tk.IntVar()

            # Find the position of a double-quoted string using a regular expression.
            pos = self._textArea.search(r'".*\s*"', "1.0", stopindex="end", count=cVar, regexp=True)
            line = int(float(pos))
            char = int(pos[pos.index('.')+1:])

            # Configure the tag for strings with the corresponding color.
            self._textArea.tag_configure("str", foreground=self._theme["strings"])

            # Define the end position of the matched string.
            end = f"{line}.{char+cVar.get()}"

            # Apply the tag to all occurrences of the matched string in the text area.
            while pos:
                self._textArea.tag_add("str", pos, end)
                pos = self._textArea.search(r'".*\s*"', end, stopindex="end")
                line = int(float(pos))
                char = int(pos[pos.index('.')+1:])
                end = f"{line}.{char+cVar.get()}"
        except:
            # Handle exceptions (e.g., if there is no valid string pattern).
            pass

    # Method to highlight function names in the code.
    def _highlightFuncName(self) -> None:
        # Try to highlight function names using a regular expression.
        try:
            # Create an IntVar to store the count of characters in the matched function name.
            cVar = tk.IntVar()

            # Find the position of a word followed by an opening parenthesis (indicating a function name).
            pos = self._textArea.search(r'\w+\s*\(', "1.0", stopindex="end", count=cVar, regexp=True)
            line = int(float(pos))
            char = int(pos[pos.index('.')+1:])

            # Configure the tag for function names with the corresponding color.
            self._textArea.tag_configure("fnname", foreground=self._theme["functionName"])

            # Define the end position of the matched function name.
            end = f"{line}.{char+cVar.get()-1}"

            # Apply the tag to all occurrences of the matched function name in the text area.
            while pos:
                # Check if the matched function name is not in the list of language keywords.
                if self._textArea.get(pos, end) not in self._colorTokens:
                    # Add the tag only if the function name is not a language keyword.
                    self._textArea.tag_add("fnname", pos, end)
                
                # Find the next occurrence of a word followed by an opening parenthesis.
                pos = self._textArea.search(r'\w+\s*\(', end, stopindex="end", count=cVar, regexp=True)
                line = int(float(pos))
                char = int(pos[pos.index('.')+1:])
                end = f"{line}.{char+cVar.get()-1}"
        except:
            # Handle exceptions (e.g., if there is no valid function name pattern).
            pass

    # Method to highlight comments in the code.
    def _highlightComments(self) -> None:
        # Call various methods to highlight different types of comments.
        self._highlightSingleLineComments()

        # Multiline comments highlighting is currently not implemented.
        # self._highlightMultiLineComments()

    # Method to highlight single-line comments in the code.
    def _highlightSingleLineComments(self) -> None:
        try:
            # Create an IntVar to store the count of characters in the matched single-line comment.
            cVar = tk.IntVar()

            # Find the position of a single-line comment using a regular expression.
            pos = self._textArea.search(r'\/\/[^\n\r]*', "1.0", stopindex="end", count=cVar, regexp=True)
            line = int(float(pos))
            char = int(pos[pos.index('.')+1:])

            # Configure the tag for single-line comments with the corresponding color.
            self._textArea.tag_configure("scomment", foreground=self._theme["comments"])

            # Define the end position of the matched single-line comment.
            end = f"{line}.{char+cVar.get()}"

            # Apply the tag to all occurrences of the matched single-line comment in the text area.
            while pos:
                self._textArea.tag_add("scomment", pos, end)
                pos = self._textArea.search(r'\/\/[^\n\r]*', end, stopindex="end", count=cVar, regexp=True)
                line = int(float(pos))
                char = int(pos[pos.index('.')+1:])
                end = f"{line}.{char+cVar.get()}"
        except:
            # Handle exceptions (e.g., if there is no valid single-line comment pattern).
            pass

    # Method to highlight multiline comments in the code (not working reliably).
    def _highlightMultiLineComments(self) -> None:
        try:
            # Create an IntVar to store the count of characters in the matched multiline comment.
            cVar = tk.IntVar()

            # Find the position of a multiline comment using a regular expression.
            pos = self._textArea.search(r"\/\*\s*\S*\*\/", "1.0", stopindex="end", count=cVar, regexp=True)
            
            line = int(float(pos))
            char = int(pos[pos.index('.')+1:])

            # Split the text area content into lines, excluding empty lines.
            fulltxt = self._textArea.get("1.0", tk.END).split('\n')
            while fulltxt[-1] == '':
                fulltxt.pop()

            # Configure the tag for multiline comments with the corresponding color.
            self._textArea.tag_configure("mcomment", foreground=self._theme["comments"])
            end = f"{line}.{char+cVar.get()}"
            
            # Handle the case where the multiline comment extends beyond the length of the current line.
            if (char+cVar.get()) > len(fulltxt[line-1]):
                totalLen = 0
                for i in fulltxt[:-1]:
                    totalLen += len(i)
                end = f"{len(fulltxt)}.{(char+cVar.get())-totalLen}"  

            # Apply the tag to all occurrences of the matched multiline comment in the text area.
            while pos:
                self._textArea.tag_add("mcomment", pos, end)

                pos = self._textArea.search(r'\/\*\s*\S*\*\/', end, stopindex="end", count=cVar, regexp=True)
                line = int(float(pos))
                char = int(pos[pos.index('.')+1:])

                # Split the text area content into lines, excluding empty lines.
                fulltxt = self._textArea.get("1.0", tk.END).split('\n')
                while fulltxt[-1] == '':
                    fulltxt.pop()

                end = f"{line}.{char+cVar.get()}"

                # Handle the case where the multiline comment extends beyond the length of the current line.
                if (char+cVar.get()) > len(fulltxt[line-1]):
                    totalLen = 0
                    for i in fulltxt[:-1]:
                        totalLen += len(i)
                    end = f"{len(fulltxt)}.{(char+cVar.get())-totalLen}"

        except:
            # Handle exceptions (e.g., if there is no valid multiline comment pattern).
            pass

    # Method to get the content of a file given its name.
    def _getFileContent(self, name: str) -> str:    
        # Open the file in read mode.
        f = open(name, 'r')
        
        # Read the content of the file.
        s = f.read()
        
        # Close the file.
        f.close()
        
        # Return the content of the file.
        return s        

    # Method to open a file and load its content into the text area.
    def _openFile(self, e=None) -> None:
        # Ask the user to select a file using the file dialog.
        name = tk.filedialog.askopenfilename(
            initialdir=os.getcwd(), 
            title="Select file",
            filetypes=(("Loks files", "*.lks"), ("All files", "*.*"))
        )
        
        # If the user cancels the file selection, return.
        if name == '':
            return

        # Get the content of the selected file.
        s = self._getFileContent(name)
        
        # Delete the current content of the text area.
        self._textArea.delete("1.0", tk.END)
        
        # Insert the content of the file into the text area.
        self._textArea.insert("1.0", s)
        
        # Set the title of the main window to the name of the opened file.
        self._rootWnd.title(name)
        
        # Update the current open file variable.
        self._curOpenFile = name
        
        # Highlight the code in the text area.
        self._highlight()
        
        # Set the flag indicating that the current file is saved.
        self._curFileIsSaved = True

    # Method to save the content of the text area to a new file using the "Save As" dialog.
    def _saveAsFile(self) -> None:
        # Open the "Save As" dialog to get the file to save.
        f = tk.filedialog.asksaveasfile(
            mode='w', 
            title="Select file",
            filetypes=[("Loks File (*.lks)", "*.lks"), ("Text File (*.txt)", "*.txt")],
            defaultextension=("Loks File (*.lks)", "*.lks")
        )

        # If the user cancels the file selection, return.
        if f is None:
            return

        # Get the text content of the text area.
        text = self._textArea.get("1.0", tk.END)

        # Write the text content to the selected file.
        f.write(text)

        # Set the title of the main window to the name of the saved file.
        self._rootWnd.title(f.name)

        # Update the current open file variable.
        self._curOpenFile = f.name

        # Close the file.
        f.close()

        # Set the flag indicating that the current file is saved.
        self._curFileIsSaved = True

    # Method to save the content of the text area to the current file.
    def _saveFile(self, e=None) -> None:
        # If the current open file is untitled, initiate the "Save As" process.
        if self._curOpenFile == "untitled":
            return self._saveAsFile()

        # Open the current file in write mode.
        f = open(self._curOpenFile, 'w')

        # Get the text content of the text area.
        text = self._textArea.get("1.0", tk.END)

        # Write the text content to the current file.
        f.write(text)

        # Set the title of the main window to the name of the saved file.
        self._rootWnd.title(f.name)

        # Close the file.
        f.close()

        # Set the flag indicating that the current file is saved.
        self._curFileIsSaved = True

    # Method to run the program using the specified Python interpreter.
    def _runProgram(self, e=None) -> None:
        # If the current open file is untitled, initiate the "Save As" process.
        if self._curOpenFile == "untitled":
            self._saveAsFile()

        # If the current file is not saved, prompt the user to save it before running.
        if not self._curFileIsSaved:
            r = messagebox.askyesno("Save File", "Do you want to save the file before running?")
            if r:
                self._saveFile()

        # Determine the platform and construct the command to run the program.
        if platform.system() == "Windows":
            # On Windows, use subprocess with CREATE_NEW_CONSOLE to open a new console window.
            subprocess.Popen(
                f'{self._preferences["pyinterp"]} "{os.getcwd().replace(os.sep, "/")}/loks-interpreter.py" "{self._curOpenFile}"',
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # On other platforms, use subprocess with shell=True.
            subprocess.Popen(
                f'{self._preferences["pyinterp"]} "{os.getcwd().replace(os.sep, "/")}/loks-interpreter.py" "{self._curOpenFile}"',
                shell=True
            )

    # Method to run the program in debug mode using the specified Python interpreter.
    def _runDebug(self, e=None) -> None:
        # If the current open file is untitled, initiate the "Save As" process.
        if self._curOpenFile == "untitled":
            self._saveAsFile()

        # If the current file is not saved, prompt the user to save it before running.
        if not self._curFileIsSaved:
            r = messagebox.askyesno("Save File", "Do you want to save the file before running?")
            if r:
                self._saveFile()

        # Determine the platform and construct the command to run the program in debug mode.
        if platform.system() == "Windows":
            # On Windows, use subprocess with CREATE_NEW_CONSOLE to open a new console window.
            subprocess.Popen(
                f'{self._preferences["pyinterp"]} "{os.getcwd().replace(os.sep, "/")}/loks-interpreter.py" "{self._curOpenFile}" -d',
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # On other platforms, use subprocess with shell=True.
            subprocess.Popen(
                f'{self._preferences["pyinterp"]} "{os.getcwd().replace(os.sep, "/")}/loks-interpreter.py" "{self._curOpenFile}" -d',
                shell=True
            )

    # Method to visualize the AST (Abstract Syntax Tree) of the Loks code.
    def _visualize(self, e=None) -> None:
        # If the current open file is untitled, initiate the "Save As" process.
        if self._curOpenFile == "untitled":
            self._saveAsFile()

        # If the current file is not saved, prompt the user to save it before visualizing AST.
        if not self._curFileIsSaved:
            r = messagebox.askyesno("Save File", "Do you want to save the file before visualizing AST?")
            if r:
                self._saveFile()

        try:
            # Try creating a 'visualize' folder in the current directory if it doesn't exist.
            if "visualize" not in list(os.walk(f"{os.getcwd().replace(os.sep, '/')}"))[0][1]:
                os.mkdir(f"{os.getcwd().replace(os.sep, '/')}/visualize")
        except:
            # Show an error message if creating the 'visualize' folder fails.
            messagebox.showerror(
                "Error",
                f"The 'visualize' folder does not exist in the current directory, and Loks was unable to create it. "
                "Try adding a 'visualize' directory to the current directory manually, and try again."
            )
            return

        # Determine the platform and construct the command to visualize AST.
        if platform.system() == "Windows":
            # On Windows, use subprocess with CREATE_NEW_CONSOLE to open a new console window.
            subprocess.Popen(
                f'{self._preferences["pyinterp"]} "{os.getcwd().replace(os.sep, "/")}/loks-interpreter.py" "{self._curOpenFile}" -g "{os.getcwd().replace(os.sep, "/")}/visualize/{os.path.basename(self._curOpenFile)}"',
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # On other platforms, use subprocess with shell=True.
            subprocess.Popen(
                f'{self._preferences["pyinterp"]} "{os.getcwd().replace(os.sep, "/")}/loks-interpreter.py" "{self._curOpenFile}" -g "{os.getcwd().replace(os.sep, "/")}/visualize/{os.path.basename(self._curOpenFile)}"',
                shell=True
            )