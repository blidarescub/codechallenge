[TOC]

#### Project description

This web application allows you to input a webpage and then fetches all the text on it, performs some natural language processing and stores all the words in a database along with their frequency of use.
After this, it generates a word cloud and displays it on the webpage. The words are scaled according to their frequency.
Lastly, it performs sentiment analysis and stores that in the database as well.
The statistics for all the urls visited is on the admin page.

The main screen of the application is accessed at http://localhost:8888
The admin page is at http://localhost:8888/admin

#### Installation

The only requirement for building this project is the installation of [Docker](https://www.docker.com/community-edition#/download "Docker").
More specifically, you need to use docker-compose.

In a terminal, navigate to and enter this folder.

```console
docker-compose -f .\docker-compose.yml up --force-recreate --no-start
```
The reason for not starting the machines is that the database takes longer to initialize than the webserver, and until the database is available the webserver will be in a restart loop. Docker does not have a viable solution for one container to wait on another and writing a workaround takes time, so it is advisable to start manually.

After the build finishes, list the machines, you should see two.
```console
docker ps --all
```

Start the database machine.
```console
docker start codechallenge_db_1
```

Wait a few  minutes, MySQL takes some time to initialize for the first time.
You can check the progress this way:
```console
docker logs -f codechallenge_db_1
```
It should say "Ready to accept connections" at the bottom.

Then start the other machine.
```console
docker start codechallenge_web_1
```
It takes only 30 seconds or so until it is ready.

Now you can access the webpage at http://localhost:8888
