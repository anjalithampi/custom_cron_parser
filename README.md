# Cron Parser

This is a Python command-line application that parses a standard cron expression and outputs an expanded, human-readable schedule. It shows the exact minute, hour, day of the month, month, and day of the week on which the cron job will run.

## Prerequisites

- Python 3.8 or higher
- A Linux/OSX environment (command line)

## Features

- Expands cron expressions with minute, hour, day of month, month, day of week, and the command to be executed.
- Supports common cron syntax like `*`, `,`, `-`, and `/` for range, list, and step values.
- Outputs the result in a clean, tabular format.

## Installation and Setup

Clone the repository:
   ```bash
   git clone git@github.com:anjalithampi/cron_parser.git
   cd cron_parser

## Example Usage

# For expanded expression
`python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find expanded"`

[OR]

# For raw expression
`python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find raw"`

## Example Output

minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find

## Running Tests

Ensure you are in the project directory.
Run tests:

`python3 test_cron_parser.py`

This will execute all unit and integration tests in test_cron_parser.py.
