#!/bin/bash
#file="downloaded_jsons_before_filter/1_2019-01-14.json"

apt install bc

declare -a pollutants=("co" "no2" "o3" "pm10" "pm25" "so2")

LIST_OF_FILES=$(ls -lat downloaded_jsons_before_filter | awk '{ print $9}')

rm -rf final_csv_files
mkdir final_csv_files

#less $file | jq  .data[0].indexes.baqi.display_name



for file in downloaded_jsons_before_filter/*
do
  filename=$(basename -- "$file")
  filename="${filename%.*}"
  echo "File name is " $file "will be filtered and converted to" $filename ".csv"
  echo "HOUR,BreezoMeter AQI,CO,NO2,O3,PM10,PM25,SO2" > final_csv_files/$filename.csv

  for hour in {0..23}
  do
    LINE="$hour,"
    LINE="$LINE$(less $file | jq .data[$hour].indexes.baqi.aqi_display | tr -d '"'),"

    for pollutant in "${pollutants[@]}"
    do
      case $pollutant in
      "co")
          VALUE=$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"')
          VALUE=$(echo "$VALUE * 1.145" | bc -l)
          LINE="$LINE$VALUE,"
          ;;
      "no2")
          VALUE=$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"')
          VALUE=$(echo "$VALUE * 1.88" | bc -l)
          LINE="$LINE$VALUE,"
          ;;
      "o3")
          VALUE=$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"')
          VALUE=$(echo "$VALUE * 2" | bc -l)
          LINE="$LINE$VALUE,"
          ;;
      "pm10")
          VALUE=$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"')
          VALUE=$(echo "$VALUE * 1" | bc -l)
          LINE="$LINE$VALUE,"
          ;;
      "pm25")
          VALUE=$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"')
          VALUE=$(echo "$VALUE * 1" | bc -l)
          LINE="$LINE$VALUE,"
          ;;
      "so2")
          VALUE=$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"')
          VALUE=$(echo "$VALUE * 2.62" | bc -l)
          LINE="$LINE$VALUE,"
          ;;      
      esac
      shift        
      LINE="$LINE$(less $file | jq .data[$hour].pollutants.$pollutant.concentration.value | tr -d '"'),"
    done
    echo $LINE >> final_csv_files/$filename.csv
  done
done




