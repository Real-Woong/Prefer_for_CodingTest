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
    same_x = []

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