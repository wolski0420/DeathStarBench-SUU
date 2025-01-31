import os
import sys
import yaml

params = sys.argv
script_name = "vtune-profiler.py"

# validating parameters
if script_name in sys.argv:
    params.remove(script_name)

# checking number of useful parameters
if len(params) < 2:
    raise Exception("Wrong number of parameters. Please provide: python3 vtune-profiler.py "
                    "<application_name> <docker-compose files ...>")

print(f"*** RUNNING VTUNE PROFILER WITH ARGUMENTS: application_name={params[0]} docker-compose_files={params[1:]} ***")

# running container with vtune
print("*** RUNNING VTUNE CONTAINER ***")
os.system("docker run --pid=host --cap-add=SYS_ADMIN --cap-add=SYS_PTRACE -it -d --name vtune-container "
          "intel/oneapi-vtune:devel-ubuntu20.04")

# reading all applications from docker-compose and their ports
print("*** TAKING SERVICES WITH PORTS FROM DOCKER-COMPOSES ***")
filtered_dc = dict()
for docker_compose_file in params[1:]:
    file = open(docker_compose_file, "r")
    dc = yaml.load(file, Loader=yaml.FullLoader)

    # taking only these services which have ports and they are not monitoring type service
    # then mapping to "<service_name>: <first assigned port>"
    filtered_dc = dict((k, v["ports"][0].split(":")[0]) for k, v in dc["services"].items()
                       if ("ports" in v and "zipkin" not in k and "jaeger" not in k))

# running vtune on every found service, then summarizing results and copying from container to host
print("*** EXECUTING VTUNE FOR APPLICATION ***")
index = 0
for name, port in filtered_dc.items():
    index_str = "{:03d}".format(index)

    print(f"****** VTUNE COLLECT {name=} {port=} ******")
    os.system(f"docker exec vtune-container vtune -collect uarch-exploration -target-ports={port} -d 60")

    print(f"****** VTUNE COLLECT {name=} {port=} ******")
    os.system(f"docker exec vtune-container vtune -report summary -result-dir r{index_str}ue -format=csv "
              f"-report-output /home/{params[0]}-{name}.csv")

    print(f"****** CP RESULTS {name=} {port=} ******")
    os.system(f"docker cp vtune-container:/home/{params[0]}-{name}.csv .")

    index += 1

# stopping vtune container
print("****** STOPPING CONTAINER ******")
os.system("docker stop vtune-container")
os.system("docker container rm vtune-container")
