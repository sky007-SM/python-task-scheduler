# Python Task Scheduler

A command-line task scheduling application written in Python that allows users to create, manage, execute, search, filter, complete, and remove tasks through an interactive terminal interface. The application supports task priorities, durations, categories, due dates, recurring tasks, task status tracking, statistics, and persistent Markdown-based storage.

The scheduler uses an interactive keyboard-driven interface with arrow-key navigation, colored terminal output, custom priority ordering, and object-oriented design.

## Features

* Add new tasks
* Automatically assign unique task IDs
* Store task name, priority, duration, category, due date, recurrence, and status
* Set task priority from 1 to 10
* Set task duration using `HH:MM` format
* Set task due dates using `YYYY-MM-DD`
* Configure task recurrence
* Support `None`, `Daily`, `Weekly`, and `Monthly` recurrence
* Execute the highest-priority pending task
* Create custom task-priority ordering
* Prioritize tasks using multiple attributes
* Track task status
* Support `Pending`, `Running`, and `Completed` states
* Undo task execution
* Mark running tasks as completed
* Automatically create the next occurrence of recurring tasks
* Undo task completion
* Search tasks by name
* Search using partial task-name prefixes
* Remove tasks by name
* Filter tasks by priority
* Filter tasks by status
* Filter tasks by due date
* Filter tasks by duration
* Filter tasks by category
* Filter tasks by recurrence
* Compare numerical and time-based attributes using greater-than, lesser-than, and equals operations
* Display all scheduled tasks
* Display task statistics
* Calculate total, pending, running, completed, and overdue tasks
* Calculate highest task priority
* Calculate average task duration
* Export statistics as a Markdown report
* Manually save tasks
* Automatically save tasks when exiting
* Persistent Markdown-based file storage
* Recover valid tasks from corrupted or incomplete records
* Cross-platform keyboard input handling
* Colored terminal interface using ANSI escape sequences
* Arrow-key menu navigation
* Toggle-based attribute selection
* Object-Oriented Design
* Class-based alternative constructors using `@classmethod`
* Type hinting using `Self` and `TypedDict`
* Menu-driven interface

## Concepts Used

* Classes and Objects
* Object-Oriented Programming (OOP)
* Constructors (`__init__`)
* Instance Methods
* Class Methods (`@classmethod`)
* Encapsulation
* Lists
* List Comprehensions
* Tuples
* Dictionaries
* Nested Data Structures
* Strings
* File Handling
* Markdown File Storage
* Object Serialization and Deserialization
* Type Hinting
* `Self` Type
* `TypedDict`
* Type Aliases
* Constants
* Loops
* Conditional Statements
* `match` / `case`
* User Input Handling
* Input Validation
* Exception Handling
* `try` / `except` / `finally`
* Regular Expressions
* Lambda Functions
* Custom Sorting Keys
* `enumerate()`
* Modulus Operator
* `datetime`
* `timedelta`
* Calendar Calculations
* ANSI Escape Sequences
* Terminal Input Handling
* `os`
* `sys`
* `tty`
* `termios`
* `msvcrt`

## Run

Run the program using:

```bash
python3 main.py
```

The program starts the Task Scheduler interface and continuously accepts menu selections until the user chooses to quit.

## Task Record Format

Tasks are stored in a Markdown file using YAML-style task blocks.

```text
---
task_id: 1
name: Complete Python Project
priority: 8
duration: 120
status: Pending
category: Programming
due_date: 2026-08-30
recurrence: None
---
```

The duration is stored as total minutes, while the application converts it back into a `timedelta` when loading the task. Dates are stored using the `YYYY-MM-DD` format.

## Task Attributes

Each task contains:

| Attribute    | Description                                   |
| ------------ | --------------------------------------------- |
| `task_id`    | Automatically assigned unique task identifier |
| `name`       | Name of the task                              |
| `priority`   | Priority from 1 to 10                         |
| `duration`   | Expected task duration                        |
| `status`     | Current task state                            |
| `category`   | Task category                                 |
| `due_date`   | Task due date                                 |
| `recurrence` | Recurrence interval                           |

New tasks initially receive the `Pending` status.

## Task Status

Tasks move through different states during their lifecycle:

```text
Pending
   ↓
Running
   ↓
Completed
```

A task can also be returned to its previous state using the undo functionality.

### Pending

A newly created task starts as `Pending`.

### Running

When a task is executed, its status changes to `Running`.

### Completed

When a running task is marked as completed, its status changes to `Completed`.

For recurring tasks, completing the current task also creates the next occurrence with a new task ID and an advanced due date.

## Menu Options

| Option              | Description                                  |
| ------------------- | -------------------------------------------- |
| Add Task            | Create a new task                            |
| Execute Task        | Execute a pending task according to priority |
| View Tasks          | Display all scheduled tasks                  |
| Search Tasks        | Search tasks by name                         |
| Mark Task Completed | Complete a running task                      |
| Remove Task         | Delete a task                                |
| View Statistics     | Display task statistics                      |
| Save Tasks          | Save current tasks to storage                |
| Quit                | Save tasks and exit                          |

The main interface continuously processes these selections until the application is terminated.

## Interactive Terminal Interface

The application does not rely exclusively on traditional numbered input menus.

Instead, it provides keyboard-driven menus using:

* `↑` / `↓` navigation
* `←` / `→` navigation
* `ENTER` selection
* Highlighted menu options
* Toggleable selections
* Colored terminal output

The application detects the operating system and uses different low-level keyboard input mechanisms.

### Windows

Windows uses the `msvcrt` module to capture individual keypresses.

### Linux / macOS

POSIX systems use `tty` and `termios` to temporarily switch the terminal into raw input mode and read individual keypresses.

Terminal settings are restored afterward using `finally`, helping prevent the terminal from remaining in raw mode after the operation finishes.

## Task Creation

When adding a task, the application requests:

```text
Task Name
Task Priority
Task Duration
Task Category
Task Due Date
Task Recurrence
```

### Priority

Task priority must be a value from:

```text
1 - 10
```

Invalid values or non-numeric input are rejected.

### Duration

Duration is entered using:

```text
HH:MM
```

Example:

```text
02:30
```

represents:

```text
2 hours 30 minutes
```

The minutes component must remain between `0` and `59`.

### Due Date

Due dates use:

```text
YYYY-MM-DD
```

Example:

```text
2026-08-30
```

### Recurrence

Tasks can be configured with:

```text
None
Daily
Weekly
Monthly
```

The recurrence selection is performed through an interactive menu.

## Task Execution

The scheduler can automatically select the highest-priority pending task.

When using **Execute Highest Priority**, pending tasks are ordered using:

1. Priority
2. Due date
3. Duration
4. Task ID

Priority is sorted in descending order, while the remaining attributes act as tie-breakers.

Conceptually:

```text
Higher Priority
      ↓
Earlier Due Date
      ↓
Shorter Duration
      ↓
Lower Task ID
```

The first task after this ordering is marked as `Running`.

## Custom Priority Selection

The scheduler also allows the user to manually choose which attributes should determine task execution order.

Available attributes are:

```text
Priority
Due Date
Duration
Task ID
```

Multiple attributes can be toggled and selected.

For example:

```text
Priority
Due Date
Task ID
```

creates a custom sorting key using those attributes in the selected order.

This uses a dynamically constructed sorting key rather than a fixed priority rule.

## Task Search

Tasks can be searched by name.

The search accepts a task-name prefix, allowing multiple matching tasks to be displayed.

Example:

```text
Search: Python
```

can return tasks whose names begin with:

```text
Python ...
```

Search results display the matching task details and the total number of matches.

## Task Removal

Tasks can be removed by entering their name.

When a matching task is found, the corresponding task object is removed from the scheduler's task list.

If no matching task exists, the application displays an appropriate message.

## Task Filtering

The scheduler provides attribute-based filtering from the **View Tasks** interface.

Available filters include:

* Priority
* Status
* Due Date
* Duration
* Category
* Recurrence

The filter system allows comparison-based filtering where appropriate.

### Priority Filtering

Priority can be filtered using:

```text
Greater Than ( > )
Lesser Than ( < )
Equals ( = )
```

Example:

```text
Priority > 7
```

### Due-Date Filtering

Due dates can be compared using:

```text
Due After ( > )
Due Before ( < )
Due On ( = )
```

### Duration Filtering

Durations can similarly be compared using:

```text
Greater Than ( > )
Lesser Than ( < )
Equals ( = )
```

Status, category, and recurrence filters perform direct matching.

## Recurring Tasks

The scheduler supports recurring tasks with three recurrence intervals:

```text
Daily
Weekly
Monthly
```

When a recurring task is completed, the application creates a new task representing its next occurrence.

### Daily

The due date advances by:

```text
1 day
```

### Weekly

The due date advances by:

```text
1 week
```

### Monthly

The application uses a dedicated `add_month()` function to advance the date by one month while handling different month lengths and year rollover.

For example, the function prevents invalid dates when moving from a longer month into a shorter month.

## Undo Functionality

After executing or completing a task, the application provides an option to undo the most recent action.

### Undo Execution

A running task can be returned to:

```text
Pending
```

### Undo Completion

A completed task can be returned to:

```text
Running
```

For recurring tasks, undoing completion also removes the newly created recurring instance.

## Task Statistics

The scheduler provides statistical information about the current task collection.

The statistics include:

* Total Tasks
* Pending Tasks
* Running Tasks
* Completed Tasks
* Overdue Tasks
* Highest Priority
* Average Duration

Example:

```text
======= Task Statistics =======

Total Tasks:        8
Pending Tasks:      4
Running Tasks:      1
Completed Tasks:    3
Overdue Tasks:      2
Highest Priority:   10
Avg Duration:       74.5 mins
```

The average duration is calculated in minutes and displayed to one decimal place.

## Statistics Report Export

Statistics can be exported into a separate Markdown report.

The generated report contains:

```text
# Tasks Report
```

followed by the calculated task statistics.

The report is stored at:

```text
file-manager/markdown-files/report.md
```

## File Structure

```text
file-manager/
└── markdown-files/
    ├── tasks.md
    └── report.md
```

### `tasks.md`

Stores the persistent task records.

### `report.md`

Stores exported task statistics.

The task storage location is configured through the `FileManager` used by the scheduler.

## Data Persistence

Task data is stored in a Markdown file rather than a database.

When the scheduler starts, it loads existing task records from:

```text
file-manager/markdown-files/tasks.md
```

When the user chooses to save or quit, the current task list is written back to the file.

## Data Recovery

The application attempts to recover valid task records when the storage file contains malformed or incomplete data.

Each Markdown task block is parsed into a dictionary and passed to the `Task.get_details()` class method.

If a task contains invalid or missing data resulting in:

```text
KeyError
ValueError
TypeError
```

the corrupted task is skipped instead of terminating the entire application.

The loader also contains an EOF safety check that attempts to process a final task block even if its closing `---` delimiter is missing.

### Example

A partially corrupted file:

```text
---
task_id: 1
name: Study Python
priority: 8
duration: 60
status: Pending
category: Programming
due_date: 2026-08-30
recurrence: None
---

INVALID DATA

---
task_id: 2
name: Complete Assignment
priority: INVALID
duration: 90
---
```

can still preserve the valid task record while ignoring the malformed one.

## Object-Oriented Design

### Task Class

The `Task` class represents an individual scheduled task.

It stores:

* Task ID
* Name
* Priority
* Duration
* Status
* Category
* Due Date
* Recurrence

Methods include:

* `task_status()`
* `display_task()`
* `get_details()`

The `get_details()` method is a class method that acts as an alternative constructor, converting stored string data back into the appropriate Python types such as `int`, `timedelta`, and `datetime`.

### FileManager Class

The `FileManager` class handles persistent storage.

Responsibilities include:

* Loading tasks
* Parsing Markdown task blocks
* Recovering valid records
* Saving tasks
* Exporting statistics reports

Methods include:

* `load_tasks()`
* `save_tasks()`
* `export_report()`

### Scheduler Class

The `Scheduler` class manages the main application logic.

Responsibilities include:

* Loading tasks
* Adding tasks
* Executing tasks
* Searching tasks
* Removing tasks
* Filtering tasks
* Viewing tasks
* Completing tasks
* Calculating statistics
* Saving task data
* Managing the main interface

Methods include:

* `add_task()`
* `execute_task()`
* `modify_task()`
* `filter_tasks()`
* `view_tasks()`
* `view_stats()`
* `finish_task()`
* `scheduler_interface()`

### Style Class

The `Style` class contains ANSI escape sequences used for terminal presentation.

It provides:

* Text formatting
* Bright foreground colors
* Background colors
* Automatic style resetting

The `apply()` class method allows multiple styles to be combined when formatting terminal output.

## Utility Functions

### `clear_screen()`

Clears the terminal screen and scrollback buffer using ANSI escape sequences.

### `clear_last_line()`

Removes previously displayed terminal lines to allow the interactive button interface to update without redrawing the entire screen.

### `add_month()`

Advances a `datetime` object by one month while handling:

* Month rollover
* Year rollover
* Different month lengths
* Leap years

### `interactive_menu()`

Provides vertical arrow-key navigation for menu selections.

### `buttons()`

Provides horizontal navigation and supports both normal button selection and multi-selection toggle interfaces.

## Example Task Lifecycle

```text
Add Task
    ↓
Pending
    ↓
Execute Task
    ↓
Running
    ↓
Mark Task Completed
    ↓
Completed
```

For a recurring task:

```text
Add Recurring Task
        ↓
     Pending
        ↓
     Execute
        ↓
     Running
        ↓
    Complete
        ↓
 Completed + Create Next Occurrence
        ↓
     New Pending Task
```

The scheduler therefore combines task management with a basic recurring-task workflow.

## Program Architecture

The overall application can be viewed as four main layers:

```text
┌─────────────────────────────┐
│     Terminal Interface      │
│ interactive_menu / buttons  │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│          Scheduler          │
│   Application Logic         │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│            Task             │
│   Task Data + Behaviour     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│        FileManager          │
│ Markdown Persistence        │
└─────────────────────────────┘
```

This separates task representation, application logic, terminal interaction, and persistent storage into distinct components.

## Example Workflow

```text
Launch Application
        ↓
Load Existing Tasks
        ↓
Open Scheduler Menu
        ↓
Add / Execute / Search / Filter Tasks
        ↓
Update Task Status
        ↓
Generate Statistics
        ↓
Optionally Export Report
        ↓
Save Tasks
        ↓
Quit Application
```

This project demonstrates practical use of **Object-Oriented Programming, file persistence, terminal interfaces, keyboard input handling, date and time manipulation, sorting, filtering, task prioritization, recurring events, exception handling, and data recovery** within a real-world command-line task management workflow.
