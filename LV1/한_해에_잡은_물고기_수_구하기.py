import sqlite3


# 프로그래머스 298516 - 한 해에 잡은 물고기 수 구하기
# https://school.programmers.co.kr/learn/courses/30/lessons/298516


def solution():
    """프로그래머스에 제출할 SQL을 문자열 안에 작성하세요."""
    return """
    SELECT COUNT(*) AS FISH_COUNT
    FROM FISH_INFO
    WHERE YEAR(TIME) = 2021;
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
        ],
        "expected": [(3,)],
    },
    {
        "name": "연도 경계값과 NULL 길이 확인",
        "rows": [
            (10, 0, 10, "2020-12-31"),
            (11, 1, None, "2021-01-01"),
            (12, 2, 30, "2021-12-31"),
            (13, 3, 40, "2022-01-01"),
        ],
        "expected": [(2,)],
    },
    {
        "name": "2021년에 잡은 물고기가 없는 경우",
        "rows": [
            (20, 0, 10, "2020-06-15"),
            (21, 1, 20, "2022-06-15"),
        ],
        "expected": [(0,)],
    },
]


def run_test(test_case):
    connection = sqlite3.connect(":memory:")

    try:
        # 프로그래머스(MySQL)의 YEAR()를 SQLite에서도 테스트할 수 있게 한다.
        connection.create_function("YEAR", 1, lambda date: int(date[:4]))
        connection.execute(CREATE_TABLE_SQL)
        connection.executemany(
            """
            INSERT INTO FISH_INFO (ID, FISH_TYPE, LENGTH, TIME)
            VALUES (?, ?, ?, ?)
            """,
            test_case["rows"],
        )

        query = solution()
        if not isinstance(query, str) or not query.strip():
            print(
                f"NOT RUN | {test_case['name']} | "
                "solution 함수의 문자열 안에 SQL을 작성하세요."
            )
            return False

        cursor = connection.execute(query)
        actual = cursor.fetchall()
        actual_columns = tuple(
            column[0].upper() for column in cursor.description or []
        )
        expected = test_case["expected"]

        passed = actual == expected and actual_columns == ("FISH_COUNT",)
        if passed:
            print(f"PASS | {test_case['name']} | 결과: {actual[0][0]}")
        else:
            print(f"FAIL | {test_case['name']}")
            print("  기대 컬럼: ('FISH_COUNT',)")
            print(f"  실제 컬럼: {actual_columns}")
            print(f"  기대 결과: {expected}")
            print(f"  실제 결과: {actual}")

        return passed
    finally:
        connection.close()


if __name__ == "__main__":
    results = []

    for case in TEST_CASES:
        try:
            results.append(run_test(case))
        except sqlite3.Error as error:
            results.append(False)
            print(f"SQL ERROR | {case['name']} | {error}")

    print(f"\n{sum(results)} / {len(results)} 통과")
