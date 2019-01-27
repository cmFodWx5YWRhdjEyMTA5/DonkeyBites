#!/bin/bash
#file="downloaded_jsons_before_filter/1_2019-01-14.json"

declare -a pollutants=("co" "no2" "o3" "pm10" "pm25" "so2")

LIST_OF_FILES=$(ls -lat downloaded_jsons_before_filter | awk '{ print $9}')

rm -rf final_csv_files
mkdir final_csv_files

#less $file | jq  .data[0].indexes.baqi.display_name


echo "hour,co,no2,o3,pm10,pm25,so2" > final_csv_files/1_2019-01-14.csv

for file in downloaded_jsons_before_filter/*
do
  filename=$(basename -- "$file")
  echo 111 ----  $filename
  filename="${filename%.*}"
  echo 222 ----  $filename 
  echo "File name is " $file "will be filtered and converted to" $filename ".csv"
  for hour in {0..23}
  do
    LINE="$hour,"
    for pollutant in "${pollutants[@]}"
    do
        LINE="$LINE$(less $file | jq  .data[$hour].pollutants.$pollutant.concentration.value |  tr -d '"'),"
    done
    echo $LINE >> final_csv_files/$filename.csv
  done
done




