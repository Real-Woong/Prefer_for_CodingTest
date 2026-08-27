import sqlite3


def solution():
    """프로그래머스에 제출할 SQL을 반환합니다."""
    return """
    SELECT CONCAT(MAX(LENGTH), 'cm') AS MAX_LENGTH
    FROM FISH_INFO;
    """


CREATE_TABLE_SQL = """
CREATE TABLE FISH_INFO (
    ID INTEGER NOT NULL,
    FISH_TYPE INTEGER NOT NULL,
    LENGTH REAL,
    TIME DATE NOT NULL
);
"""


TEST_CASES = [
    {
        "name": "프로그래머스 예제",
        "rows": [
            (0, 0, 13.37, "2021-12-04"),
            (1, 0, 50.00, "2020-03-07"),
            (2, 0, 40.00, "2020-03-07"),
            (3, 1, 43.33, "2022-03-09"),
            (4, 1, None, "2022-04-08"),
            (5, 2, 32.00, "2020-04-28"),
        ],
        "expected": "50.0cm",
    },
    {
        "name": "NULL을 제외하고 최댓값 구하기",
        "rows": [
            (0, 0, None, "2024-01-01"),
            (1, 1, 18.25, "2024-01-02"),
            (2, 2, 99.75, "2024-01-03"),
            (3, 3, None, "2024-01-04"),
            (4, 0, 75.50, "2024-01-05"),
        ],
        "expected": "99.75cm",
    },
]


def concat(*values):
    """테스트용 SQLite에서 MySQL의 CONCAT 함수를 흉내 냅니다."""
    if any(value is None for value in values):
        return None
    return "".join(str(value) for value in values)


def run_test(test_case):
    connection = sqlite3.connect(":memory:")

    try:
        connection.create_function("CONCAT", -1, concat)
        connection.execute(CREATE_TABLE_SQL)
        connection.executemany(
            """
            INSERT INTO FISH_INFO (ID, FISH_TYPE, LENGTH, TIME)
            VALUES (?, ?, ?, ?)
            """,
            test_case["rows"],
        )

        query = solution()

        if not query.strip():
            print(f"NOT RUN | {test_case['name']} | solution SQL이 비어 있습니다.")
            return

        cursor = connection.execute(query)
        result_row = cursor.fetchone()
        actual = result_row[0] if result_row is not None else None
        actual_column = cursor.description[0][0] if cursor.description else None
        expected = test_case["expected"]

        if actual == expected and actual_column.upper() == "MAX_LENGTH":
            print(f"PASS | {test_case['name']} | 결과: {actual}")
        else:
            print(f"FAIL | {test_case['name']}")
            print(f"  기대 컬럼: MAX_LENGTH")
            print(f"  실제 컬럼: {actual_column}")
            print(f"  기대 결과: {expected}")
            print(f"  실제 결과: {actual}")
    finally:
        connection.close()


if __name__ == "__main__":
    for case in TEST_CASES:
        try:
            run_test(case)
        except sqlite3.Error as error:
            print(f"SQL ERROR | {case['name']} | {error}")
