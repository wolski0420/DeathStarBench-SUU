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
or by command: 

```bash
docker pull intel/oneapi-vtune:devel-ubuntu20.04
```

NOTE: it can be necessary to run this command with ```sudo```.

### Step by step

* Start docker container with vtune:

```bash
docker run --pid=host --cap-add=SYS_ADMIN --cap-add=SYS_PTRACE -it --rm <vtune image name/id>
```

NOTE: it may be necessary to run this command with ```sudo```.

* Start collecting data from microservice from vtune CLI with command

```bash
vtune -collect uarch-exploration -target-ports=<port of service container to profile> -d \<duration in sec>
```

* Generate need data in csv format from vtune CLI with command:

```bash
vtune -report summary -result-dir <generated dir with results> -format=csv -report-output <output path with name>
```

* Copy output to host with:

```bash
docker cp <container name/id>:<path to results file in container> <output path on host>
```

* Delete not needed data and collect all data to one file with prepared python script

```bash
python generate_results.py <absoulute directory path with csv files generated with vtune> results.csv
```
NOTE: 
The above script generates result directory with results.csv file that displays 5 metrics (Bad Speculation, Front-End bound, Back-End bound, Retiring, and IPC) for every microservice that vTune report was generated.
That script was created to select the data necessary to generate figure 10 from the [DeathStarBench paper](https://www.csl.cornell.edu/~delimitrou/papers/2019.asplos.microservices.pdf).


### Alternate method

You can always run special python script to automate this process. 
You only need to do following steps:

1. Run one of prepared applications (this process is described in
appropriate application README).
2. Start our workload prepared in wrk2 (this process is also described
in appropriate application README).
3. Run our script for automation:

```bash
./vtune-profiler.sh
```

After execution, you should be able to see some generated results file
in csv format. 

## License & Copyright 

DeathStarBench is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 2.

DeathStarBench is being developed by the [SAIL group](http://sail.ece.cornell.edu/) at Cornell University. 

## Publications

More details on the applications and a characterization of their behavior can be found at ["An Open-Source Benchmark Suite for Microservices and Their Hardware-Software Implications for Cloud and Edge Systems"](http://www.csl.cornell.edu/~delimitrou/papers/2019.asplos.microservices.pdf), Y. Gan et al., ASPLOS 2019. 

If you use this benchmark suite in your work, we ask that you please cite the paper above. 


## Beta-testing

If you are interested in joining the beta-testing group for DeathStarBench, send us an email at: <microservices-bench-L@list.cornell.edu>
