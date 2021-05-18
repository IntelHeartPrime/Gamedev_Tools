# Filename : test.py
# author by : www.runoob.com

# 二次方程式 ax**2 + bx + c = 0
# a、b、c 用户提供，为实数，a ≠ 0

# 导入 cmath(复杂数学运算) 模块


import cmath

p0_list = [0,0.05,0.1,0.15,0.2,0.25,0.3]

for x in p0_list:
    zz = 1 - x
    a = -2 * zz
    b = 3*zz + x*zz
    c = x-zz*x-1

    # 计算
    d = (b ** 2) - (4 * a * c)

    # 两种求解方式
    sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)

    print('结果为 {0} 和 {1}'.format(sol1, sol2))

# 计算期望
p0 = 0.05
p1 = 0.45
p2 = 0.85

# 计算期望
result = p0 + (1-p0)*p1 + (1-p0)*(1-p1)*p2

print(result)
