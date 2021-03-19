# If the number is positive, we print an appropriate message

num = 3
p = num > 0
if p:
    print(num, "is a positive number.")

num = -1
n = num < 0
if n:
    print(num, "is a negative number.")

# Program to add natural
n = 10
sum = 0
i = 1
c = i <= n
while c:
    sum = sum + i
    i = i+1    # update counter

# print the sum
print("The sum is", sum)