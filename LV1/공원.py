# 프로그래머스 340198 - 공원
# https://school.programmers.co.kr/learn/courses/30/lessons/340198

mats1 = [5, 3, 2]
park1 = [
    ["A", "A", "-1", "B", "B", "B", "B", "-1"],
    ["A", "A", "-1", "B", "B", "B", "B", "-1"],
    ["-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1"],
    ["D", "D", "-1", "-1", "-1", "-1", "E", "-1"],
    ["D", "D", "-1", "-1", "-1", "-1", "-1", "F"],
    ["D", "D", "-1", "-1", "-1", "-1", "E", "-1"],
]

def find_area(mat, x, y, ex_set):
    is_solid = True # 꽉찼는지 확인
    for i in range(x, x + mat):
        for j in range(y, y + mat):
        # 해당 좌표가 ex_set에 없다면 (즉, -1이 아니라면)
            if (i, j) not in ex_set:
                is_solid = False # 꽉 찬 정사각형이 아닌 어딘가 공백이있음
                break

        if not is_solid:
            break
    if is_solid:
        return is_solid

def solution(mats, park):

    # 각 배열 col에서 -1인 부분의 갯수 즉 가로 길이 찾기
    # 그 위치가 -1인 위치까지 받아와서 row위치 까지 찾기
    ex = []
    for i, row in enumerate(park):
        for j, val in enumerate(row):
            if val == "-1":
                ex.append((i, j))

    x_counts = {}
    y_counts = {}
    for x, y in ex:
        if x not in x_counts:
            x_counts[x] = []
        x_counts[x].append(y)
        if y not in y_counts:
            y_counts[y] = []
        y_counts[y].append(x)

    # 기존에 모아둔 ex 리스트를 탐색 속도가 빠른 Set으로 변환 (Java의 HashSet과 동일)
    ex_set = set(ex)

    print("-------------------")
    print(x_counts)

    print("-------------------")
    print(y_counts)

    for mat in sorted(mats, reverse=True):
        for x, y in ex:
            if find_area(mat, x, y, ex_set):
                return mat

    if not find_area(mat, x, y, ex_set):
        return -1






print(solution(mats1, park1))

'''오답정리
# 1. 딕셔너리 초기화 누락 에러 (KeyError)
# [오답 원인]
# 딕셔너리에 키(방)가 없는 상태에서 바로 리스트에 값을 추가(.append)하려고 하면
# 파이썬이 해당 방이 없다고 에러를 뿜으며 프로그램이 멈춥니다.
# [해결]
if x not in x_counts:
    x_counts[x] = []
x_counts[x].append(y)
# (비유) 💡 "아직 지어지지 않은 빈방에 무작정 짐부터 던져 넣으면 알바생이 화를 냅니다. 방이 없으면 빈 방부터 먼저 만들고 물건을 넣으세요!"

# 2. 리스트와 셋(Set)의 탐색 속도 차이
# [오답 원인]
# 검사해야 할 좌표 면적이 넓을 때 리스트(List)를 그대로 쓰면 
# 컴퓨터가 처음부터 끝까지 전부 뒤져야 해서(시간 복잡도 O(N)) 시간 초과가 납니다.
# [해결]
ex_set = set(ex)  # 이름표가 붙은 사물함처럼 O(1)로 즉시 찾을 수 있게 set으로 변환
# (비유) 💡 "물건을 와르르 부어둔 큰 상자를 매번 뒤지지 말고, 이름표가 딱 붙어 있는 사물함(Set)에 정리해 두어야 한 방에 찾습니다."

# 3. 함수 반환값 누락 (None 반환 현상)
# [오답 원인]
# find_area 함수 안에서 꽉 차지 않았을 때(is_solid == False) 아무것도 return하지 않아 
# 파이썬이 자동으로 None을 반환하게 만들었습니다.
# [해결]
# 명확하게 True 또는 False를 반환하도록 설계
# (비유) 💡 "식당에 재료가 없으면 '안 됩니다'라고 똑바로 말해줘야지, 멍하니 입을 닫고 있으면 손님은 유령(None)이 나온 줄 압니다."

# 4. 반복문 덮어쓰기 문제 (가장 큰 돗자리를 놓치는 원인)
# [오답 원인]
# 큰 돗자리(3)를 찾았음에도 불구하고 반복문을 멈추지 않고 
# 그 아래 작은 돗자리(2)까지 계속 검사하면서 answer에 2를 덮어씌워 버렸습니다.
# [해결]
# break이나 answer 변수로 버티지 않고, 정답을 찾는 즉시 함수 전체를 끝내는 return 사용
for mat in sorted(mats, reverse=True):
    for x, y in ex:
        if find_area(mat, x, y, ex_set):
            return mat  # 즉시 반환하여 덮어쓰기 원천 차단
# (비유) 💡 "금메달을 찾았으면 길바닥에 떨어진 동전 주우러 가려 하지 말고, 그 즉시 들고 집으로 뛰어와야(return) 보물을 지킵니다!"
'''
