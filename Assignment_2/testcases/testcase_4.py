#Total number of digits in a number

num = 75869
count = 0
t = num != 0
while t:
    num //= 10
    count+= 1
print("Total digits are: ", count)


#Display Fibonacci series up to 10 terms
terms = 10
# first two terms
num1, num2 = 0, 1
count = 0

print("Fibonacci sequence:")
c = count < terms
while c:
    print(num1, end="  ")
    temp = num1 + num2
    # update values
    num1 = num2
    num2 = temp
    count += 1

