# Python program to check if the number is an Armstrong number or not

# take input from the user
num = int(input("Enter a number: "))

# initialize sum
total = 0

# find the sum of the cube of each digit
temp = num
t = temp > 0
while t:
   digit = temp % 10
   total += digit ** 3
   temp //= 10

# display the result
t = num == total
if t:
   print(num,"is an Armstrong number")
else:
   print(num,"is not an Armstrong number")
