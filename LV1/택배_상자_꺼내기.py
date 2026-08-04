# 프로그래머스 389478 - 택배 상자 꺼내기

n1 = 22
w1 = 6
num1 = 8

n = 13
w = 3
num = 6

#숫자 좌표 찾기
def finding_number(col, row, num, array):
    answer = 0

    for i in range(row + 1):
        for j in range(col):
            if array[i][j] == num:
                num_x = j
                break
                
    same_x = [array[k][num_x] for k in range(row + 1)]

    print(f"{num}과 같은 y좌표의 숫자들은: \n{same_x}\n")

    for i in same_x:
        if i >= num:
            answer += 1

    return answer

def solution(n, w, num):
    # 여기에 풀이를 작성하세요.
    # n: 전체 상자 수
    # w: 한 층의 상자 수
    # num: 꺼낼 상자 번호
    
    # 상자n개를 한줄씩 나눈다
    line_h = (n // w) - 1
    remain_box = n % w
    if remain_box != 0:
        hall_h = line_h + 1
    else: hall_h = line_h

    # 상자를 넣을 2차원 배열 생성
    arr = [[0] * (w) for _ in range(hall_h + 1)]
    number = 1

    # 상자에 n만큼 집어넣기
    for i in range(hall_h + 1):
        if i <= line_h:
            # print(f"현재 y좌표: {i}")
            for j in range(w):
                if i % 2 == 0: #짝수 번째 줄 똑바로
                    arr[i][j] = number
                else: #홀수 번째줄
                    arr[i][w - 1 - j] = number
                number += 1
        else: # 나머지 줄 (다 채워지지 않을 줄)
            for j in range(remain_box):
                # print(f"현재 y좌표: {i}")
                if i % 2 == 0: #짝수 번째 줄 똑바로
                    arr[i][j] = number
                    # print(f" 마지막줄 ( {i} , {j} )")
                else: #홀수 번째줄
                    arr[i][w - 1 - j] = number
                    # print(f"마지막줄 ( {i} , {j} )")
                number += 1


 
    # num 찾기
    answer = finding_number(w, hall_h, num, arr)
    


    # num포함한 위에 쌓인 숫자들 갯수 찾기

                

    print(f"높이 0 부터: {line_h}")
    print(f"전체높이 0 부터: {hall_h}")
    print(f"남은상자: {remain_box} \n")
    for row in arr:
      print(row)
    
    
    return answer

print("example1 ---------")
print(solution(n1, w1, num1))
print("example2 ---------")
print(solution(n, w, num))

# def run_test(number, n, w, num, expected):
#     result = solution(n, w, num)
#     passed = result == expected

#     print(f"테스트 {number}")
#     print(f"n={n}, w={w}, num={num}")
#     print(f"내 결과: {result}")
#     print(f"기대값: {expected}")
#     print(f"통과 여부: {passed}")
#     print("-" * 45)


# if __name__ == "__main__":
#     test_cases = [
#         (22, 6, 8, 3),
#         (13, 3, 6, 4),
#     ]

#     for number, (n, w, num, expected) in enumerate(test_cases, start=1):
#         run_test(number, n, w, num, expected)

# list_comprehension: [새로운list에들어갈값_연산까지다해서 for 변수 in 반복문이_도는공간 if 조건]


# [오답 정리 - 지그재그 역방향 채우기]
#
# 1. 홀수 번째 줄을 오른쪽에서 왼쪽으로 채우는 방법이 떠오르지 않아 막혔다.
#    각 줄마다 방향이 바뀐다는 것(i % 2)까지는 이해했는데,
#    "배열은 왼쪽부터 순서대로 채워야 한다"고 생각해서 그 다음이 막혔다.
#    -> 배열은 순서대로 쓸 필요가 없다. 아무 인덱스에나 바로 쓸 수 있다.
#       "어느 방향으로 쓸까"가 아니라 "몇 번 칸에 쓸까"를 구하는 문제로 바꾸면
#       방향 문제가 아니라 인덱스 계산 문제가 된다.
#
# 2. w - 1 - j 는 어디서 나오는가 (외우지 말고 유도하기)
#    w = 6 일 때, 뒤집으면 어느 칸이 어디로 가는지 짝을 지어본다.
#
#      j        :  0  1  2  3  4  5
#      뒤집으면 :  5  4  3  2  1  0
#      두 수의 합:  5  5  5  5  5  5   <- 항상 같다
#
#    대응하는 두 인덱스의 합은 항상 (맨앞 + 맨뒤) = 0 + (w - 1) = w - 1 이다.
#    따라서 j 의 짝은 (w - 1) - j.
#
# 3. 일반화: 구간 [a, b] 를 뒤집으면   j  ->  a + b - j
#      0-based 배열 전체 : a=0, b=w-1  ->  w - 1 - j    (이 문제)
#      1-based           : a=1, b=w    ->  w + 1 - j
#      부분 구간 [2, 7]  : a=2, b=7    ->  9 - j
#
# 4. 검산법 (off-by-one 이 헷갈릴 때 5초 만에 확인)
#    양 끝 두 개만 대입해 본다. 1차식이므로 양 끝이 맞으면 중간은 자동으로 맞다.
#      j = 0     ->  w - 1 - 0       = w - 1   (맨 오른쪽)  OK
#      j = w - 1 ->  w - 1 - (w - 1) = 0       (맨 왼쪽)    OK
#
# 5. 이 공식을 몰라도 푸는 길이 있었다: 순회 방향 자체를 뒤집는다.
#
#      cols = range(w) if i % 2 == 0 else range(w - 1, -1, -1)
#      for j in cols:
#          arr[i][j] = number
#          number += 1
#
#    "오른쪽부터 넣고 싶다"를 그대로 옮긴 코드라 인덱스 산수가 아예 없다.
#    막혔을 때 공식을 만들어내려 하지 말고, 순회 순서를 바꾸는 길도 떠올리자.
#
# 6. 이 사고방식(방향 -> 좌표 변환)은 격자 문제 전반에서 계속 반복된다.
#    회전, 대각선 순회, 나선형(달팽이) 채우기가 전부 같은 접근이다.

# list에 역으로 넣기


# [코드에서 고칠 점 - 틀리진 않았지만 의도대로 동작하지 않는 부분]
#
# 7. finding_number 의 break 가 반쪽짜리다. (15 ~ 19줄)
#
#      for i in range(row + 1):
#          for j in range(col):
#              if array[i][j] == num:
#                  num_x = j
#                  break        # <- 안쪽 for 만 빠져나온다. 바깥 for 는 계속 돈다
#
#    num 을 찾은 뒤에도 남은 행을 전부 훑는다.
#    결과가 맞았던 건 num 이 배열에 딱 하나뿐이라 num_x 가 덮어써지지 않았기 때문이고,
#    의도대로 동작한 것은 아니다.
#    -> 이중 반복문을 한 번에 빠져나오려면 break 를 두 번 쓰거나,
#       찾는 즉시 return 하는 별도 함수로 분리하는 것이 깔끔하다.
#
#    추가로, num 이 배열에 없으면 num_x 가 아예 만들어지지 않아
#    다음 줄에서 UnboundLocalError 가 난다.
#    이 문제는 num 이 항상 1 ~ n 이라 걸리지 않았을 뿐, 안전한 코드는 아니다.
#    -> num_x = -1 처럼 초기값을 두고 못 찾은 경우를 명시적으로 처리하자.
#
# 8. 변수명과 실제 의미가 어긋난다.
#
#    same_x 라는 이름인데 실제로 모으는 것은 같은 "열(column)" 의 값들이고,
#    출력 문구도 "같은 y좌표" 라고 되어 있다. (21, 23줄)
#    x / y 좌표 용어와 행 / 열 인덱스를 섞어 쓰면 나중에 내가 제일 헷갈린다.
#    -> same_col 로 통일하고, 출력도 "같은 열의 숫자들" 로 바꾸자.
#
#    매개변수 이름도 마찬가지다. finding_number(col, row, num, array) 에
#    실제로 넘기는 값은 finding_number(w, hall_h, ...) 이므로
#      col  = w      -> 열의 "개수"
#      row  = hall_h -> 마지막 행의 "인덱스"
#    개수와 인덱스가 같은 자리에 섞여 있다.
#    -> width, last_row 처럼 개수인지 인덱스인지 이름에 드러내자.