# 토요일 통합 트랙 1 - 행렬 기초
#
# 선형대수 개념을 파이썬으로 직접 구현한다.
# NumPy 를 쓰지 말고 반복문으로 만든다. 그래야 코테 구현력 연습이 같이 된다.
#
# 아래 세 함수의 pass 를 지우고 직접 채운다.
# 정답은 여기 없다. 채점기가 알려준다.


def mat_vec(A, v):
    """행렬 A 와 벡터 v 의 곱. 결과는 벡터(1차원 리스트).

    핵심: 이게 '선형변환'이다. 벡터 v 가 A 에 의해 다른 벡터로 옮겨진다.
    A 의 각 행과 v 를 각각 내적하면 결과 벡터의 각 성분이 나온다.
    """
    pass


def transpose(A):
    """행렬 A 의 전치. 행과 열을 뒤바꾼다.

    힌트: 결과의 [i][j] 자리에 원본의 무엇이 들어가야 하는가?
    택배 상자 문제에서 배운 것과 같다 —
    '어느 방향으로 옮길까'가 아니라 '몇 번 칸에 쓸까'로 생각한다.
    """
    pass


def matmul(A, B):
    """행렬 A 와 B 의 곱.

    핵심: 이건 '변환의 합성'이다. B 로 변환한 다음 A 로 변환하는 것과 같다.
    A 가 (n x m), B 가 (m x p) 이면 결과는 (n x p).
    가운데 m 이 맞지 않으면 곱할 수 없다.
    """
    pass


# ---------------------------------------------------------------
# 채점기 — 기대값은 손으로 계산해서 넣어둔 것이다.
# ---------------------------------------------------------------
TESTS = [
    ("mat_vec", mat_vec,
     [
         # (인자들, 기대값, 설명)
         (([[1, 2], [3, 4]], [5, 6]), [17, 39], "기본"),
         (([[2, 0], [0, 3]], [1, 1]), [2, 3], "x축 2배, y축 3배로 늘리는 변환"),
         (([[0, -1], [1, 0]], [1, 0]), [0, 1], "반시계 90도 회전 변환"),
     ]),
    ("transpose", transpose,
     [
         (([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]], "2x3 -> 3x2"),
         (([[1]],), [[1]], "1x1"),
         (([[1, 2], [3, 4]],), [[1, 3], [2, 4]], "정방행렬"),
     ]),
    ("matmul", matmul,
     [
         (([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]], "2x2"),
         (([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]]),
          [[58, 64], [139, 154]], "2x3 곱하기 3x2"),
         (([[0, -1], [1, 0]], [[0, -1], [1, 0]]),
          [[-1, 0], [0, -1]], "90도 회전 두 번 = 180도 회전"),
     ]),
]


def main():
    total = passed = 0

    for name, func, cases in TESTS:
        print(f"\n=== {name} ===")
        for args, expected, note in cases:
            total += 1
            try:
                result = func(*args)
            except Exception as error:
                print(f"  [오류] {note}: {type(error).__name__}: {error}")
                continue

            if result is None:
                print(f"  [미구현] {note}")
                continue

            if result == expected:
                passed += 1
                print(f"  [통과] {note}")
            else:
                print(f"  [실패] {note}")
                print(f"         결과  : {result}")
                print(f"         기대값: {expected}")

    print(f"\n{passed} / {total} 통과")

    # NumPy 가 설치되어 있으면 무작위 행렬로 한 번 더 검증한다.
    # (선택 사항 — pip install numpy)
    try:
        import numpy as np
    except ImportError:
        print("\n(numpy 가 없어 무작위 교차검증은 건너뜀. pip install numpy 하면 켜진다.)")
        return

    sample = [[1, 2], [3, 4]]
    if transpose(sample) is None or matmul(sample, sample) is None:
        return  # 아직 구현 전이면 교차검증은 의미가 없다

    rng = np.random.default_rng(0)
    mismatches = 0
    for _ in range(200):
        n, m, p = rng.integers(1, 6, size=3)
        A = rng.integers(-9, 10, size=(n, m))
        B = rng.integers(-9, 10, size=(m, p))
        if matmul(A.tolist(), B.tolist()) != (A @ B).tolist():
            mismatches += 1
        if transpose(A.tolist()) != A.T.tolist():
            mismatches += 1
    print(f"무작위 교차검증 200회 - 불일치 {mismatches}건")


if __name__ == "__main__":
    main()
