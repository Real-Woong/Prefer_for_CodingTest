# 프로그래머스 468370 - 중요한 단어를 스포 방지

m = "here is muzi here is a secret message"
s = [[0, 3], [23, 28]]

m1 = "my phone number is 01012345678 and may i have your phone number"
s1 = [[5, 5], [25, 28], [34, 40], [53, 59]]

def solution(message, spoiler_ranges):
    # 여기에 풀이를 작성하세요.
    # message: 문자열
    # spoiler_ranges: [[start, end], ...]

    # 일단 단어를 나눈다
    m_split = message.split()

    # SPOIL, UN-SPOIL 단어로 나눈다
    cursor = 0
    spoil_w = []
    unspoil_w = []
    for word in m_split:
        start = message.find(word, cursor) # 단어 하나의 시작점을 지어
        end = start + len(word) - 1 # 그 시작점에서 단어의 끝지점 받아옴
        cursor = end + 1 # 다음 단어로 이동

        # 단어의 알파벳 하나라도 spoiled ranges에 포함되지 않으면 is_unspoiled = True
        is_unspoiled = all (end < s_start or start > s_end for s_start, s_end in spoiler_ranges)

        if is_unspoiled:
            unspoil_w.append(word)
        else:
            spoil_w.append(word)


    

    answer = set(spoil_w) - set(unspoil_w)
        
    print(f"spoiling: {spoil_w}")
    print(f"unspoling:{unspoil_w}")
    print(f"answer:{answer}")

    return len(answer)

print(solution(m, s))
print('\n')
print(solution(m1, s1))



# def run_test(number, message, spoiler_ranges, expected):
#     result = solution(message, spoiler_ranges)
#     passed = result == expected

#     print(f"테스트 {number}")
#     print(f"message: {message!r}")
#     print(f"spoiler_ranges: {spoiler_ranges}")
#     print(f"내 결과: {result}")
#     print(f"기대값: {expected}")
#     print(f"통과 여부: {passed}")
#     print("-" * 45)


# if __name__ == "__main__":
#     test_cases = [
#         (
#             "here is muzi here is a secret message",
#             [[0, 3], [23, 28]],
#             1,
#         ),
#         (
#             "my phone number is 01012345678 and may i have your phone number",
#             [[5, 5], [25, 28], [34, 40], [53, 59]],
#             4,
#         ),
#     ]

    # for number, (message, spoiler_ranges, expected) in enumerate(test_cases, start=1):
    #     run_test(number, message, spoiler_ranges, expected)


# [오답 정리]
#
# 1. spoiler_ranges를 하나씩 확인할 때마다 spoil_w 또는 unspoil_w에 word를 append했다.
#    범위가 4개면 단어 하나가 최대 4번 추가되어 중복이 발생했다.
#    또한 한 범위와는 겹치고 다른 범위와는 겹치지 않으면 두 리스트에 모두 들어갈 수 있었다.
#    -> 모든 범위를 확인한 뒤 단어당 한 번만 분류해야 한다.
#
# 2. any(범위와 겹치지 않는 조건)으로 is_unspoiled를 구했다.
#    any는 하나라도 True면 True이므로, 어느 한 범위와만 겹치지 않아도 unspoiled가 되어버렸다.
#    -> unspoiled는 모든 스포일러 범위와 겹치지 않아야 하므로 all(겹치지 않는 조건)을 사용한다.
#
# 3. spoil_w를 for문으로 순회하면서 spoil_w.remove(i)를 사용했다.
#    순회 중인 리스트의 크기와 인덱스가 바뀌어 다음 원소를 건너뛸 수 있고,
#    remove()는 같은 값이 여러 개여도 첫 번째 값 하나만 삭제한다.
#    -> 원본 리스트를 순회하며 수정하지 말고, set의 차집합을 사용한다.
#
# 4. message.split()만 사용하면 각 단어의 원래 문자열 인덱스가 사라진다.
#    -> cursor와 message.find(word, cursor)로 각 단어의 시작 위치를 찾는다.
#       끝 인덱스는 범위에 포함되므로 start + len(word) - 1로 계산한다.
