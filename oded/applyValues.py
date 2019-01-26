import csv

class ContactDetails():
    def __init__(self, filename):
        with open(filename, "r") as f_input:
            csv_input = csv.reader(f_input)
            self.details = list(csv_input)

    def get_col_row(self, col, row):
        return self.details[row-1][col-1]

data = ContactDetails("points.csv")


for i in range(1, 299):
    current_lat = data.get_col_row(2, i+1)
    current_lon = data.get_col_row(3, i+1)
    print("Row {row} current_lat is {lat}, current_lon is {lon}".format(row=i, lat=current_lat, lon=current_lon))

