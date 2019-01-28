import csv
import os
import shutil
import fileinput
import urllib.request
import urllib.parse
import threading


class Locations():
    def __init__(self, filename):
        with open(filename, "r") as f_input:
            csv_input = csv.reader(f_input)
            self.details = list(csv_input)

    def get_col_row(self, row, col):
        return self.details[row-1][col-1]



def applyValues (min_value, max_value):
    data = Locations("points.csv")

    for i in range(int(min_value), int(max_value), 1): #299
        current = i + 1
        print (current)
        current_lat = data.get_col_row(current,2)
        current_lon = data.get_col_row(current,3)
        print("Row {row} current_lat is {lat}, current_lon is {lon}".format(row=i, lat=current_lat, lon=current_lon))
        
        old_name = "requests.txt.orig.templated"
        new_name =  directory + "/requests_applied_" + str(i) + ".txt"
        shutil.copy(old_name, new_name)
        for line in fileinput.input([new_name], inplace=True):
            print(line.replace('xxxxLATxxxx', current_lat), end='')
        for line in fileinput.input([new_name], inplace=True):
            print(line.replace('xxxxLONxxxx', current_lon), end='')

        with open(new_name, 'rU') as urls:
            for url in urls:
                print (url)
                par = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                date = par['start_datetime'][0]
                date = date[:-9]
                print ("Date is " + date)
                print ("Row is " + str(i) )
                json_file_name = directory_json + "/" + str(i) + "_" + date + ".json"
                # Download the file from `url` and save it locally under `file_name`:
                try:
                    with urllib.request.urlopen(url) as response, open(json_file_name, 'wb') as out_file:
                        datafile = response.read() # a `bytes` object
                        out_file.write(datafile)
                except urllib.error.HTTPError as e:
                    print("Error: ", e)

if __name__ == "__main__":
    print ("Start apply Values to URLs and download them")

    threads = []
    ranges = dict({'1': '1-15', '2': '16-30', '3': '31-45', '4': '46-50', '5': '51-65', '6': '66-80', '7': '81-95', '8': '96-110', '9': '111-115', '10': '116-130', '11': '131-145', '12': '146-160', '13': '161-175', '14': '176-190', '15': '191-205', '16': '206-220', '17': '221-235', '18': '236-250', '19': '251-265', '20': '266-280', '21': '281-299',})

    directory="requests_with_applied_values"
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    directory_json="downloaded_jsons_before_filter"
    if os.path.exists(directory_json):
        shutil.rmtree(directory_json)
    os.makedirs(directory_json)
    
    for i in range(1, 22):
        min_value = ranges[str(i)].split("-")[0]
        max_value = ranges[str(i)].split("-")[1]
        t = threading.Thread(target=applyValues,args=(min_value, max_value))
        threads.append(t)
        t.start()
        print ("===== Fire Thread for - [" + str(i) + "]")
        # time.sleep(15)

    for t in threads:
        t.join()
