"""
Jacob Ezzell
June 19th 2024
ICS 4370
Description: This loops over a list and finds the largest value
"""

#prep the lists
dogs = ['Max', 'Lucy', 'Wolf', 'Rex', 'Buffy']
weights = [35.4, 60.2, 12.4, 40.3, 43.1]

#formatting line length
linelength = 30

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
    #print the pair
    print(f"|{dogs[i]}\t|\t{weights[i]}|")
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

