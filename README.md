# DeathStarBench

Open-source benchmark suite for cloud microservices. DeathStarBench includes five end-to-end services, four for cloud systems, and one for cloud-edge systems running on drone swarms. 

## End-to-end Services <img src="microservices_bundle4.png" alt="suite-icon" width="40"/>

* Social Network (released)
* Media Service (released)
* Hotel Reservation (released)
* E-commerce site (in progress)
* Banking System (in progress)
* Drone coordination system (in progress)
* ContosoCrafts (in progress)
* Reactive-Company (in progress)

## Cycle breakdown and IPC analisys 

To collect data about cycle breakdown and IPC for each microservice in End-to-end Service docker image of intel vtune is needed. 

Get docker image from https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler-download.html?operatingsystem=linux&distributions=docker \
or by command docker pull intel/vtune-profiler 

### Step by step

* Start docker container with vtune \
sudo docker run --pid=host --cap-add=SYS_ADMIN --cap-add=SYS_PTRACE -it --rm \<vtune image id>
* Start collecting data from microservice from vtune CLI with command \
vtune -collect systerm-overview sampling-mode=hw -target-process \<port of microservice> -d \<duration in sec>
* Generate need data in csv format from vtune CLI with command\ 
vtune -report top-down -result-dir \<TODO skad> -format=csv -report-output \<path to output file>
* Copy output to host with\
docker cp \<Container:path to results> \<output path>
* Delete not needed data and collect all data to one file with prepared python script\
TODO

Output file contains cycle breakdowns and IPC analisys for each microserivce.



## License & Copyright 

DeathStarBench is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 2.

DeathStarBench is being developed by the [SAIL group](http://sail.ece.cornell.edu/) at Cornell University. 

## Publications

More details on the applications and a characterization of their behavior can be found at ["An Open-Source Benchmark Suite for Microservices and Their Hardware-Software Implications for Cloud and Edge Systems"](http://www.csl.cornell.edu/~delimitrou/papers/2019.asplos.microservices.pdf), Y. Gan et al., ASPLOS 2019. 

If you use this benchmark suite in your work, we ask that you please cite the paper above. 


## Beta-testing

If you are interested in joining the beta-testing group for DeathStarBench, send us an email at: <microservices-bench-L@list.cornell.edu>
