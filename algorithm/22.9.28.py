# 使用二分法查找近似平方根
# 二分法的核心：找到low和high，然后不停的改变边界值知道最终找到满足条件的值
x = 81
epsilon = 0.01
numGuesses = 0
low = 0.0
high = max(1.0, x)
ans = (high + low) / 2
while abs(ans**2 - x) >= epsilon:
    numGuesses += 1
    if ans**2 < x:
        low = ans
    else:
        high = ans
    ans = (high+low)/2
print('numGuesses = ', numGuesses)
print(ans, 'is close to square root of', x)