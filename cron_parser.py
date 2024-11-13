import re
import sys
from typing import List, Tuple, Union

## HELPER FUNCTIONS
# Helper function to generate padded columns for table output
def _generate_padding(name: str, length: int) -> str:
    """Ensure that the field name is properly padded with spaces to the desired length."""
    return name + " " * (length - len(name))
    

## PUBLIC FUNCTIONS
# Public function to expand cron components (minute, hour, etc.)
def expand_expression(component: str, expression: str, options: Union[List[int], List[str]], min_val: str, max_val: str) -> Union[List[int], List[str]]:
    """Expand a cron schedule expression component."""
    
    """ Handle "*" for any value """
    if expression == "*":
        return options

    """ Handle dash for ranges, e.g. "1-5" """
    cron_match = re.match(r"^(\d+)-(\d+)$", expression)
    if cron_match:
        start = int(cron_match.group(1))
        end = int(cron_match.group(2))
        # Validation : Both start and end should fall within allowed range
        if min_val <= start <= max_val and min_val <= end <= max_val and start <= end:
            return list(range(start, end + 1))
        raise ValueError(f"Invalid range for '{component}': {expression}") # Handle error

    """ Handle comma-separated values, e.g. "1,2,3" """
    comma_match = re.match(r"^\d+(?:,\d+)*$", expression)
    if comma_match:
        values = list(map(int, expression.split(',')))
        # Each value should fall within allowed range
        if all(min_val <= value <= max_val for value in values):
            return list(map(int, expression.split(',')))
        raise ValueError(f"Invalid range for comma separated values for '{component}': {expression}") # Handle error

    """ Handle step values, e.g. "*/5" """
    step_match = re.match(r"^(\d+|\*)/(\d+)$", expression)
    if step_match:
        base = step_match.group(1)
        step = int(step_match.group(2))
        if min_val <= step <= max_val:
            # Handle base range with step value
            if base == "*":
                base = options
            else:
                base = options[int(base):]  # Slice options if base is a number
            return base[::step]
        raise ValueError(f"Invalid step values for '{component}': {expression}") # Handle error
    
    
    """Check for comma-separated cron-like expression like '15,20-23,30,40,51-53'. """
    cron_match = re.match(r"^(\d+|\d+-\d+|\*|\d+/\d+)(?:,(\d+|\d+-\d+|\*|\d+/\d+))*$", expression)
    if bool(cron_match):
        expanded_part = []
        parts = expression.split(',')
        for part in parts:
           """ Handle dash for ranges, e.g. "1-5" """
           cron_match = re.match(r"^(\d+)-(\d+)$", part)
           if cron_match:
                start = int(cron_match.group(1))
                end = int(cron_match.group(2))
                if not (min_val <= start <= max_val and min_val <= end <= max_val and start <= end):
                    raise ValueError(f"Invalid range for '{component}: {part}") # Handle error
                expanded_part.extend(list(range(start, end + 1)))
                continue

           """ Handle comma-separated values, e.g. "1,2,3" """
           comma_match = re.match(r"^\d+(?:,\d+)*$", part)
           if comma_match:
                values = list(map(int, part.split(',')))
                # Each value should fall within allowed range
                if not (all(min_val <= value <= max_val for value in values)):
                    if len(values) == 1:
                       raise ValueError(f"Invalid value for '{component}: {part}") # Handle error 
                    raise ValueError(f"Invalid range for comma separated values for '{component}: {part}") # Handle error
                expanded_part.extend(values)
                continue

           """ Handle step values, e.g. "*/5" """
           step_match = re.match(r"^(\d+|\*)/(\d+)$", part)
           if step_match:
                base = step_match.group(1)
                step = int(step_match.group(2))
                if not (min_val <= step <= max_val):
                    raise ValueError(f"Invalid step values for '{component}: {part}") # Handle error
                # Handle base range with step value
                if base == "*":
                    base = options
                else:
                    base = options[int(base):]  # Slice options if base is a number

                expanded_part.extend(base[::step])
        return sorted(set(expanded_part))
    """ If none of the above matched, raise an error """
    raise ValueError(f"Invalid cron expression for '{component}: {expression}")

 # Public function to parse base expression
def parse_expression(cron_expression: str) -> List[any]:
        expressions = cron_expression.split()
        """ Return if the arguments are less than 6 """
        if len(expressions) != 6:
            raise ValueError("Cron expression must contain exactly 5 time fields and 1 command field") # Handle error
        return expressions

# Public function to parse the cron expression into its components
def parse_raw_components(cron_expression: str) -> Tuple[str, str, str, str, str]:
        parts = parse_expression(cron_expression)
        return parts[0], parts[1], parts[2], parts[3], parts[4]



## CLASSES
# Abstract base class for cron expressions
class BaseCronExpression:
    def __init__(self, cron_expression: str):
        self.cron_expression = cron_expression
        self.raw_expression = parse_expression(cron_expression)
        self.command = self.raw_expression[5] 


    def to_table_format(self, values: dict) -> List[Tuple[str, Union[str, List[int]]]]:
        """Return the cron expression in a table format, reusing the same method for both raw and expanded."""
        return [
            ("minute", values.get('minute')),
            ("hour", values.get('hour')),
            ("day of month", values.get('dom')),
            ("month", values.get('month')),
            ("day of week", values.get('dow')),
            ("command", self.command),
        ]


# Class for raw cron expression (returns raw values)
class RawCronExpression(BaseCronExpression):
    def __init__(self, cron_expression: str):
        super().__init__(cron_expression)
        self.minute, self.hour, self.dom, self.month, self.dow = parse_raw_components(cron_expression)

    def to_table_format(self) -> List[Tuple[str, Union[str, List[int]]]]:
        """Return the raw cron expression in a table format."""
        raw_values = {
            'minute': self.minute,
            'hour': self.hour,
            'dom': self.dom,
            'month': self.month,
            'dow': self.dow,
        }
        return super().to_table_format(raw_values)


# Class to handle expanding the cron expression (expanded values)
class ExpandedCronExpression(BaseCronExpression):
    def __init__(self, cron_expression: str):
        super().__init__(cron_expression)
        self.minute, self.hour, self.dom, self.month, self.dow = parse_raw_components(cron_expression)
        self.expanded_minute = self.expand_component('minute(s)', self.minute, list(range(60)), 0, 59) # # Validate minute (0-59)
        self.expanded_hour = self.expand_component('hour(s)', self.hour, list(range(24)), 0, 23) # Validate hour (0-23)
        self.expanded_dom = self.expand_component('day(s) of month', self.dom, list(range(1, 32)), 1, 31) # Validate day of month (1-31)
        self.expanded_month = self.expand_component('month(s)', self.month, list(range(1, 13)), 1, 12) # Validate month (1-12)
        self.expanded_dow = self.expand_component('day(s) of week', self.dow, list(range(0, 7)), 0, 6)  # Validate day of week (0-6, where 0 is Sunday)

    def expand_component(self, component: str, expression: str, options: Union[List[int], List[str]], min_val: str, max_val: str) -> Union[List[int], List[str]]:
        """Expand each field of the cron expression."""
        return expand_expression(component, expression, options, min_val, max_val)

    def to_table_format(self) -> List[Tuple[str, Union[str, List[int]]]]:
        """Return the expanded cron expression in a table format."""
        expanded_values = {
            'minute': self.expanded_minute,
            'hour': self.expanded_hour,
            'dom': self.expanded_dom,
            'month': self.expanded_month,
            'dow': self.expanded_dow,
        }
        return super().to_table_format(expanded_values)

# Class to handle table output rendering
class TableOutput:
    def __init__(self, table_data: List[Tuple[str, Union[str, List[int]]]], name_col_length: int = 14):
        self.table_data = table_data
        self.name_col_length = name_col_length

    def render(self) -> str:
        """Render the data as a formatted table."""
        out = ""
        for name, value in self.table_data:
            if isinstance(value, list):
                value = " ".join([str(x) for x in value])
            row = f"{_generate_padding(name, self.name_col_length)} {value}\n"
            out += row
        return out.rstrip()  # Remove trailing newline for exact output


## MAIN FUNCTIONS
# Main function to expand the cron expression
def expand_cron_expression(cron_expression: str) -> str:
    """Expand and return a formatted cron expression."""
    expanded = ExpandedCronExpression(cron_expression)
    return TableOutput(expanded.to_table_format()).render()


# Main function for raw cron expression rendering
def raw_cron_expression(cron_expression: str) -> str:
    raw = RawCronExpression(cron_expression)
    return TableOutput(raw.to_table_format()).render()



## COMMAND-LINE INTERFACE
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 cron_parser.py '<cron_expression>' 'expanded / raw'")
        sys.exit(1)

    cron_expr = sys.argv[1]
    parse_command = sys.argv[2]
    try:
        if not isinstance(parse_command, str):
            raise ValueError(f"Invalid parse command: {parse_command}")
        if parse_command.lower() == 'expanded':
            print(expand_cron_expression(cron_expr))
        elif parse_command.lower() == 'raw':
            print(raw_cron_expression(cron_expr))
        else:
            raise ValueError(f"Invalid parse command: {parse_command}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
