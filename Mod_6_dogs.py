"""
Jacob Ezzell
July 24th 2024
ICS 4370
Description: Changing the dog table to read from a file and use a class
"""
from prettytable import PrettyTable

#dog class
class Dawg:
    def __init__ (self, name, weight):
        self.name = name
        self.weight = weight
        #weight for year 1
        self.next_weight = weight*1.15
        #weight for year 2
        self.after_weight = self.next_weight * 1.1
        
    def dump(self):
        print(f"{self.name}\t {self.weight:.2f}\t {self.next_weight:.2f}\t {self.after_weight:.2f}") 

    def dump_list(self):
        return [self.name, self.weight, round(self.next_weight,2), round(self.after_weight,2)]

if __name__ ==  "__main__":

    #prep the list that will hold the objects
    dogs = []
    #pointer to the list index of the largest dog
    bigdawg = 0
    #table object for display
    table = PrettyTable()

    #open link to the file and read in the values
    #try opening the file
    try:
        #with will auto-release the file connection
        with open('Dogs_Week6.csv', 'r') as file:
            
            #read the header to a separate variable
            data_header = file.readline()

            #split up the values of the header line, stripping white space
            header_split=data_header.strip().split(',')
            
            #find the indicies for the name and the weight
            name_index = header_split.index("Dog")
            weight_index = header_split.index("Weight")

            #read the rest of the data from the file
            for line in file:
                #split up the line
                line_split= line.split(',')
                #create a new dawg object and load in the values
                # force the weight to be a float since its a string
                dogs.append(Dawg(line_split[name_index], float(line_split[weight_index])))
                
    except(FileNotFoundError):
        print('error opening file')

    #load the names of the columns into the table object
    table.field_names=["Name", "Weight", "Next Year", "One More"]

    #loop counter
    i=0

    for dog in dogs:
        #dog.dump()
        table.add_row(dog.dump_list())
        if dog.weight > dogs[bigdawg].weight:
            bigdawg = i
        #increment loop counter
        i += 1

    table.title= 'All the Dawgs'

    print(table)
    print(f"The biggest dawg is {dogs[bigdawg].name}, who is {dogs[bigdawg].weight} lbs.")