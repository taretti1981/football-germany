# football-germany
## Build image
```docker build -t bundesliga-update-service .```
## Run image replacing config.xml
```docker run -v /localpath/config.xml:/app/config.xml -it bundesliga-update-service
