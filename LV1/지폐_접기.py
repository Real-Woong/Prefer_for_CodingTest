# 프로그래머스 340199 - 지폐 접기
# https://school.programmers.co.kr/learn/courses/30/lessons/340199
# 1. 지폐를 접은 횟수를 저장할 정수 변수 answer를 만들고 0을 저장합니다.
# 2. 반복문을 이용해 bill의 작은 값이 wallet의 작은 값 보다 크거나 bill의 큰 값이 wallet의 큰 값 보다 큰 동안 아래 과정을 반복합니다.
#     2-1. bill[0]이 bill[1]보다 크다면
#         bill[0]을 2로 나누고 나머지는 버립니다.
#     2-2. 그렇지 않다면
#         bill[1]을 2로 나누고 나머지는 버립니다.
#     2-3. answer을 1 증가시킵니다.
# 3. answer을 return합니다.

wallet1 = [30, 15]
bill1 = [26, 17]

wallet2 = [50, 50]
bill2 = [100, 241]


            

def solution(wallet, bill):
    # 접은횟수 
    answer = 0
    # bill의 작은 값이 wallet의 작은 값보다 크거나 OR bill의 큰 값이 wallet의 큰 값보다 큰 동안 반복
    # 즉 가로세로가 아니라 그냥 큰값, 작은값을 짝지어서 비교
    while min(bill) > min(wallet) or max(bill) > max(wallet):
        # 가로세로가 아니라 큰 값 작은값중 하나를 접음
        # 그럼위에서 작은값의 index위치가 바뀌면 그게 bill을 90도로 돌린다는
        # 예:
        # bill = [32, 30] , wallet = [20, 16] 
        # [32와 20 비교, 30과 16비교]
        # 한번 반복문을 돌고 = [16, 30] | [20, 16]
        # 다시 돌면 [16과 16비교, 30과 20 비교] 즉 16과 16비교 때문에 while 조건에 False가 됨
        if bill[0] >= bill[1]:
            bill[0] //= 2
        else:
            bill[1] //= 2

        answer += 1
    return answer


print(solution(wallet1, bill1))  # 기대값: 1
print(solution(wallet2, bill2))  # 기대값: 4


# 오답정리
# 너무 어렵게 생각함:
# 문제는 그저 answer변수 reuturn하니 answer add를 스킵할때를말하건데 나는 진짜 지폐를 회전할때를 구해야한다고 생각함
# 즉 지금 여기서는 그냥 max min으로 했으면 됐음
# 틀린답:
    # 지갑의 가로세로 둘중 아무거나 큰지 아닌지 확인
    # 만약에 false면 둘중에 뭐가 큰지 확인
    # 하나는 true면 bill의 가로와 세로를 바꾸고 한번더 check
    # 여기서도 작으면 한번 접음
    # answer = 0
    # while(all(w >= b for w, b in zip(wallet, bill))):
    #     check = [w >= b for w, b in zip(wallet, bill)]
    #     print(check)


    #     for width, height in check:
    #         if width == False:
    #            bill[0] = bill[0] // 2
    #            check_for_rotate(wallet, bill)
    #            print(f"돈의 가로를 접음:  {bill[0]}")
    #            answer += 1
    #         elif height == False:
    #             bill[1] = bill[1] // 2
    #             check_for_rotate(wallet, bill)
    #             print(f"돈의 세로를 접음:  {bill[1]}")
    #             answer += 1
    #         else:
    #            bill[0] = bill[0] // 2
    #            check_for_rotate(wallet, bill)
    #            print(f"돈의 가로를 접음:  {bill[0]}")
    #            answer += 1   
# def check_for_rotate(wallet, bill):
#     #돈의 세로가 지갑의 가로보다 작을때
#     if bill[1] <= wallet[0]:
#         bill[0], bill[1] = bill[1], bill[0]
#     elif bill[0] <= wallet[1]:
#         bill[0], bill[1] = bill[1], bill[0]