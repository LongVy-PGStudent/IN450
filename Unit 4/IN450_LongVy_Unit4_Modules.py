# Long Vy
# IN450 - Unit 4
# 4/21/2026

"""
References

Azkia, D. (2025, April 29). Bug tracking management for QA teams: Let’s get it right | by Devy Azkia | Medium. Medium. https://devyazkia.medium.com/bug-tracking-management-for-qa-teams-lets-get-it-right-b4f3e7cfe129 
GeeksforGeeks. (2025, July 15). Python unittest - assertequal() function. https://www.geeksforgeeks.org/python/python-unittest-assertequal-function/
Obregon, A. (2024, May 31). Writing unit tests in python with unittest. https://medium.com/@AlexanderObregon/writing-unit-tests-in-python-with-unittest-0a23463d93dd 
Qiang, B. (2016, October 27). The absolute beginner’s guide to test driven development, with a practical example | by Beth Qiang | Medium. Medium. https://medium.com/@bethqiang/the-absolute-beginners-guide-to-test-driven-development-with-a-practical-example-c39e73a11631 

"""



def example1(array_of_ints, n):

    currmin = 100
    for i in range(n):
        if array_of_ints[i] < currmin:
            currmin = array_of_ints[i]
    return currmin
 
 
def example2(array_of_ints):

    for i in range(100):
        print(array_of_ints[i])
 
 
def example3(array_of_ints):

    a = 10
    b = 5
    found = False
    for i in range(len(array_of_ints)):
        if a == array_of_ints[i]:
            print("The value of a was found in int array.")
            found = True
        elif b == array_of_ints[i]:
            # Note: original pseudocode prints "value of a" here too — preserved as-is
            print("The value of a was found in int array.")
            found = True
    if not found:
        print("None of the search values were found.")