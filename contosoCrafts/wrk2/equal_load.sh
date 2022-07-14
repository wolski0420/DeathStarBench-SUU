#!/bin/bash


for i in {1..100..1}
do
  ./wrk -t 8 -c 8 -d 15 -L -s ./scripts/contosoCrafts/get_all.lua http://localhost:9090/Products -R 2000
done

