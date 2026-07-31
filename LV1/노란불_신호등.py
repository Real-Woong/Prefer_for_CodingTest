def solution(signals):
    

    
    pass


if __name__ == "__main__":
    test_cases = [
        ([[2, 1, 2], [5, 1, 1]], 13),
        ([[2, 3, 2], [3, 1, 3], [2, 1, 1]], 11),
        ([[3, 3, 3], [5, 4, 2], [2, 1, 2]], 193),
        ([[1, 1, 4], [2, 1, 3], [3, 1, 2], [4, 1, 1]], -1),
    ]

    for number, (signals, expected) in enumerate(test_cases, start=1):
        result = solution(signals)

        print(f"테스트 {number}")
        print(f"입력: {signals}")
        print(f"내 결과: {result}")
        print(f"기대값: {expected}")
        print(f"통과 여부: {result == expected}")
        print("-" * 30)