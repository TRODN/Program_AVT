#Function call
def findDivisible(numberList):
    print("Given list is ", numberList)
    print("Divisible of 5 in a list")
    for num in numberList:
        if (num % 5 == 0):
            print(num)

funcall = findDivisible(numList)

#Test if first and last number of a list is same
numList = [10, 20, 30, 40, 10]
print("Given list is ", numberList)
firstElement = numberList[0]
lastElement = numberList[-1]
t = firstElement == lastElement
if t:
    print(True)
else:
    print(False)

#Calculate income tax for the given income
income = 45000
taxPayable = 0
print("Given income", income)

tax = income <= 10000
if tax:
    taxPayable = 0
else:
    # first 10,000
    taxPayable = 0

    # next 10,000
    taxPayable = 10000 * 10 / 100

    # remaining
    taxPayable += (income - 20000) * 20 / 100

print("Total tax to pay is", taxPayable)
