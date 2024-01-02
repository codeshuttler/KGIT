docker ps -a | cut -d ' ' -f1 | xargs docker stop
docker ps -a | cut -d ' ' -f1 | xargs docker rm
docker rmi -f $(docker images -aq)