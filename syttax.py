import sys
import re

VERSION = "0.1.0"

variables = {}


class SyttaxError(Exception):
    pass


def evaluate(expression):
    expression = expression.strip()

    # Strings
    if (
        expression.startswith('"')
        and expression.endswith('"')
    ):
        return expression[1:-1]

    if (
        expression.startswith("'")
        and expression.endswith("'")
    ):
        return expression[1:-1]

    # Integers
    if re.fullmatch(r"-?\d+", expression):
        return int(expression)

    # Decimals
    if re.fullmatch(r"-?\d+\.\d+", expression):
        return float(expression)

    # Variables
    if expression in variables:
        return variables[expression]

    # Basic calculations
    parts = expression.split()

    if len(parts) == 3:
        left = evaluate(parts[0])
        operator = parts[1]
        right = evaluate(parts[2])

        if operator == "+":
            return left + right

        if operator == "-":
            return left - right

        if operator == "*":
            return left * right

        if operator == "/":
            if right == 0:
                raise SyttaxError("Cannot divide by zero")

            return left / right

    raise SyttaxError(
        f"Cannot understand expression: {expression}"
    )


def execute(line):
    line = line.strip()

    # Empty line
    if not line:
        return

    # Comment
    if line.startswith("#"):
        return

    # SAY
    if line.startswith("say "):
        expression = line[4:]
        print(evaluate(expression))
        return

    # SET
    if line.startswith("set "):
        statement = line[4:]

        if "=" not in statement:
            raise SyttaxError(
                "Expected '=' in variable declaration"
            )

        name, value = statement.split("=", 1)

        name = name.strip()
        value = value.strip()

        if not name.isidentifier():
            raise SyttaxError(
                f"Invalid variable name: {name}"
            )

        variables[name] = evaluate(value)
        return

    # ASK
    if line.startswith("ask "):
        statement = line[4:]

        if "=" not in statement:
            raise SyttaxError(
                "ASK requires a variable"
            )

        name, question = statement.split("=", 1)

        name = name.strip()
        question = question.strip()

        message = evaluate(question)

        variables[name] = input(
            str(message) + " "
        )

        return

    raise SyttaxError(
        f"Unknown command: {line}"
    )


def run(filename):
    try:
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

    except FileNotFoundError:
        print(
            f"SyttaxError: '{filename}' was not found."
        )
        return

    for line_number, line in enumerate(
        lines,
        start=1
    ):

        try:
            execute(line)

        except SyttaxError as error:
            print(
                f"SyttaxError "
                f"[line {line_number}]: {error}"
            )
            return

        except Exception as error:
            print(
                f"SyttaxRuntimeError "
                f"[line {line_number}]: {error}"
            )
            return


def main():

    print(
        f"SyttaxScript v{VERSION}"
    )

    if len(sys.argv) < 2:

        print(
            "Usage: python syttax.py program.syx"
        )

        return

    filename = sys.argv[1]

    if not filename.endswith(".syx"):

        print(
            "SyttaxError: "
            "SyttaxScript files must use .syx"
        )

        return

    run(filename)


if __name__ == "__main__":
    main()
