def solve(l):
    n = len(l)
    
    dp = [[[float('inf')] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
    
    dp[0][n][n] = 0

    for i in range(n):
        for last_black in range(n + 1):
            for last_white in range(n + 1):
                if dp[i][last_black][last_white] == float('inf'):
                    continue

                if last_black == n or l[i] > l[last_black]:
                    dp[i + 1][i][last_white] = min(dp[i + 1][i][last_white], dp[i][last_black][last_white])

                if last_white == n or l[i] < l[last_white]:
                    dp[i + 1][last_black][i] = min(dp[i + 1][last_black][i], dp[i][last_black][last_white])

                dp[i + 1][last_black][last_white] = min(dp[i + 1][last_black][last_white], dp[i][last_black][last_white] + 1)

    result = float('inf')
    for last_black in range(n + 1):
        for last_white in range(n + 1):
            result = min(result, dp[n][last_black][last_white])
    
    return result

while True:
    n = int(input())
    if n == -1:
        break
    l = list(map(int, input().split()))
    print(solve(l))
