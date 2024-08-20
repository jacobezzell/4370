"""
Jacob Ezzell
July 8th 2024
ICS 4370
Description: Adding a function to the dog table
"""

def get_bigger(weight, next_year, year_after):
    """uses the weight passed to it, and pointers to two lists that you are adding values to"""
    next_weight = weight*1.15
    next_year.append(round(next_weight, 2))
    after_weight = next_weight * 1.1
    year_after.append(round(after_weight, 2))

#prep the lists
dogs = ['Max', 'Lucy', 'Wolf', 'Rex', 'Buffy']
weights = [35.4, 60.2, 12.4, 40.3, 43.1]
next_year = []
year_after = []

#formatting line length
linelength = 45

#print the header
print('-' * linelength)
print('Dawgs and their weights:')
print('-' * linelength)

#i is my iterator variable
i = 0
#maxweight will be a pointer to the biggest Dawg
maxweight = 0

#for each dog in the list
for dog in dogs:
    get_bigger(weights[i], next_year, year_after)
    #print the pair
    print(f"|{dogs[i]:^10}|{weights[i]:^10}|{next_year[i]:^10}|{year_after[i]:^10}|")
    #test if the weight is the biggest one yet
    if(weights[i] > weights[maxweight]):
        #if not, assign the pointer the new max position
        maxweight = i

    #last step, increment the iterator
    i +=1

#print out the footer with the biggest values
print('-' * linelength)
print(f"The biggest Dawg is {dogs[maxweight]} \nwho is {weights[maxweight]} lbs.")
print('-' * linelength)

