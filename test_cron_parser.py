import unittest
from cron_parser import (
    _generate_padding,
    expand_expression,
    parse_expression,
    parse_raw_components,
    RawCronExpression,
    ExpandedCronExpression,
    TableOutput,
    expand_cron_expression,
    raw_cron_expression
)


class TestCronParser(unittest.TestCase):

    ## Tests for _generate_padding
    def test_generate_padding(self):
        self.assertEqual(_generate_padding("minute", 10), "minute    ")
        self.assertEqual(_generate_padding("hour", 8), "hour    ")

    def test_padding_with_special_characters(self):
        """Test padding with strings containing special characters."""
        self.assertEqual(_generate_padding("min@hour", 12), "min@hour    ")
    
    def test_padding_very_small_width(self):
        """Test padding where length is only 1 or 2."""
        self.assertEqual(_generate_padding("longword", 2), "longword")  # no truncation, only padding
        self.assertEqual(_generate_padding("a", 2), "a ")

    ## Minute validations
    def test_expand_minute_valid_range(self):
        """Test that a valid range order like '30-50' works."""
        result = expand_expression("minute", "30-50", list(range(60)), 0, 59)
        self.assertEqual(result, list(range(30, 51)))
    
    def test_expand_minute_invalid_range(self):
        """Test that an invalid range order like '20-10' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("minute", "20-10", list(range(60)), 0, 59)

    def test_expand_minute_valid_value(self):
        """Test that a valid value like '30' works."""
        result = expand_expression("minute", "30", list(range(60)), 0, 59)
        self.assertEqual(result, [30])

    def test_expand_minute_invalid_high_value(self):
        """Test that an invalid value like '60' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("minute", "60", list(range(60)), 0, 59)

    def test_expand_minute_invalid_negative_value(self):
        """Test that an invalid negative value like '-1' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("minute", "-1", list(range(60)), 0, 59)

    def test_expand_minute_step_valid(self):
        """Test that an invalid step value like '*/15"' works."""
        result = expand_expression("minute", "*/15", list(range(60)), 0, 59)
        self.assertEqual(result, [0, 15, 30, 45])

    def test_expand_minute_step_invalid(self):
        """Test that an invalid step value like '*/100"' raises an error.."""
        with self.assertRaises(ValueError):
            expand_expression("minute", "*/100", list(range(60)), 0, 59)

    def test_expand_minute_valid_comma_format(self):
        """Test that a valid comma-separated format like '33,34,35' works."""
        result = expand_expression("minute", "33,34,35", list(range(60)), 0, 59)
        self.assertEqual(result, [33, 34, 35])

    def test_expand_minute_invalid_comma_format(self):
        """Test that an invalid comma-separated format like '1,,2' raises error."""
        with self.assertRaises(ValueError):
            expand_expression("minute", "1,,2", list(range(60)), 0, 59)    

    ## Hour validations
    def test_expand_hour_valid(self):
        """Test that a valid range like '4-23' works."""
        result = expand_expression("hour", "4-23", list(range(24)), 0, 23)
        self.assertEqual(result, list(range(4, 24)))

    def test_expand_hour_invalid_range(self):
        """Test that an invalid range order like '23-45' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("hour", "23-45", list(range(24)), 0, 23)

    def test_expand_hour_valid_value(self):
        """Test that a valid value like '12' works."""
        result = expand_expression("hour", "12", list(range(22)), 0, 23)
        self.assertEqual(result, [12])

    def test_expand_hour_invalid_high_value(self):
        """Test that an invalid value like '24' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("hour", "24", list(range(24)), 0, 23)

    def test_expand_hour_invalid_negative_value(self):
        """Test that an invalid negative value like '-1' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("hour", "-1", list(range(24)), 0, 23)

    def test_expand_hour_step_valid(self):
        """Test that an invalid step value like '*/6"' works."""
        result = expand_expression("hour", "*/6", list(range(24)), 0, 23)
        self.assertEqual(result, [0, 6, 12, 18])

    def test_expand_hour_step_invalid(self):
        """Test that an invalid step value like '*/25"' raises an error.."""
        with self.assertRaises(ValueError):
            expand_expression("hour", "*/25", list(range(24)), 0, 23)

    def test_expand_hour_valid_comma_format(self):
        """Test that a valid comma-separated format like '4,5' works."""
        result = expand_expression("hour", "4,5", list(range(24)), 0, 23)
        self.assertEqual(result, [4, 5]);  

    def test_expand_hour_invalid_comma_format(self):
        """Test that an invalid comma-separated format like '12,,13' raises error."""
        with self.assertRaises(ValueError):
            expand_expression("hour", "12,,13", list(range(24)), 0, 23)    

    ## Day of Month validations
    def test_expand_dom_valid(self):
        """Test that a valid range like '1-31' works."""
        result = expand_expression("day of month", "1-31", list(range(1, 32)), 1, 31)
        self.assertEqual(result, list(range(1, 32)))

    def test_expand_dom_invalid_range(self):
        """Test that an invalid range order like '33-45' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("day of month", "33-45", list(range(1, 32)), 1, 31)

    def test_expand_dom_valid_value(self):
        """Test that a valid value like '12' works."""
        result = expand_expression("dom", "12", list(range(1, 32)), 1, 31)
        self.assertEqual(result, [12])

    def test_expand_dom_invalid_high_value(self):
        """Test that an invalid value like '32' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("day of month", "32", list(range(1, 32)), 1, 31)

    def test_expand_dom_invalid_negative_value(self):
        """Test that an invalid negative value like '0' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("day of month", "0", list(range(1, 32)), 1, 31)   

    def test_expand_dom_step_valid(self):
        """Test that an invalid step value like '*/10"' works."""
        result = expand_expression("day of month", "*/10", list(range(1, 32)), 1, 31)
        self.assertEqual(result, [1, 11, 21, 31])

    def test_expand_dom_step_invalid(self):
        """Test that an invalid step value like '*/32"' raises an error.."""
        with self.assertRaises(ValueError):
            expand_expression("day of month", "*/32", list(range(1, 32)), 1, 31)
    
    def test_expand_dom_valid_comma_format(self):
        """Test that a valid comma-separated format like '4,5' works."""
        result = expand_expression("day of month", "4,5", list(range(1, 32)), 1, 31)
        self.assertEqual(result, [4, 5])

    def test_expand_dom_invalid_comma_format(self):
        """Test that an invalid comma-separated format like '12,,13' raises error."""
        with self.assertRaises(ValueError):
            expand_expression("day of month", "12,,13", list(range(1, 32)), 1, 31)    


    ## Month validations
    def test_expand_month_valid(self):
        """Test that a valid range like '1-12' works."""
        result = expand_expression("month", "1-12", list(range(1, 13)), 1, 12)
        self.assertEqual(result, list(range(1, 13)))

    def test_expand_month_invalid_range(self):
        """Test that an invalid range order like '33-45' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("month", "33-45", list(range(1, 13)), 1, 12)

    def test_expand_month_valid_value(self):
        """Test that a valid value like '10' works."""
        result = expand_expression("month", "10", list(range(1, 13)), 1, 12)
        self.assertEqual(result, [10])

    def test_expand_month_invalid_high_value(self):
        """Test that an invalid value like '13' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("month", "13", list(range(1, 13)), 1, 12)

    def test_expand_month_invalid_negative_value(self):
        """Test that an invalid negative value like '0' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("month", "0", list(range(1, 13)), 1, 12)   

    def test_expand_month_step_valid(self):
        """Test that an invalid step value like '*/2"' works."""
        result = expand_expression("month", "*/2", list(range(1, 13)), 1, 12)
        self.assertEqual(result, [1, 3, 5, 7, 9, 11])

    def test_expand_month_step_invalid(self):
        """Test that an invalid step value like '*/13"' raises an error.."""
        with self.assertRaises(ValueError):
            expand_expression("month", "*/13", list(range(1, 13)), 1, 12)
    
    def test_expand_month_valid_comma_format(self):
        """Test that a valid comma-separated format like '4,5' works."""
        result = expand_expression("month", "4,5", list(range(1, 13)), 1, 12)
        self.assertEqual(result, [4, 5]) 

    def test_expand_month_invalid_comma_format(self):
        """Test that an invalid comma-separated format like '9,,10' raises error."""
        with self.assertRaises(ValueError):
            expand_expression("month", "9,,10", list(range(1, 13)), 1, 12)    



    ## Day of Week validations

    def test_expand_dow_valid(self):
        """Test that a valid range like '0-6' works."""
        result = expand_expression("day of week", "0-6", list(range(7)), 0, 6)
        self.assertEqual(result, list(range(7)))

    def test_expand_dow_invalid_range(self):
        """Test that an invalid range order like '7-10' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("day of week", "7-10", list(range(7)), 0, 6)

    def test_expand_dow_valid_value(self):
        """Test that a valid value like '5' works."""
        result = expand_expression("day of week", "5", list(range(7)), 1, 12)
        self.assertEqual(result, [5])

    def test_expand_dow_invalid_high_value(self):
        """Test that an invalid value like '7' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("day of week", "7", list(range(7)), 0, 6)

    def test_expand_dow_invalid_negative_value(self):
        """Test that an invalid negative value like '-1' raises an error."""
        with self.assertRaises(ValueError):
            expand_expression("day of week", "-1", list(range(7)), 0, 6)   

    def test_expand_dow_step_valid(self):
        """Test that an invalid step value like '*/2"' works."""
        result = expand_expression("day of week", "*/2", list(range(7)), 0, 6)
        self.assertEqual(result, [0, 2, 4, 6])

    def test_expand_dow_step_invalid(self):
        """Test that an invalid step value like '*/8"' raises an error.."""
        with self.assertRaises(ValueError):
            expand_expression("day of week", "*/8", list(range(7)), 0, 6)
    
    def test_expand_dow_valid_comma_format(self):
        """Test that a valid comma-separated format like '4,5' works."""
        result = expand_expression("day of week", "4,5", list(range(7)), 0, 6)
        self.assertEqual(result, [4,5])  

    def test_expand_dow_invalid_comma_format(self):
        """Test that an invalid comma-separated format like '4,,5' raises error."""
        with self.assertRaises(ValueError):
            expand_expression("day of week", "4,,5", list(range(7)), 0, 6)    

    # Tests for parse_expression
    def test_parse_expression_valid(self):
        """Test parsing a valid cron expression."""
        result = parse_expression("*/5 0 1,15 * 1 /my/command")
        self.assertEqual(result, ["*/5", "0", "1,15", "*", "1", "/my/command"])

    def test_parse_expression_invalid_length(self):
        """Test parsing an invalid cron expression with wrong field count."""
        with self.assertRaises(ValueError):
            parse_expression("*/5 0 1,15 * /my/command")  # Only 5 fields instead of 6

    # Tests for parse_raw_components
    def test_parse_raw_components(self):
        """Test parsing raw components of a cron expression."""
        result = parse_raw_components("*/10 2 * * * /my/command")
        self.assertEqual(result, ("*/10", "2", "*", "*", "*"))

        # Tests for TableOutput
    def test_table_output_empty_data(self):
        """Test rendering an empty table."""
        table_output = TableOutput([])
        self.assertEqual(table_output.render(), "")

    def test_table_output_custom_column_length(self):
        """Test rendering with custom column lengths."""
        data = [("field1", "value1"), ("field2", "value2")]
        table_output = TableOutput(data, name_col_length=5)
        expected_output = (
            "field1 value1\n"
            "field2 value2"
        )
        self.assertEqual(table_output.render(), expected_output)

    def test_table_output_list_values(self):
        """Test table output with list values in fields."""
        data = [("minute", [0, 15, 30, 45]), ("hour", [0])]
        table_output = TableOutput(data)
        expected_output = "minute         0 15 30 45\nhour           0"
        self.assertEqual(table_output.render(), expected_output)



    ## Integration Tests for complete cron expressions

    # Integration Tests for RawCronExpression
    def test_raw_cron_expression_valid(self):
        """Test the raw cron expression output with a valid input."""
        raw_cron = RawCronExpression("*/10 2 * * * /my_custom/command")
        output = raw_cron.to_table_format()
        expected_output = [
            ("minute", "*/10"),
            ("hour", "2"),
            ("day of month", "*"),
            ("month", "*"),
            ("day of week", "*"),
            ("command", "/my_custom/command")
        ]
        self.assertEqual(output, expected_output)

    # Integration Tests for ExpandedCronExpression
    def test_expand_cron_expression_simple(self):
        """Test a simple expanded cron expression."""
        cron_expr = "*/15 0 1,15 * 1 /my_command.sh"
        expanded_cron = expand_cron_expression(cron_expr)
        expected_output = (
            "minute         0 15 30 45\n"
            "hour           0\n"
            "day of month   1 15\n"
            "month          1 2 3 4 5 6 7 8 9 10 11 12\n"
            "day of week    1\n"
            "command        /my_command.sh"
        )
        self.assertEqual(expanded_cron, expected_output)

    def test_expand_cron_expression_complex(self):
        """Test complex combination of ranges, steps, and commas in expand_cron_expression."""
        cron_expr = "1-5,15/3 0,12 1-10,15 5,6 0-3 /my_command.sh"
        expanded_cron = expand_cron_expression(cron_expr)
        expected_output = (
            "minute         1 2 3 4 5 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57\n"
            "hour           0 12\n"
            "day of month   1 2 3 4 5 6 7 8 9 10 15\n"
            "month          5 6\n"
            "day of week    0 1 2 3\n"
            "command        /my_command.sh"
        )
        self.assertEqual(expanded_cron, expected_output)

    def test_expand_cron_expression_second_complex(self):
        """Test complex combination of ranges, steps, and commas in expand_cron_expression."""
        cron_expr = "15/3,20-23,30,40,51-53 0 1,15 * 1-6 /my_command.sh"
        expanded_cron = expand_cron_expression(cron_expr)
        expected_output = (
            "minute         15 18 20 21 22 23 24 27 30 33 36 39 40 42 45 48 51 52 53 54 57\n"
            "hour           0\n"
            "day of month   1 15\n"
            "month          1 2 3 4 5 6 7 8 9 10 11 12\n"
            "day of week    1 2 3 4 5 6\n"
            "command        /my_command.sh"
        )
        self.assertEqual(expanded_cron, expected_output)

    def test_expand_cron_expression_invalid_field(self):
        """Test expanded cron expression with an invalid field."""
        with self.assertRaises(ValueError):
            expand_cron_expression("*/5 * 32 * * /bin/command")  # Day of month > 31


    def test_expand_cron_expression_full_valid(self):
        cron_expr = "*/10 0 1-15 1-6 0,3,6 /mycommand.sh"
        output = expand_cron_expression(cron_expr)
        expected_output = (
            "minute         0 10 20 30 40 50\n"
            "hour           0\n"
            "day of month   1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n"
            "month          1 2 3 4 5 6\n"
            "day of week    0 3 6\n"
            "command        /mycommand.sh"
        )
        self.assertEqual(output, expected_output)

    # Integration Test for invalid minute
    def test_expand_cron_expression_invalid_minute(self):
        cron_expr = "*/61 0 1-15 1-6 0,3,6 /mycommand.sh"
        with self.assertRaises(ValueError):
            expand_cron_expression(cron_expr)

    # Integration Test for invalid hour
    def test_expand_cron_expression_invalid_hour(self):
        cron_expr = "*/10 24 1-15 1-6 0,3,6 /mycommand.sh"
        with self.assertRaises(ValueError):
            expand_cron_expression(cron_expr)

    # Integration Test for invalid day of month
    def test_expand_cron_expression_invalid_dom(self):
        cron_expr = "*/10 0 32 1-6 0,3,6 /mycommand.sh"
        with self.assertRaises(ValueError):
            expand_cron_expression(cron_expr)

    # Integration Test for invalid month
    def test_expand_cron_expression_invalid_month(self):
        cron_expr = "*/10 0 1-15 13 0,3,6 /mycommand.sh"
        with self.assertRaises(ValueError):
            expand_cron_expression(cron_expr)

    # Integration Test for invalid day of week
    def test_expand_cron_expression_invalid_dow(self):
        cron_expr = "*/10 0 1-15 1-6 7 /mycommand.sh"
        with self.assertRaises(ValueError):
            expand_cron_expression(cron_expr)

    # Integration Test for too few fields in expression
    def test_invalid_cron_expression_too_few_fields(self):
        """Test cron expression with too few fields, expecting ValueError."""
        with self.assertRaises(ValueError):
            expand_cron_expression("*/15 0 * /command")

    # Integration Test for missing command 
    def test_invalid_cron_expression_command(self):
        """Test cron expression with invalid command field raises ValueError."""
        with self.assertRaises(ValueError):
            expand_cron_expression("*/10 2 15 * *")  # Command is missing
if __name__ == '__main__':
    unittest.main()

