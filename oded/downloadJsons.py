import urllib.request
url="https://github.com/doronshai/DonkeyBites/blob/master/oded/test_10.json"
file_name=url[url.rfind("/")+1:]
print (file_name)

urls = ("https://github.com/doronshai/DonkeyBites/blob/master/oded/test_1.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_2.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_3.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_4.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_5.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_6.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_7.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_8.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_9.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_10.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_11.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_12.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_13.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_14.json", "https://github.com/doronshai/DonkeyBites/blob/master/oded/test_15.json")


# Download the file from `url` and save it locally under `file_name`:
with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read() # a `bytes` object
    out_file.write(data)
