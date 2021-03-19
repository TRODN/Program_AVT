a = 1
b = 2
c = 3
d = 4
p = a < b
q = b < c
r = c < d
while p :
  while q :
    print(r)
  a = (a + 1)
  p = a < b
