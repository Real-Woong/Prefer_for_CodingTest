#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

def find_gcd(a, b):
    if b == 0:
        return a
    return find_gcd(b, a % b)   

def find_lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return (a * b) // find_gcd(a, b)

def lcm(n):
    if not n:
        return 0
    results = n[0]
    for numbers in n[1:]:
        results = find_lcm(results, numbers)
    return results


def is_yellow(signal, t):
    g, y, r = signal
    period = g + y + r
    pos = (t-1) % period
    return g <= pos < g + y
    # g > pos면 초록, g + y <= pos면 빨강 그 외는 기본값인 노랑
    
def solution(signals):
    # 반복되는 최소 주기 계산 (또는 최소 주기 구하기)
    arr = []
  
    for i in signals:
        x = sum(i)
        arr.append(x)
        
    hall_period = lcm(arr)
            
    # 주기 계산을 통해 특정 시간에 신호등 불이 들어오는지 찾기
    time = 1
    for  time in range(1 , hall_period + 1):             
        if all(is_yellow(per_light, time) for per_light in signals):
            return time
    else: return -1


if __name__ == "__main__":
    test_cases = [
        ([[2, 1, 2], [5, 1, 1]], 13),
        ([[2, 3, 2], [3, 1, 3], [2, 1, 1]], 11),
        ([[3, 3, 3], [5, 4, 2], [2, 1, 2]], 193),
        ([[1, 1, 4], [2, 1, 3], [3, 1, 2], [4, 1, 1]], -1),
    ]

    for number, (signals, expected) in enumerate(test_cases, start=1):
        result = solution(signals)

        print(f"테스트 케이스 {number}")
        print(f"신호등: {signals}")
        print(f"실행 결과: {result}")
        print(f"기대 결과: {expected}")
        print(f"일치 여부: {result == expected}")
        print("-" * 30)