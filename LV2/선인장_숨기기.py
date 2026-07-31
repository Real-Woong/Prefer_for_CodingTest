import random
def solution(m, n, h, w, drops):
    # m x n 크기의 지도 안에서
    # h x w 크기 선인장을 놓을 수 있는
    # "왼쪽 위 좌표 후보"를 하나씩 확인한다.
    

    # 위쪽 행부터 확인한다.
    # 행이 같다면 왼쪽 열부터 확인한다.
    for top_row in ...:
        for top_col in ...:

            # 현재 선인장의 왼쪽 위 좌표는
            # [top_row, top_col] 이다.

            # 이 선인장이 실제로 차지하는 범위는
            # 행: top_row부터 h칸
            # 열: top_col부터 w칸
            # 이다.

            # drops를 첫 번째 비부터 순서대로 확인한다.
            for rain_order, drop in enumerate(drops):

                # 현재 비의 좌표 drop이
                # 현재 선인장 사각형 안에 들어오는지 확인한다.

                # 처음으로 사각형 안에 들어온 비를 발견하면
                # 이 선인장이 처음 젖는 시점을 기록한다.
                # 이후의 비는 볼 필요가 없으므로 멈춘다.
                pass

            # 끝까지 봤는데 선인장 안에 비가 한 번도 안 왔다면
            # 이 후보는 "비를 맞지 않는 후보"다.
            # 이런 후보가 있으면 가장 우선이다.

            # 각 후보의 "처음 비를 맞는 시점"을 비교한다.
            # 더 늦게 맞는 후보로 정답을 갱신한다.

            # 같은 시점이라면,
            # 더 위쪽 행 → 더 왼쪽 열 후보를 선택한다.

    # 선택된 선인장 구역의 왼쪽 위 좌표를 반환한다.


def make_random_case():
    # 확인하기 쉽도록 작은 지도 생성
    m = random.randint(1, 6)
    n = random.randint(1, 6)

    h = random.randint(1, m)
    w = random.randint(1, n)

    # 지도에 존재하는 모든 좌표
    all_coordinates = []

    for row in range(m):
        for col in range(n):
            all_coordinates.append([row, col])

    # 빗방울 개수는 1개부터 전체 칸 개수까지
    drop_count = random.randint(1, m * n)

    # 같은 칸에 두 번 떨어지지 않도록 무작위 선택
    drops = random.sample(all_coordinates, drop_count)

    return m, n, h, w, drops


def check_answer(m, n, h, w, answer):
    # 반환 형식 확인
    if not isinstance(answer, list):
        return False, "반환값이 리스트가 아닙니다."

    if len(answer) != 2:
        return False, "반환값에는 좌표 2개가 있어야 합니다."

    row, col = answer

    if not isinstance(row, int) or not isinstance(col, int):
        return False, "좌표는 정수여야 합니다."

    # 선인장 구역이 지도 밖으로 나가는지 확인
    if not (0 <= row <= m - h):
        return False, "행 좌표 때문에 선인장 구역이 지도 밖으로 나갑니다."

    if not (0 <= col <= n - w):
        return False, "열 좌표 때문에 선인장 구역이 지도 밖으로 나갑니다."

    return True, "기본 형식과 좌표 범위가 정상입니다."


if __name__ == "__main__":
    # 실행할 때마다 같은 테스트를 생성
    random.seed(1234)

    for test_number in range(1, 11):
        m, n, h, w, drops = make_random_case()

        print(f"\n===== 테스트 {test_number} =====")
        print(f"m={m}, n={n}, h={h}, w={w}")
        print(f"drops={drops}")

        try:
            answer = solution(m, n, h, w, drops)
            print(f"solution 결과={answer}")

            passed, message = check_answer(m, n, h, w, answer)
            print(f"기본 검사={passed}, {message}")

        except Exception as error:
            print(f"실행 중 오류 발생: {type(error).__name__}: {error}")