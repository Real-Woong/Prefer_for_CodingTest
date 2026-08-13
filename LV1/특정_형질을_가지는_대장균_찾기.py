import sqlite3


def solution():
    """프로그래머스에 제출할 SQL을 문자열 안에 작성하세요."""
    return """
    SELECT COUNT(*) AS COUNT
    FROM ECOLI_DATA
    WHERE (GENOTYPE & 1 > 0 OR GENOTYPE & 4 > 0) 
    AND (GENOTYPE & 2 = 0 )

    """


TEST_CASES = [
    {
        "name": "프로그래머스 예제",
        "rows": [
            (1, None, 10, "2019-01-01", 8),
            (2, None, 2, "2019-01-01", 15),
            (3, 2, 100, "2020-01-01", 1),
            (4, 2, 16, "2020-01-01", 13),
        ],
        "expected": 2,
    },
    {
        "name": "조건을 만족하는 개체가 없는 경우",
        "rows": [
            (1, None, 10, "2021-01-01", 2),
            (2, 1, 20, "2021-01-02", 8),
            (3, 1, 30, "2021-01-03", 10),
        ],
        "expected": 0,
    },
    {
        "name": "1번 또는 3번 형질 조합 확인",
        "rows": [
            (1, None, 10, "2022-01-01", 1),
            (2, 1, 20, "2022-01-02", 4),
            (3, 1, 30, "2022-01-03", 5),
            (4, 2, 40, "2022-01-04", 3),
            (5, 2, 50, "2022-01-05", 6),
        ],
        "expected": 3,
    },
]


CREATE_TABLE_SQL = """
CREATE TABLE ECOLI_DATA (
    ID INTEGER NOT NULL,
    PARENT_ID INTEGER,
    SIZE_OF_COLONY INTEGER NOT NULL,
    DIFFERENTIATION_DATE DATE NOT NULL,
    GENOTYPE INTEGER NOT NULL
);
"""


def run_test(test_case):
    connection = sqlite3.connect(":memory:")

    try:
        connection.execute(CREATE_TABLE_SQL)
        connection.executemany(
            """
            INSERT INTO ECOLI_DATA (
                ID,
                PARENT_ID,
                SIZE_OF_COLONY,
                DIFFERENTIATION_DATE,
                GENOTYPE
            )
            VALUES (?, ?, ?, ?, ?)
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

        if (
            actual == expected
            and actual_column is not None
            and actual_column.upper() == "COUNT"
        ):
            print(f"PASS | {test_case['name']} | 결과: {actual}")
        else:
            print(
                f"FAIL | {test_case['name']} | "
                f"기댓값: COUNT={expected}, "
                f"실제값: {actual_column}={actual}"
            )
    finally:
        connection.close()


if __name__ == "__main__":
    for case in TEST_CASES:
        try:
            run_test(case)
        except sqlite3.Error as error:
            print(f"SQL ERROR | {case['name']} | {error}")
