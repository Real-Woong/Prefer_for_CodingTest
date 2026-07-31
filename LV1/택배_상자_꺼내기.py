# 프로그래머스 389478 - 택배 상자 꺼내기


def solution(n, w, num):
    # 여기에 풀이를 작성하세요.
    # n: 전체 상자 수
    # w: 한 층의 상자 수
    # num: 꺼낼 상자 번호
    pass


def run_test(number, n, w, num, expected):
    result = solution(n, w, num)
    passed = result == expected

    print(f"테스트 {number}")
    print(f"n={n}, w={w}, num={num}")
    print(f"내 결과: {result}")
    print(f"기대값: {expected}")
    print(f"통과 여부: {passed}")
    print("-" * 45)


if __name__ == "__main__":
    test_cases = [
        (22, 6, 8, 3),
        (13, 3, 6, 4),
    ]

    for number, (n, w, num, expected) in enumerate(test_cases, start=1):
        run_test(number, n, w, num, expected)
