# candlestick-screener
web-based technical screener for candlestick patterns using TA-Lib, Python, and Flask

## Video Tutorials for this repository:

* Candlestick Pattern Recognition - https://www.youtube.com/watch?v=QGkf2-caXmc
* Building a Web-based Technical Screener - https://www.youtube.com/watch?v=OhvQN_yIgCo
* Finding Breakouts - https://www.youtube.com/watch?v=exGuyBnhN_8

## Building Docker Image
```
docker build -t candlestick .
docker container run --publish 80:80 --detach candlestick
```
