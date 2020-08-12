import numpy as np

m = np.linspace(2, 26, 25, dtype = 'int32')
print(m)

m = m.reshape(5,5)
print(m)

for i in range(1,4):
    for j in range(1, 4):
        m[i,j] = 0
print(m)

m = m@m
print(m)

v = m[0]
ans = 0
for i in v:
    ans += i*i
print(np.sqrt(ans))
