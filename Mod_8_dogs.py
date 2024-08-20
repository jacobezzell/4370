"""
Jacob Ezzell
Aug 6th 2024
ICS 4370
Description: Working with JSON and visualization
"""
import json
from datetime import datetime
import pygal

class Dog():
    def __init__(self, dogID, dogName, dogBreed, dogAge, ownerID):
        """Initialize the dog."""
        self.dogID = dogID
        self.dogName = dogName.title()
        self.dogBreed = dogBreed.title()
        self.dogAge = dogAge
        self.ownerID = ownerID
        self.dogWeightList = []
        self.dogDateWeighed = []

    def add_weight(self, weight, date):
        """Add information to the class"""
        self.dogWeightList.append(weight)
        self.dogDateWeighed.append(date)
    
file_path = 'dogWeights.json'
with open(file_path) as json_file:
    data_set = json.load(json_file)

dogDictionary = {}
for puppy in data_set:
    if puppy['DogID'] not in dogDictionary:
        newDog = Dog(puppy['DogID'], puppy['Dog'], puppy['DogBreed'],puppy['DogAge'], puppy['OwnerID'])
        print (puppy['Dog'] + " added")
        dogDictionary[puppy['DogID']] = newDog
    else:
        dogDictionary[puppy['DogID']].dogAge = puppy['DogAge']
    dogDictionary[puppy['DogID']].add_weight(puppy['Weight'],datetime.strptime(puppy['Date'], '%b-%d-%Y'))


#Find the min and max years to graph
minyear = 200000
maxyear = 0

for key, puppy in dogDictionary.items():
    print(puppy.dogName, puppy.dogAge, puppy.dogWeightList, puppy.dogDateWeighed)
    #find the date ranges
    for year in puppy.dogDateWeighed:
        print(year.year)
        if year.year < minyear:
            minyear = year.year
        if year.year > maxyear:
            maxyear = year.year

print(f"Years {minyear} to {maxyear}")  

#prep the chart
line_chart = pygal.Line()
line_chart.title = 'Dog Weights per year'
line_chart.x_labels = map(str, range(minyear, maxyear))

#make a line for each dog....

#for each dog in the dictionary
for key, puppy in dogDictionary.items():
    #blank list to hold the weights for this dog, including placeholders
    weights_to_graph = []

    #create a list of weights each year in the range
    for year in range(minyear, maxyear+1):
        #is this year in the list for this dog?
        found_it = False
        #look through each year in the dog's list of years weights were taken and see if the current year is there
        for count, dt in enumerate(puppy.dogDateWeighed):
            if dt.year == year:
                #if it is, mark the spot
                found_it = True
                found_it_at = count
        if found_it:
            #if we found the right year, use the same pointer to save the corresponding weight to the list
            weights_to_graph.append(puppy.dogWeightList[found_it_at])
        else:
            #if we didn't find it, stick a blank placeholder into the list for that year.
            weights_to_graph.append(None)

    #add the line chart object for this dog and the list of weights
    line_chart.add(puppy.dogName, weights_to_graph)

#save the file
line_chart.render_to_file('dogs.svg')