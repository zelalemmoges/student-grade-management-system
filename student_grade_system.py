
"""
Student Grade Management System

Author: Zelalem Moges

Accepts student marks, validates inputs, calculates average marks and
letter grades, and displays results.
"""

MIN_MARK = 0.0
MAX_MARK = 100.0

# (lower bound inclusive, letter grade) - checked from highest to lowest
GRADE_SCALE = [
    (90, "A+"),
    (85, "A"),
    (80, "A-"),
    (75, "B+"),
    (70, "B"),
    (65, "B-"),
    (60, "C+"),
    (50, "C"),
    (45, "D"),
    (0, "F"),
]


# ----------------------------------------------------------------
# Validation
# ----------------------------------------------------------------

def validate_name(name):
    """Return the cleaned name, or raise ValueError if invalid."""

    name = name.strip()

    if not name:
        raise ValueError("Name cannot be empty.")

    if not all(ch.isalpha() or ch in " .-'" for ch in name):
        raise ValueError(
            "Name may contain only letters, spaces, '.', '-' and apostrophes."
        )

    return name


def validate_mark(text):
    """Convert text to a float mark in [0, 100], or raise ValueError."""

    try:
        mark = float(str(text).strip())
    except ValueError:
        raise ValueError(f"'{text}' is not a number.")

    if mark != mark or mark in (float("inf"), float("-inf")):
        raise ValueError("Mark must be a finite number.")

    if not (MIN_MARK <= mark <= MAX_MARK):
        raise ValueError(
            f"Mark must be between {MIN_MARK:g} and {MAX_MARK:g}."
        )

    return mark


def validate_count(text, low=1, high=20):
    """Validate a whole-number count (e.g. number of subjects)."""

    try:
        n = int(str(text).strip())
    except ValueError:
        raise ValueError(f"'{text}' is not a whole number.")

    if not (low <= n <= high):
        raise ValueError(f"Value must be between {low} and {high}.")

    return n


# ----------------------------------------------------------------
# Calculation
# ----------------------------------------------------------------

def calculate_average(marks):
    """Average of a non-empty list of marks."""

    if not marks:
        raise ValueError("At least one mark is required.")

    return sum(marks) / len(marks)


def letter_grade(average):
    """Map an average mark to a letter grade."""

    if not (MIN_MARK <= average <= MAX_MARK):
        raise ValueError("Average out of range.")

    for lower, grade in GRADE_SCALE:
        if average >= lower:
            return grade

    return "F"


def make_record(name, subjects, marks):
    """Build one student's result record."""

    avg = calculate_average(marks)

    return {
        "name": name,
        "subjects": list(subjects),
        "marks": list(marks),
        "average": avg,
        "grade": letter_grade(avg),
    }


# ----------------------------------------------------------------
# Display
# ----------------------------------------------------------------

def format_results(records):
    """Return a printable results table (string)."""

    if not records:
        return "No students recorded."

    width = max(len("Name"), max(len(r["name"]) for r in records))

    line = "+" + "-" * (width + 2) + "+----------+-------+"

    out = [
        line,
        f"| {'Name'.ljust(width)} | Average  | Grade |",
        line
    ]

    for r in records:
        out.append(
            f"| {r['name'].ljust(width)} | "
            f"{r['average']:8.2f} | {r['grade']:^5} |"
        )

    out.append(line)

    avgs = [r["average"] for r in records]

    best = max(records, key=lambda r: r["average"])
    worst = min(records, key=lambda r: r["average"])

    out.append(
        f"Students: {len(records)}   "
        f"Class average: {sum(avgs) / len(avgs):.2f}"
    )

    out.append(
        f"Highest: {best['name']} ({best['average']:.2f})   "
        f"Lowest: {worst['name']} ({worst['average']:.2f})"
    )

    return "\n".join(out)


def format_detail(record):
    """Return a per-subject breakdown for one student."""

    lines = [f"Student: {record['name']}"]

    for s, m in zip(record["subjects"], record["marks"]):
        lines.append(f"  {s:<20} {m:6.2f}")

    lines.append(
        f"  Average: {record['average']:.2f}   "
        f"Grade: {record['grade']}"
    )

    return "\n".join(lines)


# ----------------------------------------------------------------
# User Interface
# ----------------------------------------------------------------

def prompt(message, validator):
    """Keep asking until validator accepts the input."""

    while True:
        try:
            return validator(input(message))
        except ValueError as err:
            print(f"  Invalid input: {err}")


def enter_student(records):

    name = prompt("Student name: ", validate_name)

    n = prompt("Number of subjects (1-20): ", validate_count)

    subjects, marks = [], []

    for i in range(1, n + 1):

        subject = (
            input(f"  Subject {i} name (Enter for 'Subject {i}'): ").strip()
            or f"Subject {i}"
        )

        mark = prompt(
            f"  Mark for {subject} (0-100): ",
            validate_mark
        )

        subjects.append(subject)
        marks.append(mark)

    record = make_record(name, subjects, marks)

    records.append(record)

    print("\n" + format_detail(record) + "\n")


def show_detail(records):

    if not records:
        print("No students recorded.\n")
        return

    for i, r in enumerate(records, 1):
        print(f"  {i}. {r['name']}")

    idx = prompt(
        "Select student number: ",
        lambda t: validate_count(t, 1, len(records))
    )

    print("\n" + format_detail(records[idx - 1]) + "\n")


def main():

    records = []

    menu = (
        "=== Student Grade Management System ===\n"
        "1. Enter a student's marks\n"
        "2. Show results for all students\n"
        "3. Show one student's detail\n"
        "4. Quit"
    )

    while True:

        print(menu)

        choice = input("Choose an option: ").strip()

        if choice == "1":
            enter_student(records)

        elif choice == "2":
            print("\n" + format_results(records) + "\n")

        elif choice == "3":
            show_detail(records)

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("  Invalid option. Enter 1-4.\n")


# ----------------------------------------------------------------
# Program Entry Point
# ----------------------------------------------------------------

if __name__ == "__main__":
    main()
