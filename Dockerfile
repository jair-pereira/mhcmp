FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base python3.8 python3-pip python3-setuptools python3-dev
ENV PYTHONPATH "${PYTHONPATH}:/home"
WORKDIR /home

# copying requirements
COPY ./docker/requirements.txt ./
COPY ./docker/requirements.r ./

# installing requirements
RUN pip3 install --no-cache-dir -r requirements.txt
RUN Rscript requirements.r

# copying local github rep
RUN mkdir mhcmp
COPY . /home/mhcmp
WORKDIR /home/mhcmp

# install coco
RUN python3 ./coco/do.py run-python

# irace setup
RUN chmod +x ./irace/target-runner_pso.sh
RUN chmod +x ./irace/target-runner_ata.sh
RUN chmod +x ./irace/target-runner_gsa.sh
RUN chmod +x ./irace/target-runner_rio.sh
RUN chmod +x ./irace/target-runner_ffa.sh
RUN chmod +x ./irace/target-runner_saa.sh
RUN chmod +x ./irace/target-runner_de.sh

# run exp
# RUN chmod +x test.sh
# CMD ["./test.sh"]
