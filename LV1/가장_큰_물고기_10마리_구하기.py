import sqlite3


def solution():
    return """
      SELECT ID, LENGTH
      FROM FISH_INFO
      WHERE LENGTH IS NOT NULL
      ORDER BY LENGTH DESC, ID ASC
      LIMIT 10;
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
            (5, 2, 13, "2021-04-28"),
            (6, 3, 60, "2021-07-27"),
            (7, 0, 55, "2021-01-18"),
            (8, 2, 73, "2020-01-28"),
            (9, 3, 73, "2021-04-08"),
            (10, 2, 22, "2020-06-28"),
            (11, 2, 17, "2022-12-23"),
        ],
        "expected": [
            (8, 73.0),
            (9, 73.0),
            (6, 60.0),
            (7, 55.0),
            (1, 50.0),
            (2, 40.0),
            (0, 30.0),
            (10, 22.0),
            (3, 20.0),
            (11, 17.0),
        ],
    },
    {
        "name": "동일한 길이일 때 ID 정렬 확인",
        "rows": [
            (15, 0, 100, "2024-01-01"),
            (3, 1, 100, "2024-01-02"),
            (9, 2, 100, "2024-01-03"),
            (1, 0, 90, "2024-01-04"),
            (2, 0, 80, "2024-01-05"),
            (4, 0, 70, "2024-01-06"),
            (5, 0, 60, "2024-01-07"),
            (6, 0, 50, "2024-01-08"),
            (7, 0, 40, "2024-01-09"),
            (8, 0, 30, "2024-01-10"),
            (10, 0, 20, "2024-01-11"),
            (11, 0, None, "2024-01-12"),
        ],
        "expected": [
            (3, 100.0),
            (9, 100.0),
            (15, 100.0),
            (1, 90.0),
            (2, 80.0),
            (4, 70.0),
            (5, 60.0),
            (6, 50.0),
            (7, 40.0),
            (8, 30.0),
        ],
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

        solution_function = globals().get("solution")
        if solution_function is None:
            print(
                f"NOT RUN | {test_case['name']} | "
                "파일 위쪽에 solution 함수를 직접 작성하세요."
            )
            return

        query = solution_function()
        if not isinstance(query, str) or not query.strip():
            print(f"NOT RUN | {test_case['name']} | solution SQL이 비어 있습니다.")
            return

        cursor = connection.execute(query)
        actual = cursor.fetchall()
        actual_columns = tuple(column[0].upper() for column in cursor.description or [])
        expected = test_case["expected"]

        if actual == expected and actual_columns == ("ID", "LENGTH"):
            print(f"PASS | {test_case['name']}")
        else:
            print(f"FAIL | {test_case['name']}")
            print(f"  기대 컬럼: ('ID', 'LENGTH')")
            print(f"  실제 컬럼: {actual_columns}")
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
