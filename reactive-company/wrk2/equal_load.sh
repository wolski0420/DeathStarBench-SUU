#!/bin/bash


for i in {1..50..1}
do
  ./wrk -t 8 -c 8 -d 15 -L -s ./scripts/reactive-company/get_all_blogposts_stream.lua http://localhost:8080/stream -R 2000
done

