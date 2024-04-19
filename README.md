# Setting up a simple Kafka process using python


### PUT IN AN INTRO OF WHAT I AM DOING, THE COMPONENTS, AND THE OUTCOME.

The first step is to get a docker container up and running using the apache/kafka image.  Open a command prompt or terminal window depending on your operating system and start with the following command.

```
docker pull apache/kafka
```

Now get a local container up and running on port 9092.

```
docker run -p 9092:9092 apache/kafka:3.7.0
```
The next step is to create a topic.  We will go to execute a command inside the container in the standard installation directory. In the standard apache docker image a host of shell scripts are found that allow for the management of the kafka server.


```
docker exec -it epic_chaum /bin/bash

cd /opt/kafka/bin
ls
```

Take a second an look around at what the directory contains. It has a number of utilities that are available.

Now I am going to create a topic called transactions.  

```
./kafka-topics.sh --create --bootstrap-server localhost:9092 --topic transactions

./kafka-topics.sh --bootstrap-server localhost:9092 --list
```

This will show the creation of the topic. Now we will do a simple test using another one of the utility scripts in the bin directory. We will start an interactive session to type in messages that will be written to the kafka stream.  Execute the command and type some text next to the prompt.  When complete, ctrl-c out of the prompt 

```
./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic transactions
```

Now, lets take a look at the text by reading it as a consumer.  This command will connect to the topic and print the output to the screen.  Once this is done, we know we have a working topic and we can move into the steps of setting up a basic python process.

```
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic transactions --from-beginning
```

