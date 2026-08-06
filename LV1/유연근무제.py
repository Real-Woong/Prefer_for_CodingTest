# 프로그래머스 388351 - 유연근무제
# https://school.programmers.co.kr/learn/courses/30/lessons/388351

# [오답 정리]
# 1. 문제 해석 미스: 요일의 순환을 생각하지 못했다.
#    처음에는 startday를 기준으로 [startday - 1:5]만 잘랐다.
#    그러면 금요일처럼 뒤쪽에서 시작할 때 주말 뒤의 월~목요일을
#    확인하지 못한다. 7일은 순환하므로 시작일을 기준으로 토·일요일의
#    인덱스를 계산한 뒤, 주말만 제외해야 한다.
# 2. enumerate를 처음 사용했다.
#    enumerate(배열)는 배열을 튜플로 저장하는 것이 아니라,
#    반복할 때 (인덱스, 값) 형태의 쌍을 하나씩 반환한다.
# 3. HHMM 형식의 시간에 처음에는 그냥 10을 더해 분 올림을 놓쳤다.
#    예: 08:55 + 10분은 865가 아니라 09:05(905)다.
#    분이 60 이상이 되면 시간을 1 올리는 add_10_minutes 처리가 필요하다.

schedules1 = [700, 800, 1100]
timelogs1 =  [
                [710, 2359, 1050, 700, 650, 631, 659],
                [800, 801, 805, 800, 759, 810, 809],
                [1105, 1001, 1002, 600, 1059, 1001, 1100],
            ]
startday1 = 5 

s = [730, 855, 700, 720]
t = [
[710, 700, 650, 735, 700, 931, 912],
[908, 901, 805, 815, 800, 831, 835],
[705, 701, 702, 705, 710, 710, 711],
[707, 731, 859, 913, 934, 931, 905],
    ]
start = 1

def add_10_minutes(time):
    hour = time // 100
    minute = time % 100 + 10

    if minute >= 60:
        hour += 1
        minute -= 60

    return hour * 100 + minute

def filtering_day(days, start):
    sat = (6 - start) % 7
    sun = (7 - start) % 7
    
    return [[time for index, time in enumerate(employee_logs) if index not in (sat, sun)] for employee_logs in days]
    

def solution(schedules, timelogs, startday):
    # 시작 요일을 기준으로 주말을 제외한다.
    filtered_by_startday = filtering_day(timelogs, startday)
    # print(f"필터링: {filtered_by_startday}")
    add_10m = [add_10_minutes(time) for time in schedules]
    # print(f"직원들의 이벤트 참여 가능날짜: {filtered_by_startday}")
    # print(f"직원들의 출근 최댓값: {add_10m}")
    
    # 지각허용 범위인 add_10ms 와 이벤트 참여가능날짜를 각각 비교해
    # 사람마다 지각한 수를 샌다
    # 만약 0이면 answer변수에 1을 더해 이벤트선물을 줄 사람 수를 구한다
    index = 0
    answer = 0
    count_late = [0] * len(add_10m)
    for i in add_10m:
        for j in filtered_by_startday[index]:
            if j > i : 
                count_late[index] += (1)
        index += 1
    # print(f"지각했나? {count_late}")
    
    
    for i in count_late:
        if i == 0:
            answer += 1
            
    return answer        
            
    


print(solution(schedules1, timelogs1, startday1))
print(solution(s, t, start))

# def run_test(number, schedules, timelogs, startday, expected):
#     result = solution(schedules, timelogs, startday)

#     print(f"테스트 케이스 {number}")
#     print(f"schedules: {schedules}")
#     print(f"timelogs: {timelogs}")
#     print(f"startday: {startday}")
#     print(f"실행 결과: {result}")
#     print(f"기대 결과: {expected}")
#     print(f"일치 여부: {result == expected}")
#     print("-" * 45)


# if __name__ == "__main__":
#     test_cases = [
#         (
#             [700, 800, 1100],
#             [
#                 [710, 2359, 1050, 700, 650, 631, 659],
#                 [800, 801, 805, 800, 759, 810, 809],
#                 [1105, 1001, 1002, 600, 1059, 1001, 1100],
#             ],
#             5,
#             3,
#         ),
#         (
#             [730, 855, 700, 720],
#             [
#                 [710, 700, 650, 735, 700, 931, 912],
#                 [908, 901, 805, 815, 800, 831, 835],
#                 [705, 701, 702, 705, 710, 710, 711],
#                 [707, 731, 859, 913, 934, 931, 905],
#             ],
#             1,
#             2,
#         ),
#     ]

    # for number, test_case in enumerate(test_cases, start=1):
    #     run_test(number, *test_case)
