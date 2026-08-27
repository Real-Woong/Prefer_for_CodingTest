import sqlite3


def solution():
    """프로그래머스에 제출할 MySQL 쿼리를 반환합니다."""
    return """
    SELECT ROUND(AVG(COALESCE(LENGTH, 10)), 2) AS AVERAGE_LENGTH
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
            (0, 0, 30, "2021-12-04"),
            (1, 0, 50, "2020-03-07"),
            (2, 0, 40, "2020-03-07"),
            (3, 1, 20, "2022-03-09"),
            (4, 1, None, "2022-04-08"),
            (5, 2, None, "2021-04-28"),
        ],
        "expected": 26.67,
    },
    {
        "name": "NULL을 10cm로 포함하는지 확인",
        "rows": [
            (0, 0, None, "2024-01-01"),
            (1, 1, None, "2024-01-02"),
            (2, 2, 20, "2024-01-03"),
            (3, 3, 30, "2024-01-04"),
        ],
        "expected": 17.5,
    },
    {
        "name": "소수점 셋째 자리 반올림 확인",
        "rows": [
            (0, 0, 11, "2024-01-01"),
            (1, 1, 12, "2024-01-02"),
            (2, 2, 13, "2024-01-03"),
            (3, 3, 15.664, "2024-01-04"),
        ],
        "expected": 12.92,
    },
]


def run_test(test_case):
    connection = sqlite3.connect(":memory:")

    try:
        connection.execute(CREATE_TABLE_SQL)
        connection.executemany(
            """
            INSERT INTO FISH_INFO (ID, FISH_TYPE, LENGTH, TIME)
            VALUES (?, ?, ?, ?)
            """,
            test_case["rows"],
        )

        cursor = connection.execute(solution())
        result_row = cursor.fetchone()
        actual = result_row[0] if result_row is not None else None
        actual_column = cursor.description[0][0] if cursor.description else None
        expected = test_case["expected"]

        if actual == expected and actual_column.upper() == "AVERAGE_LENGTH":
            print(f"PASS | {test_case['name']} | 결과: {actual}")
        else:
            print(f"FAIL | {test_case['name']}")
            print("  기대 컬럼: AVERAGE_LENGTH")
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
