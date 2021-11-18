#!/bin/bash

csv_filename="PPML '21 Organizer assignements - PosterAreas.csv"

poster_list=`ls ppml21-paper*-poster.pdf`

for i in $poster_list; do
    poster_number=$(cut -f2  -d '-' <<< "$i" | sed 's/[^0-9]*//g')
    area_number=$(grep ",#$poster_number," "$csv_filename" | cut -f6 -d ',')
    echo "$poster_number-->$area_number"
    convert -flatten -density 150 $i -resize 5120x2880 $area_number.png;
    convert -flatten $i -resize 512x288 "$area_number"_thumb.png;
done

