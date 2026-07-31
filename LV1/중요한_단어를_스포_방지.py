# 프로그래머스 468370 - 중요한 단어를 스포 방지


def solution(message, spoiler_ranges):
    # 여기에 풀이를 작성하세요.
    # message: 문자열
    # spoiler_ranges: [[start, end], ...]
    pass


def run_test(number, message, spoiler_ranges, expected):
    result = solution(message, spoiler_ranges)
    passed = result == expected

    print(f"테스트 {number}")
    print(f"message: {message!r}")
    print(f"spoiler_ranges: {spoiler_ranges}")
    print(f"내 결과: {result}")
    print(f"기대값: {expected}")
    print(f"통과 여부: {passed}")
    print("-" * 45)


if __name__ == "__main__":
    test_cases = [
        (
            "here is muzi here is a secret message",
            [[0, 3], [23, 28]],
            1,
        ),
        (
            "my phone number is 01012345678 and may i have your phone number",
            [[5, 5], [25, 28], [34, 40], [53, 59]],
            4,
        ),
    ]

    for number, (message, spoiler_ranges, expected) in enumerate(test_cases, start=1):
        run_test(number, message, spoiler_ranges, expected)
