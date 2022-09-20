# Create a python script:
#
# create list of 100 random numbers from 0 to 1000
# sort list from min to max (without using sort())
# calculate average for even and odd numbers
# print both average result in console 
# Each line of code should be commented with description.
#
# Commit script to git repository and provide link as home task result.

import random as rnd
N = 100    # number of list elements
D = 1001   # upper value for interval of values: [0...D1]

rnd.seed(44)
# generate list (list comprehention) of N values, each value is random value from interval [0...D]
rand_numbers_list = [ rnd.randrange(D) for i in range(N)]

print('\n', len(rand_numbers_list), 'Source list:', rand_numbers_list)

# find minimum value in each sublist list[i:] and place it on the first place in sublist, i in [0...N-1]
for i in range(N-1):

    # find minimum value in the sublist and its index in the sublist 

    min_el = rand_numbers_list[i]

    for j, el in enumerate(rand_numbers_list[i:]):

        if el < min_el:
            min_el = el
            jj = j

    # exchange values between first position in the sublist and found minimum value in the sublist    
    
    rand_numbers_list[i], rand_numbers_list[i+jj] = rand_numbers_list[i+jj], rand_numbers_list[i]

print('\n', len(rand_numbers_list), 'Sorted list:', rand_numbers_list)

# calculate average number of even and odd values

sum_even = 0
cnt_even = 0

sum_odd = 0
cnt_odd = 0

for el in rand_numbers_list:
    if (el % 2) == 0:
        # even number
        cnt_even = cnt_even + 1
        sum_even = sum_even + el
    else:
        # odd number
        cnt_odd = cnt_odd + 1
        sum_odd = sum_odd + el

# print(f'Even numbers. N={cnt_even}, sum={sum_even}')
# print(f'Odd numbers. N={cnt_odd},  sum={sum_odd}' )

if cnt_even == 0:
    avg_even = 0
else: 
    avg_even = sum_even / cnt_even

print(f'Average of even numbers: {avg_even}')

if cnt_odd == 0:
    avg_odd = 0
else: 
    avg_odd = sum_odd / cnt_odd

print(f'Average of odd numbers: {avg_odd}')
