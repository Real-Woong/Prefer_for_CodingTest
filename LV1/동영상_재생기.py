# 프로그래머스 340213 - 동영상 재생기
# https://school.programmers.co.kr/learn/courses/30/lessons/340213

# 오답 원인1:
    # ":"을 제거한 값은 '총 초'가 아니라 MMSS 형태의 숫자이다.
    # 따라서 이 값에 바로 10을 더하거나 빼면 분 경계에서 잘못 계산된다.
    #
    # 예시 1:
    # 00:55 → 55
    # 55 + 10 → 65
    # 실제 결과는 01:05여야 하지만 중간값이 00:65 형태가 된다.
    #
    # 예시 2:
    # 01:05 → 105
    # 105 - 10 → 95
    # 실제 결과는 00:55여야 하지만 00:95 형태가 된다.
 # 오답 원인2:
        # 오프닝 검사는 모든 명령이 끝난 뒤 한 번만 하는 것이 아니라
        # 각 명령을 실행하여 위치가 변경될 때마다 확인해야 한다.
        #
        # 이 위치에서 opening_check()를 하지 않으면,
        # 중간 명령으로 오프닝 구간에 들어간 후 다음 명령이 그대로 실행된다.
        # + op_start 가 0일때 생각을 안헀음


video_len1 = "34:33"
pos1 = "13:00"
op_start1 = "00:55"
op_end1 = "02:55"
commands1 = ["next", "prev"]

video_len2 = "10:55"
pos2 = "00:05"
op_start2 = "00:15"
op_end2 = "06:55"
commands2 = ["prev", "next", "next"]

video_len3 = "07:22"
pos3 = "04:05"
op_start3 = "00:15"
op_end3 = "04:07" 
commands3 = ["next"]

# def time_norm_60(video_len_cal):
#     video_m = video_len_cal // 100
#     video_s = video_len_cal % 100

#     if video_s >= 60:
#         # 오답 원인:
#         # video_s에 먼저 % 60을 적용하면 video_s는 무조건 60 미만이 된다.
#         # 따라서 그다음 video_s // 60의 결과는 항상 0이 되어
#         # 초가 분으로 제대로 넘어가지 않는다.
#         video_s = video_s % 60
#         video_m += video_s // 60
#     return f"{video_m:02d}:{video_s:02d}"

def to_seconds(time):
    m, s = map(int, time.split(":"))
    return m * 60 + s

def to_time(time):
    m, s = divmod(time, 60)
    return f"{m:02d}:{s:02d}"

def opening_check(time, op_start, op_end):
    op_start_cal = to_seconds(op_start)
    op_end_cal = to_seconds(op_end)

    if op_start_cal <= time <= op_end_cal:
        time = op_end_cal
        
    print(f"--log_opencheck: {time}")

    return time

def solution(video_len, pos, op_start, op_end, commands):
    # video_len = 비디오길이, pos = 직전 위치 , op_start/end = 오프닝 시간, commands 순서대로 실행되는 배열
    # prev 입력시: 10초 전으로이동 (재생시간이 10초 미만일 경우 처음으로)
    # next 입력시: 10초 후로 (남은 시간이 10초 미만일경우 마지막으로)
    # 오프닝 건너뛰기: 현재 위치가 오프닝 구간 op_start <= 현재 재생위치 <= op_end 일시 끝나는 위치로

    # 각 시간들 int로 변환 (00:07 => 7) (13:03 => 1303) (06:20 => 620)
    print("-----------start------------------")
    video_len_cal = to_seconds(video_len)
    pos_cal = to_seconds(pos)

    print(f"--start_log: {pos_cal}")
    # 오프닝 skip
    pos_cal = opening_check(pos_cal, op_start, op_end)
    
    # 각 command에 따라 이동하는 함수 생성
    for i in commands:
        if i == "prev":
            if (pos_cal - 10) < 0:
                pos_cal = 0
                pos_cal = opening_check(pos_cal, op_start, op_end)
                print(f"----log: {pos_cal}")
            else:
                pos_cal -= 10
                pos_cal = opening_check(pos_cal, op_start, op_end)
                print(f"----log: {pos_cal}")
        elif i == "next":
            if (pos_cal + 10) >= video_len_cal:
                pos_cal = video_len_cal
                print(f"----log: {pos_cal}")
            else:
                pos_cal += 10
                pos_cal = opening_check(pos_cal, op_start, op_end)
                print(f"----log: {pos_cal}")

    # command입력후 open skip
    pos_cal = opening_check(pos_cal, op_start, op_end)

    answer = to_time(pos_cal)

    return answer


if __name__ == "__main__":
    test_cases = [
        (video_len1, pos1, op_start1, op_end1, commands1),
        (video_len2, pos2, op_start2, op_end2, commands2),
        (video_len3, pos3, op_start3, op_end3, commands3),
    ]

    for number, test_case in enumerate(test_cases, start=1):
        result = solution(*test_case)
        print(f"테스트 케이스 {number}: {result}")
