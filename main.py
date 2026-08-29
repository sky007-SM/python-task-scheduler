# Python Task Scheduler

import calendar # Imported calendar for date advancement calculations
from datetime import (
    datetime,
    timedelta,
)  # Imported datetime to get date of entry, and timedelta for duration
from typing import Self, TypedDict  # Imported Self and TypedDict for explicit typing
import os  # Imported os to check operating system type
import sys  # Imported sys to read keyboard byte input and manage terminal


# Explicit typing for the Data type task_attributes using TypedDict
class TaskAttributes(TypedDict, total=False):
    task_id: str
    name: str
    priority: str
    duration: str
    category: str
    due_date: str
    recurrence: str
    status: str


type task_attributes = TaskAttributes


def clear_screen() -> None:
    # ANSI escape sequence \033[H moves cursor to top-left
    # ANSI escape sequence \033[2J erases the entire screen
    # ANSI escape sequence \033[3J erases entire scrollback Buffer
    print("\033[H\033[2J\033[3J", end="")


def clear_last_line(count: int) -> None:
    # ANSI escape sequence \033[F moves cursor up 1 line
    # ANSI escape sequence \033[K erases from cursor to end of line
    print("\033[F\033[K" * count, end="", flush=True)

def add_month(date: datetime) -> datetime:
    """Advances datetime by 1 month, handling year rollover and day clamping cleanly."""
    month = date.month % 12 + 1 # Calculates target month (1-12) and wraps Dec (12) to Jan (1)
    year = date.year + (date.month // 12) # Increments year by 1 if current month is Dec (12)
    max_days = calendar.monthrange(year, month)[1] # Gets total days in target month (handles leap years)
    day = min(date.day, max_days) # limit day to month's max days to prevent invalid date errors
    return date.replace(year=year, month=month, day=day)

class Style:
    """Style Class containing required colours for output formatting"""

    # Formatting Reset
    RESET = "\033[0m"

    # Text Attributes
    BOLD = "\033[1m"

    # Bright Foreground Colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background Colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_ORANGE = "\033[48;5;208m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @classmethod
    def apply(cls, text: str, *styles: str) -> str:
        """Applies one or more ANSI styles to a string and appends RESET automatically.
        * is the extendable iterable unpacking operator, that accepts multiple
        arguments and allows packing and unpacking them from a collection"""
        combined_style = "".join(styles)
        return f"{combined_style}{text}{cls.RESET}"


# Checks whether operating system is Windows
if os.name == "nt":
    """Imports Microsoft Visual C++ Runtime module for access to low level console I/O functions"""
    import msvcrt

    def get_input() -> str | None:
        """Reads a single keypress from the console and returns it immediately as a byte string
        (built in byte object) without printing it to the screen (echoing) or waiting for Enter
        """

        key_input: bytes = msvcrt.getch()
        if key_input in (b"\x00", b"\xe0"):  # Arrow keys prefix on Windows
            key_input = msvcrt.getch()

            return {"H": "UP", "P": "DOWN", "K": "LEFT", "M": "RIGHT"}.get(
                key_input.decode("ascii", "ignore"), ""
            )
        # Checks if the key was Carriage Return (\r) or Line Feed (\n)
        if key_input in (b"\r", b"\n"):
            return "ENTER"
        # Returns an empty string for any unhandled key
        return ""


# Checks whether operating system is not Windows, ie Mac or linux (posix)
else:
    import tty, termios

    """Imports Unix-specific standard library modules. termios handles low-level terminal I/O 
        controls, while tty provides utility functions to alter terminal modes."""

    def get_input() -> str | None:
        """Reads a single keypress from the console and returns it immediately as a byte string
        (built in byte object) without printing it to the screen (echoing) or waiting for Enter
        """

        # Fetches the integer File Descriptor (fd) associated with standard input (keyboard stream).
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        """Reads and stores the current attributes/settings of the 
            terminal device (e.g., line buffering, character echo). 
            This backup is saved so settings can be restored later"""
        try:
            tty.setraw(sys.stdin.fileno())
            """ tty.setraw Switches the terminal from "canonical" mode (line-buffered, echoing typed characters) to "raw" mode. 
                In raw mode, character echoing is disabled and keypresses are instantly available to the program."""
            ch = sys.stdin.read(
                1
            )  # Reads exactly 1 byte/character directly from standard input stream without waiting for Enter.
            if ch == "\x1b":
                """Checks if the pressed key is the Escape character (\x1b in hex, or ASCII 27).
                Terminal arrow keys send multi-character ANSI escape sequences that all start with \x1b
                """
                ch2 = sys.stdin.read(2)
                # reads the next 2 characters from the input stream to capture the rest of the escape sequence.
                if ch2 == "[A":
                    return "UP"
                if ch2 == "[B":
                    return "DOWN"
                if ch2 == "[C":
                    return "RIGHT"
                if ch2 == "[D":
                    return "LEFT"
                # Returns an empty string for any unhandled key
                return ""
            # Checks if the key was Carriage Return (\r) or Line Feed (\n)
            elif ch in ("\r", "\n"):
                return "ENTER"
        finally:
            """finally Guarantees that the cleanup code executes regardless of whether try succeeded or threw an error.
            termios.tcsetattr(...): Restores the terminal settings back to their original state (old_settings).
            TCSADRAIN ensures the mode changes only after all queued output has been fully written to the screen.
            """
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Returns an empty string for any unhandled key
        return ""


def interactive_menu(options: list[str], menu_header: str) -> str:
    selected_index: int = 0  # To ensure first option is always selected first

    while True:
        clear_screen()
        print(Style.apply(menu_header, Style.BOLD))
        print(f"\n(Use ↑/↓ and Press ENTER)\n")

        """The enumerate built in function offers alternative way to access both index and value
            of element in an iterable collection with using len() and range() functions. It returns 
            and unpacks tuple of value from iterable and an integer start value we can set which 
            defaults to 0. Syntax enumerate(iterable, start = 0) """

        for index, option in enumerate(options):
            # Corresponding Style is applied based on selection of option for emphasis
            if index == selected_index:
                print(
                    Style.apply(f"❯ [ {option} ]", Style.BRIGHT_WHITE, Style.BG_ORANGE)
                )
            else:
                print(f"    [ {option} ]")

        key_input: str = (
            get_input()
        )  # Function that reads keyboard input for arrow keys and "ENTER"

        # Matches Key input to corresponding output
        if key_input == "UP":
            # Moves the highlighted option when arrow key input is detected
            selected_index = (selected_index - 1) % (len(options))
        elif key_input == "DOWN":
            # Using modulus with total length ensures buttons will wrap from bottom to top or vice versa
            selected_index = (selected_index + 1) % (len(options))
        elif key_input == "ENTER":
            clear_screen()
            return options[selected_index]


def buttons(
    options: list[str],
    colour_bg: str | None,
    colour_bright: str | None,
    menu_button: bool,
    toggle: bool,
) -> str | list[str]:
    selected_index: int = 0  # To ensure first option is always selected first
    last_index: int = len(options) - 1  # Equivalent to index -1
    second_last_index: int = len(options) - 2  # Equivalent to index -2
    toggled_buttons: list[str] = []  # Stores attributes enabled as string
    if not toggle:
        print(f"\n(Use ←/→ and Press ENTER)\n")
    else:
        print(
            f"\n(Use ←/→ and Press ENTER to toggle selection, and confirm selected attributes)\n"
        )

    while True:
        if not toggle:

            """The enumerate built in function offers alternative way to access both index and value
            of element in an iterable collection with using len() and range() functions. It returns
            and unpacks tuple of value from iterable and an integer start value we can set which
            defaults to 0. Syntax enumerate(iterable, start = 0)"""

            for index, option in enumerate(options):
                selected: bool = selected_index == index
                # Checks whether menu navigation options are needed
                if menu_button:
                    # Display Menu Button Quit
                    if index == last_index:
                        if selected:
                            print(
                                Style.apply(
                                    f"❯ [ {option} ]",
                                    Style.BOLD,
                                    Style.BG_WHITE,
                                    Style.BRIGHT_RED,
                                ),
                                end="  ",
                            )
                        else:
                            print(
                                Style.apply(
                                    f"    [ {option} ]",
                                    Style.BG_RED,
                                    Style.BRIGHT_WHITE,
                                ),
                                end="  ",
                            )
                    # Displays Menu Button Return to Menu
                    elif index == second_last_index:
                        if selected:
                            print(
                                Style.apply(
                                    f"❯ [ {option} ]",
                                    Style.BOLD,
                                    Style.BG_RED,
                                    Style.BRIGHT_WHITE,
                                ),
                                end="  ",
                            )
                        else:
                            print(
                                Style.apply(f"    [ {option} ]", Style.BRIGHT_RED),
                                end="  ",
                            )
                    # Displays Extra Action buttons
                    else:
                        if selected:
                            print(
                                Style.apply(
                                    f"❯ [ {option} ]",
                                    Style.BOLD,
                                    colour_bg,
                                    Style.BRIGHT_WHITE,
                                ),
                                end="  ",
                            )
                        else:
                            print(
                                Style.apply(f"    [ {option} ]", colour_bright),
                                end="  ",
                            )
                # Display only action buttons
                else:
                    if selected:
                        print(
                            Style.apply(
                                f"❯ [ {option} ]",
                                Style.BOLD,
                                colour_bg,
                                Style.BRIGHT_WHITE,
                            ),
                            end="  ",
                        )
                    else:
                        print(Style.apply(f"    [ {option} ]", colour_bright), end="  ")
        else:

            """The enumerate built in function offers alternative way to access both index and value
            of element in an iterable collection with using len() and range() functions. It returns
            and unpacks tuple of value from iterable and an integer start value we can set which
            defaults to 0. Syntax enumerate(iterable, start = 0)"""

            for index, option in enumerate(options):
                selected: bool = selected_index == index
                if option in toggled_buttons:  # Allows Toggle, and untoggle
                    if selected:
                        print(
                            Style.apply(
                                f"❯ [ {option} ]",
                                Style.BOLD,
                                Style.BG_WHITE,
                                Style.BRIGHT_BLUE,
                            ),
                            end="  ",
                        )
                    else:
                        print(
                            Style.apply(
                                f"    [ {option} ]",
                                Style.BOLD,
                                Style.BG_BLUE,
                                Style.BRIGHT_WHITE,
                            ),
                            end="  ",
                        )
                # Displays button to confirm selection and return values
                elif index == last_index:
                    # newline added 3 times to display button distinctly below toggle options
                    if selected:
                        print(
                            Style.apply(
                                f"\n\n\n❯ [ {option} ]",
                                Style.BOLD,
                                Style.BG_WHITE,
                                Style.BRIGHT_GREEN,
                            ),
                            end="  ",
                        )
                    else:
                        print(
                            Style.apply(
                                f"\n\n\n    [ {option} ]",
                                Style.BG_GREEN,
                                Style.BRIGHT_WHITE,
                            ),
                            end="  ",
                        )

                else:
                    if selected:
                        print(
                            Style.apply(
                                f"❯ [ {option} ]",
                                Style.BOLD,
                                Style.BG_WHITE,
                                Style.BRIGHT_CYAN,
                            ),
                            end="  ",
                        )
                    else:
                        print(
                            Style.apply(
                                f"    [ {option} ]",
                                Style.BOLD,
                                Style.BG_CYAN,
                                Style.BRIGHT_WHITE,
                            ),
                            end="  ",
                        )
        """ The flush=True forces Python to immediately push any buffered output 
            directly to the terminal screen without waiting for newline character 
            for drawing text, unlike its default line buffered output type"""
        print(flush=True)
        key_input: str = (
            get_input()
        )  # Function that reads keyboard input for arrow keys and "ENTER"

        if key_input == "LEFT":
            # Moves the highlighted option when arrow key input is detected
            selected_index = (selected_index - 1) % (len(options))
            if toggle:
                clear_last_line(4)
            else:
                clear_last_line(1)
        elif key_input == "RIGHT":
            # Using modulus with total length ensures buttons will wrap from bottom to top or vice versa
            selected_index = (selected_index + 1) % (len(options))
            if toggle:
                clear_last_line(4)
            else:
                clear_last_line(1)
        elif key_input == "ENTER":
            if toggle:
                if selected_index == last_index:
                    if (
                        toggled_buttons
                    ):  # Ensures Atleast one attribute is selected for sorting
                        clear_screen()
                        return toggled_buttons
                    else:
                        print(Style.apply("Set Priority to Continue", Style.BRIGHT_RED, Style.BOLD))

                else:
                    # Handles the button toggle mechanic by altering list accordingly
                    selected_option = options[selected_index]
                    if selected_option in toggled_buttons:
                        toggled_buttons.remove(selected_option)
                    else:
                        toggled_buttons.append(selected_option)
                    clear_last_line(4)

            else:
                clear_screen()
                return options[selected_index]
        else:
            # Condition to clear buttons regardless of key input
            if toggle:
                clear_last_line(4)
            else:
                clear_last_line(1)


class Task:

    def __init__(
        self,
        task_id: int,
        name: str,
        priority: int,
        duration: timedelta,
        category: str,
        due_date: datetime,
        recurrence: str,
        status: str = "Pending",
    ) -> None:
        """Initializes Task attributes that are given below, status is the only attribute with default value
        used when adding task, this enables previously created tasks retain their status while loading from file
        """

        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.duration = duration
        self.status = status
        self.category = category
        self.due_date = due_date
        self.recurrence = recurrence

    def task_status(self, start_task: bool, undo_task: bool) -> None:
        """Updates Status of a Task depending on boolean flags passed"""

        if start_task:
            self.status = "Running"
        elif undo_task:
            self.status = "Pending"
        else:
            self.status = "Completed"

    def display_task(self, view: bool = True) -> str | None:
        """Method To Display formatted Task details if viewed by user or
        produce formatted string used when saving the markdown file"""
        duration_mins = int(self.duration.total_seconds() // 60)
        due_date_str: str = self.due_date.strftime("%Y-%m-%d")  #
        if not view:
            return (
                "---\n"
                f"task_id: {self.task_id}\n"
                f"name: {self.name}\n"
                f"priority: {self.priority}\n"
                f"duration: {duration_mins}\n"
                f"status: {self.status}\n"
                f"category: {self.category}\n"
                f"due_date: {due_date_str}\n"
                f"recurrence: {self.recurrence}\n"
                "---\n"
            )
        else:
            due_date: datetime = self.due_date + timedelta(days=1)
            # Adds Text Formatting Based to indicate overdue status
            if due_date < datetime.now():
                date_style = Style.BRIGHT_RED
            else:
                date_style = Style.BRIGHT_GREEN
            print(
                f"task_id: {self.task_id}\n"
                f"name: {Style.apply(self.name, Style.BOLD, Style.BG_WHITE)}\n"
                f"category: {Style.apply(self.category, Style.BOLD, Style.BG_WHITE)}\n"
                f"priority: {self.priority} | duration: {duration_mins}\n"
                f"status: {self.status} | due_date: {Style.apply(due_date_str, date_style)} | recurrence: {self.recurrence}\n\n"
            )

    @classmethod  # Decorator used to create a class, ie an alternative constructor
    def get_details(cls, record: task_attributes) -> Self:
        """Method that loads corresponding data from dictionary and creates object of class Task,
        Corresponding conversions to required type is also performed before passing the arguments
        """

        return cls(
            task_id=int(record["task_id"]),
            name=record["name"],
            priority=int(record["priority"]),
            duration=timedelta(
                hours=int(record["duration"])
                // 60,  # Integer division converts minutes to hour
                minutes=int(record["duration"])
                % 60,  # Modulus used to obtain remaining minutes
            ),
            category=record["category"],
            # String parse time function creates datetime object from string
            due_date=datetime.strptime(record["due_date"], "%Y-%m-%d"),
            recurrence=record["recurrence"],
            status=record["status"],  # Only Constructor that passes status argument
        )


class FileManager:

    def __init__(self, file_location: str) -> None:
        """Initializes File Manager Instance with file location as only attribute"""

        self.file_location = file_location

    def load_tasks(self) -> list[Task]:
        """Method to Load Tasks from corresponding markdown file and create Task object
        and of all uncorrupted data, returns the list of tasks created from the data"""

        tasks: list[Task] = []
        current_data: task_attributes = {}
        inside_block: bool = False
        try:
            # Markdown file format opened with encoding="utf-8"
            with open(self.file_location, "r", encoding="utf-8") as file:
                for line in file:
                    line_str: str = line.strip()
                    if line_str == "---":
                        if inside_block:
                            # Reached closing '---', process task if data exists
                            if current_data:
                                try:
                                    task: Task = Task.get_details(current_data)
                                    if task:
                                        tasks.append(task)

                                except (KeyError, ValueError, TypeError):
                                    """Key error handles exception if the invoked key does not exist in dictionary"""
                                    pass  # Skip corrupted/malformed task blocks safely
                                current_data = {}
                            inside_block = False
                        else:
                            inside_block = True
                        continue

                    # Parse Data as Key-Value Pairs in the dictionary
                    if inside_block and ":" in line_str:
                        key, val = line_str.split(":", 1)
                        current_data[key.strip()] = val.strip()

                # EOF Safety Check: Parse any trailing block missing a closing '---'
                if inside_block and current_data:
                    try:
                        task: Task = Task.get_details(current_data)
                        if task:
                            tasks.append(task)
                    except (KeyError, ValueError, TypeError):
                        # Skips corrupted record safely
                        pass

                return tasks
        except FileNotFoundError:
            return []

    def save_tasks(self, records: list[Task]) -> None:
        """Method that saves the tasks to markdown file"""

        # Markdown file format opened with encoding="utf-8"
        with open(self.file_location, "w", encoding="utf-8") as file:
            for record in records:
                file.write(f"{record.display_task(False)}\n")

    def export_report(self, report_str: str) -> None:
        """Method that creates report for export report option from view stats"""

        # Markdown file format opened with encoding="utf-8"
        with open(
            "file-manager/markdown-files/report.md", "w", encoding="utf-8"
        ) as file:
            file.write("# Tasks Report\n\n")
            file.write(report_str)
            file.write("\n---")


class Scheduler:

    # Initializes File Manager Instance for Task Scheduler (Class attribute) with location
    tasks_manager: FileManager = FileManager("file-manager/markdown-files/tasks.md")

    def __init__(self) -> None:
        """Initializes Scheduler Instance with tasks list as only attribute"""

        # Invokes functions that loads records from markdown file
        self.tasks_list: list[Task] = Scheduler.tasks_manager.load_tasks()

    def menu_navigation_buttons(self) -> None:
        """Handles universal navigation options at the end of operations."""
        action: str = buttons(["Return to Menu", "Quit"], None, None, True, False)
        if action == "Quit":
            Scheduler.tasks_manager.save_tasks(self.tasks_list) # Invokes function to save task to file
            sys.exit(0)

    def add_task(self) -> None:
        """Method that accepts data from user to create Task object with status set to Pending"""

        existing_ids: list[int] = [task.task_id for task in self.tasks_list]
        new_id: int = 1
        while new_id in existing_ids:
            new_id += 1
        task_id: int = new_id
        while True:
            name: str = input("Enter Task Name: ").title().strip()
            if not name:  # Ensures empty string is not accepted
                print(Style.apply("Name cannot be empty", Style.BRIGHT_RED, Style.BOLD))
            else:
                break
        while True:
            try:
                priority: int = int(
                    input("Enter Task Priority on a scale from 1 to 10: ")
                )
            except ValueError:
                print(Style.apply("Error: Invalid input enter a valid number", Style.BRIGHT_RED, Style.BOLD))
            else:
                # Ensures priority is always between 1 and 10
                if priority in range(1, 11):
                    break
                else:
                    print(Style.apply("Priority must be on a scale from 1 to 10, Try again", Style.BRIGHT_YELLOW, Style.BOLD))
        while True:
            user_input: str = input(
                "Enter Task Duration in hours and minutes (HH:MM): "
            ).strip()

            # Parses corresponding hour and minutes values to create timedelta object
            try:
                duration_data: list[str] = user_input.split(":")
                if (
                    int(duration_data[1]) <= 59
                ):  # Ensures minutes value is always less than 60
                    duration: timedelta = timedelta(
                        hours=int(duration_data[0]), minutes=int(duration_data[1])
                    )
                    break
                else:
                    print(Style.apply("Minutes (MM) must be a value from 0 to 59", Style.BRIGHT_YELLOW, Style.BOLD))
            except (ValueError, IndexError):
                print(Style.apply("Error: Invalid format, please use HH:MM ", Style.BRIGHT_RED, Style.BOLD))
        while True:
            category: str = input("Enter Task Category: ").title().strip()
            if not category:  # Ensures empty string is not accepted
                print(Style.apply("Category cannot be empty", Style.BRIGHT_RED, Style.BOLD))
            else:
                break
        while True:
            user_input: str = input("Enter Task Due Date (YYYY-MM-DD): ").strip()
            try:
                due_date: datetime = datetime.strptime(user_input, "%Y-%m-%d")
            except ValueError:
                print(Style.apply("Error: Invalid format, please use YYYY-MM-DD ", Style.BRIGHT_RED, Style.BOLD))
            else:
                break

        # Recurrence is selected via menu
        recurrence: str = interactive_menu(
            ["None", "Daily", "Weekly", "Monthly"],
            "======= Choose Recurrence Type =======",
        )
        new_task: Task = Task(
            task_id, name, priority, duration, category, due_date, recurrence
        )  # status will take default value of pending since its new taask
        self.tasks_list.append(new_task)
        print(Style.apply("Task has been successfully added", Style.BRIGHT_GREEN, Style.BOLD))

        self.menu_navigation_buttons()

    def execute_task(self) -> None:
        """Method that is used to sort priority and execute highest priority task"""

        scheduled_task: list[Task] = [
            task for task in self.tasks_list if task.status == "Pending"
        ]
        if scheduled_task:
            task_type: str = interactive_menu(
                ["Execute Highest Priority", "Set Priority"],
                f"\n======= Task Scheduler =======\n",
            )
            match task_type:

                case "Execute Highest Priority":
                    # Sorts priority while considering all the relevant attributes
                    scheduled_task.sort(
                        key=lambda task: (
                            -task.priority,
                            task.due_date,
                            task.duration,
                            task.task_id,
                        )
                    )
                    scheduled_task[0].task_status(True, False)
                    print(Style.apply("Executing highest priority Task", Style.BRIGHT_GREEN, Style.BOLD))

                case "Set Priority":
                    # Provides user the options to choose attributes for priority sort
                    attributes: list[str] = [
                        "Priority",
                        "Due Date",
                        "Duration",
                        "Task ID",
                    ]
                    # Toggle Buttons are utilised for this option
                    attribute_priorities: str = buttons(
                        attributes + ["Confirm Selection"], None, None, False, True
                    )

                    def sort_key(task: Task) -> tuple:
                        key: tuple = ()
                        if attributes[0] in attribute_priorities:
                            key += (-task.priority,)
                        if attributes[1] in attribute_priorities:
                            key += (task.due_date,)
                        if attributes[2] in attribute_priorities:
                            key += (task.duration,)
                        if attributes[3] in attribute_priorities:
                            key += (task.task_id,)
                        return key

                    # Paranthesis is not required since key function passes values directly
                    scheduled_task.sort(key=sort_key)
                    scheduled_task[0].task_status(True, False)
                    print(Style.apply("Executing highest priority Task", Style.BRIGHT_GREEN, Style.BOLD))

            # Menu option buttons to exit function or perform further actions
            action: str = buttons(
                ["Undo Executed Task", "Return to Menu", "Quit"],
                Style.BG_YELLOW,
                Style.BRIGHT_YELLOW,
                True,
                False,
            )

            match action:
                case "Undo Executed Task":
                    # Undoes the previously executed Task
                    scheduled_task[0].task_status(False, True)
                    clear_screen()
                    print(Style.apply("Status has been reset for Last Executed Task", Style.BRIGHT_GREEN, Style.BOLD))
                    self.menu_navigation_buttons()

                case "Return to Menu":
                    return

                case "Quit" | None:
                    Scheduler.tasks_manager.save_tasks(
                        self.tasks_list
                    )  # Invokes function to save task to file
                    sys.exit(0)
        else:
            print(Style.apply("No Task Remaining to Execute", Style.BRIGHT_YELLOW, Style.BOLD))

            self.menu_navigation_buttons()

    def modify_task(self, delete: bool):
        """Method that can search for tasks by name, and delete or display the task
        depending on whether boolean passed is True or False. The method stores
        all Tasks that have corresponding name and displays them in search mode.
        For delete mode it deletes first task object with matching name"""

        if self.tasks_list:
            while True:
                if delete:
                    name: str = input("Enter Task Name to Delete: ").title().strip()
                else:
                    name: str = input("Enter Task Name to Search: ").title().strip()
                if not name:  # Ensures empty string is not accepted
                    print(Style.apply("Name cannot be empty", Style.BRIGHT_RED, Style.BOLD))
                else:
                    break
            if delete:
                for task in self.tasks_list:
                    if task.name == name:
                        self.tasks_list.remove(task)
                        print(Style.apply(f"Task: {name}, has been successfully removed", Style.BRIGHT_GREEN, Style.BOLD))
                        break
                else:
                    print(Style.apply("No Matching Tasks Found", Style.BRIGHT_YELLOW, Style.BOLD))
            else:
                matched_tasks: list[Task] = [
                    task for task in self.tasks_list if task.name.startswith(name)
                ]
                if matched_tasks:
                    print(Style.apply("======= Search Results =======", Style.BG_BLUE, Style.BOLD))
                    for task in matched_tasks:
                        task.display_task()
                    print(f"\nTotal Matching Tasks: {len(matched_tasks)}")
                else:
                    print(Style.apply("No Matching Tasks Found", Style.BRIGHT_YELLOW, Style.BOLD))

        else:
            print(Style.apply("No Tasks Are Scheduled", Style.BRIGHT_YELLOW, Style.BOLD))

        self.menu_navigation_buttons()

    def filter_tasks(self) -> None:
        """Method that provides options to filter tasks by attributes and value and
        display results of filter applied, when invoked from view tasks"""

        filter_options: list[str] = [
            "Priority",
            "Status",
            "Due Date",
            "Duration",
            "Category",
            "Recurrence",
            "Return to View Tasks",
        ]
        filter_type: str = interactive_menu(
            filter_options, "\n======= Filter Tasks By ======="
        )

        # Exits filter menu and returns user to view tasks
        if filter_type == "Return to View Tasks":
            return

        filtered_results: list[Task] = []

        # Filter Tasks by Priority
        if filter_type == "Priority":
            while True:
                try:
                    priority: int = int(
                        input("Enter Task Priority on a scale from 1 to 10: ")
                    )
                except ValueError:
                    print(Style.apply("Error: Invalid input enter a valid number ", Style.BRIGHT_RED, Style.BOLD))
                else:
                    if priority in range(1, 11):
                        break
                    else:
                        print(Style.apply("Priority must be on a scale from 1 to 10, Try again", Style.BRIGHT_YELLOW, Style.BOLD))

            # Buttons function invoked without menu options
            compare_choice: str = buttons(
                ["Greater Than ( > )", "Lesser Than ( < )", "Equals ( = )"],
                Style.BG_GREEN,
                Style.BRIGHT_GREEN,
                False,
                False,
            )

            if compare_choice == "Greater Than ( > )":
                filtered_results = [
                    task for task in self.tasks_list if task.priority > priority
                ]
            elif compare_choice == "Lesser Than ( < )":
                filtered_results = [
                    task for task in self.tasks_list if task.priority < priority
                ]
            else:
                filtered_results = [
                    task for task in self.tasks_list if task.priority == priority
                ]

        # Filter Tasks by Status
        elif filter_type == "Status":
            status_type: str = interactive_menu(
                ["Pending", "Running", "Completed"], "\n======= Select Status ======="
            )
            filtered_results = [
                task for task in self.tasks_list if task.status == status_type
            ]

        # Filter Tasks by Due Date
        elif filter_type == "Due Date":
            while True:
                user_input: str = input("Enter Task Due Date (YYYY-MM-DD): ").strip()
                try:
                    target_date: datetime = datetime.strptime(user_input, "%Y-%m-%d")
                except ValueError:
                    print(Style.apply("Error: Invalid format, please use YYYY-MM-DD", Style.BRIGHT_RED, Style.BOLD))
                else:
                    break

            # Buttons function invoked without menu options
            compare_choice: str = buttons(
                ["Due After ( > )", "Due Before ( < )", "Due On ( = )"],
                Style.BG_GREEN,
                Style.BRIGHT_GREEN,
                False,
                False,
            )

            if compare_choice == "Due After ( > )":
                filtered_results = [
                    task for task in self.tasks_list if task.due_date > target_date
                ]
            elif compare_choice == "Due Before ( < )":
                filtered_results = [
                    task for task in self.tasks_list if task.due_date < target_date
                ]
            else:
                filtered_results = [
                    task for task in self.tasks_list if task.due_date == target_date
                ]

        # Filter Tasks by Duration
        elif filter_type == "Duration":
            while True:
                user_input: str = input(
                    "Enter Task Duration in hours and minutes (HH:MM): "
                ).strip()
                try:
                    duration_data: list[str] = user_input.split(":")
                    if (
                        int(duration_data[1]) <= 59
                    ):  # Ensures minutes value is always less than 60
                        target_duration: timedelta = timedelta(
                            hours=int(duration_data[0]), minutes=int(duration_data[1])
                        )
                        break
                    else:
                        print(Style.apply("Minutes (MM) must be a value from 0 to 59", Style.BRIGHT_YELLOW, Style.BOLD))
                except (ValueError, IndexError):
                    print(Style.apply("Error: Invalid format, please use HH:MM ", Style.BRIGHT_RED, Style.BOLD))

            # Buttons function invoked without menu options
            compare_choice: str = buttons(
                ["Greater Than ( > )", "Lesser Than ( < )", "Equals ( = )"],
                Style.BG_GREEN,
                Style.BRIGHT_GREEN,
                False,
                False,
            )

            if compare_choice == "Greater Than ( > )":
                filtered_results = [
                    task for task in self.tasks_list if task.duration > target_duration
                ]
            elif compare_choice == "Lesser Than ( < )":
                filtered_results = [
                    task for task in self.tasks_list if task.duration < target_duration
                ]
            else:
                filtered_results = [
                    task for task in self.tasks_list if task.duration == target_duration
                ]

        # Filter Tasks by Category
        elif filter_type == "Category":
            while True:
                category: str = input("Enter Task Category: ").title().strip()
                if not category:  # Ensures empty string is not accepted
                    print(Style.apply("Category cannot be empty", Style.BRIGHT_RED, Style.BOLD))
                else:
                    break
            filtered_results = [
                task for task in self.tasks_list if task.category == category
            ]

        # Filter Tasks by Recurrence
        elif filter_type == "Recurrence":
            recurrence_type: str = interactive_menu(
                ["None", "Daily", "Weekly", "Monthly"], "\nSelect Recurrence:"
            )
            filtered_results = [
                task for task in self.tasks_list if task.recurrence == recurrence_type
            ]

        clear_screen()
        if filtered_results:
            print(Style.apply(f"======= Filtered Tasks ({filter_type}) =======\n", Style.BG_BLUE, Style.BOLD))
            for task in filtered_results:
                task.display_task()
        else:
            print(
                Style.apply(
                    "No matching tasks found for the given criteria.",
                    Style.BRIGHT_YELLOW, Style.BOLD
                )
            )

    def view_tasks(self) -> None:
        """Method that displays all existing tasks and allows user to filter tasks by
        the attributes, priority, status, duration, due date, category or recurrence"""

        if self.tasks_list:
            print(Style.apply(f"======= All Tasks =======", Style.BG_BLUE, Style.BOLD))
            for task in self.tasks_list:
                task.display_task()

            # Menu option buttons to exit function or perform further actions
            action: str = buttons(
                ["Filter Tasks", "Return to Menu", "Quit"],
                Style.BG_YELLOW,
                Style.BRIGHT_YELLOW,
                True,
                False,
            )

            match action:
                case "Filter Tasks":
                    self.filter_tasks()

                case "Return to Menu":
                    return

                case "Quit" | None:
                    Scheduler.tasks_manager.save_tasks(
                        self.tasks_list
                    )  # Invokes function to save task to file
                    sys.exit(0)

        else:
            print(Style.apply("No Tasks have been Scheduled", Style.BRIGHT_YELLOW, Style.BOLD))

        self.menu_navigation_buttons()

    def view_stats(self) -> None:
        """Method that calculates stats of existing tasks such as count of Total,
        pending, running, overdue and completed tasks, Highest priority,
        and average duration. It also has option export report as markdown file"""

        total: int = len(self.tasks_list)
        if total == 0:
            print(Style.apply("No task data available.", Style.BRIGHT_YELLOW, Style.BOLD))

            self.menu_navigation_buttons()

        else:
            print(Style.apply("======= Task Statistics =======", Style.BG_BLUE, Style.BOLD))
            pending: int = sum(
                1 for task in self.tasks_list if task.status == "Pending"
            )
            running: int = sum(
                1 for task in self.tasks_list if task.status == "Running"
            )
            completed: int = sum(
                1 for task in self.tasks_list if task.status == "Completed"
            )
            overdue: int = sum(
                1
                for task in self.tasks_list
                if (task.due_date + timedelta(days=1) < datetime.now())
            )
            max_priority: int = max(task.priority for task in self.tasks_list)
            avg_duration: float = (
                sum((task.duration.total_seconds() // 60) for task in self.tasks_list)
                / total
            )
            report_str: str = (
                f"Total Tasks:        {total}\n"
                f"Pending Tasks:      {pending}\n"
                f"Running Tasks:      {running}\n"
                f"Completed Tasks:    {completed}\n"
                f"Overdue Tasks:      {overdue}\n"
                f"Highest Priority:   {max_priority}\n"
                f"Avg Duration:       {avg_duration:.1f} mins\n"
            )

            print(report_str)

            # Menu option buttons to exit function or perform further actions
            action: str = buttons(
                ["Export Report", "Return to Menu", "Quit"],
                Style.BG_YELLOW,
                Style.BRIGHT_YELLOW,
                True,
                False,
            )

            match action:
                case "Export Report":
                    # Creates Markdown file of Statistics report
                    Scheduler.tasks_manager.export_report(report_str)
                    clear_screen()
                    self.menu_navigation_buttons()

                case "Return to Menu":
                    return

                case "Quit" | None:
                    Scheduler.tasks_manager.save_tasks(
                        self.tasks_list
                    )  # Invokes function to save task to file
                    sys.exit(0)

    def finish_task(self):
        """Method that accepts name of Task and mark corresponding Task as Completed"""

        ongoing_tasks: list[Task] = [
            task for task in self.tasks_list if task.status == "Running"
        ]
        if ongoing_tasks:
            print(Style.apply("======= Ongoing Tasks =======", Style.BG_BLUE, Style.BOLD))
            for task in ongoing_tasks:
                task.display_task()
            while True:
                name: str = input("\nEnter Task Name to search: ").title().strip()
                if not name:  # Ensures empty string is not accepted
                    print(Style.apply("Name cannot be empty", Style.BRIGHT_RED, Style.BOLD))
                else:
                    break

            recurrence_exists: bool = False
            task_index: int = 0
            target_found: bool = False
            for task in ongoing_tasks:

                if task.name == name:
                    target_found = True
                    next_due: datetime = task.due_date
                    task_index = ongoing_tasks.index(task)
                    # Handles Tasks with Recurrence while
                    if task.recurrence != "None":
                        recurrence_exists = True
                        if task.recurrence == "Daily":
                            next_due += timedelta(days=1)
                        elif task.recurrence == "Weekly":
                            next_due += timedelta(weeks=1)
                        elif task.recurrence == "Monthly":
                            next_due = add_month(task.due_date)
                        existing_ids: list[int] = [
                            task.task_id for task in self.tasks_list
                        ]
                        new_id: int = 1
                        while new_id in existing_ids:
                            new_id += 1
                        task_id: int = new_id
                        # Creates next iteration for tasks with recurrence
                        # The due date is advanced by corresponding interval
                        reccuring_task: Task = Task(
                            task_id,
                            task.name,
                            task.priority,
                            task.duration,
                            task.category,
                            next_due,
                            task.recurrence,
                        )
                        self.tasks_list.append(reccuring_task)
                    task.task_status(False, False)
                    task.display_task()
                    print(Style.apply("\nTask Completed", Style.BRIGHT_GREEN, Style.BOLD))
                    break

            if target_found:
                # Menu option buttons to exit function or perform further actions
                action: str = buttons(
                    ["Undo Executed Task", "Return to Menu", "Quit"],
                    Style.BG_YELLOW,
                    Style.BRIGHT_YELLOW,
                    True,
                    False,
                )

                match action:
                    case "Undo Executed Task":
                        # Undoes the previously completed Task
                        ongoing_tasks[task_index].task_status(True, False)
                        if recurrence_exists:
                            # Removes new iteration of recurring task added
                            self.tasks_list.pop()
                        clear_screen()
                        print(Style.apply("Status has been reset for Last Completed Task", Style.BRIGHT_GREEN, Style.BOLD))
                        self.menu_navigation_buttons()

                    case "Return to Menu":
                        return

                    case "Quit" | None:
                        Scheduler.tasks_manager.save_tasks(
                            self.tasks_list
                        )  # Invokes function to save task to file
                        sys.exit(0)
            else:
                print(Style.apply("No Matching Tasks Found", Style.BRIGHT_YELLOW, Style.BOLD))

                self.menu_navigation_buttons()

        else:
            print(Style.apply("No Tasks Are Scheduled", Style.BRIGHT_YELLOW, Style.BOLD))

            self.menu_navigation_buttons()

    def scheduler_interface(self) -> None:
        """Serves as the main loop processing CLI inputs and performing
        corresponding functions continuously untill program exits"""

        menu_options: list[str] = [
            "Add Task",
            "Execute Task",
            "View Tasks",
            "Search Tasks",
            "Mark Task Completed",
            "Remove Task",
            "View Statistics",
            "Save Tasks",
            "Quit",
        ]
        while True:
            choice: str = interactive_menu(
                menu_options, f"\n======= Task Scheduler =======\n"
            )
            match choice:
                case "Add Task":
                    self.add_task()  # Invokes function to add new task

                case "Execute Task":
                    self.execute_task()  # Invokes function to execute task by priority

                case "View Tasks":
                    self.view_tasks()  # Invokes function to view tasks

                case "Search Tasks":
                    self.modify_task(False)  # Invokes function to search for task
                    # The False paramter sets the function to search mode

                case "Mark Task Completed":
                    self.finish_task()  # Invokes function to complete a task

                case "Remove Task":
                    self.modify_task(True)  # Invokes function to delete a task
                    # The True paramter sets the function to delete mode

                case "View Statistics":
                    self.view_stats()

                case "Save Tasks":
                    Scheduler.tasks_manager.save_tasks(
                        self.tasks_list
                    )  # Invokes function to save task to file

                case "Quit":
                    Scheduler.tasks_manager.save_tasks(
                        self.tasks_list
                    )  # Invokes function to save task to file
                    sys.exit(0)  # Exits the program


def main() -> None:
    # Initializes Task Scheduler Instance
    task_scheduler: Scheduler = Scheduler()
    task_scheduler.scheduler_interface()


# Guard header in case imported
if __name__ == "__main__":
    main()
