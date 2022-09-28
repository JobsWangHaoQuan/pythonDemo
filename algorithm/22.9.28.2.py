# 阶乘的函数编写
#阶乘的定义 1! = 1   (n +1)! = (n + 1) * n!

# 使用迭代法计算阶乘
def factI(n):
    # 假设n为正整数，返回n的阶乘
    result = 1
    while n > 1:
        result = result * n
        n -= 1
    return result
# 使用递归法计算阶乘
def factR(n):
    if n == 1:
        return 1
    else:
        return n*factR(n-1)

#菲波那切数列
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def testFib(n):
    for i in range(n+1):
        print('fig of', i, '=', fib(i))

testFib(10)