# Dimka - Binance bot

[![Build Status][testing-image]][testing-link]
[![Coverage Status][coverage-image]][coverage-link]
[![License][license-image]][license-link]

This is an experimental bot for auto trading the Binance exchange.


**Be very careful when using this bot. Potentially it can loose your money.**
**Use this bot at your own risk.**


## Table Of Contents

- [How it looks?](#how-it-looks)
- [How it works?](#how-it-works)
- [Installation with Docker](#installation-with-docker)
- [Login to docker container](#login-to-docker-container)
- [Running the bot](#running-the-bot)
- [Run tests](#run-tests)
- [Contributing](#contributing)
- [Donate & Thanks to developer](#donate)
- [Disclaimer](#disclaimer)


## How it looks?

![How it looks?](/i/img_1.png?raw=true "Optional Title")


## How it works? 


## Installation with Docker

Install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

```
    cp /{proj_path}/Dockerfile.dist /{proj_path}/Dockerfile 
    cp /{proj_path}/docker-compose.yml.dist /{proj_path}/docker-compose.yml 
```

Build and run docker container

```
    docker-compose build 
    docker-compose up -d 
```

Inside [conf](/conf/) you can find configuration examples.
Copy this files and create your own configuration.
* **[/conf/conf.yaml.dist](/conf/conf.yaml.dist)** - this file contains bot configuration parameters.
Change them for your own needs.  

**Important!!!** Each bot instance should have his own:
* configuration file
* database (database file defined in configuration file)
* Binance account  

*Don't share this data between separate bot instances. Otherwise the behavior of the bot can be unpredictable.*


## Login to docker container
```bash
    docker exec  -ti -e COLUMNS="`tput cols`" -e LINES="`tput lines`" dimka-binance  bash
```

## Running the bot
To see help about bot additional parameters use command:
```bash
    python 3-step-bot.py --help
```

Running the bot:
```bash
    python 3-step-bot.py /var/www/conf/conf.yaml. --step=3 --iters=10 --high-diff=50 --debug
```


## Run tests
```bash

    python -m unittest discover dimka-binance
```


## Contributing
To create new endpoint - [create issue](https://github.com/madmis/dimka-binance/issues/new) 
or [create pull request](https://github.com/madmis/dimka-binance/compare)


## Donate

If you find the bot useful and would like to donate, you can send some coins here:

```
BTC 17RaWy3SwvwhrMnakaMARX4N2vh5ukxpiz
BCH: qpsx260laq6wj4s99052nuy063v7j0sxsqxluur84z
ETH: 0x387D91F008dB992c7DAd9be8493dfA68E565706E
XRP: rpoi4dWSbEyQP2xmpsNMxCk2g2n5QvVSmM
Waves: 3PPXpTagbQCSXYZ3Y5h6vuFPj6RxHbnapmE
BTS: madmis-1
```

## Disclaimer

I am not responsible for anything done with this bot. 
You use it at your own risk. 
There are no warranties or guarantees expressed or implied. 
You assume all responsibility and liability.


[testing-link]: https://travis-ci.org/madmis/dimka-binance
[testing-image]: https://travis-ci.org/madmis/dimka-binance.svg?branch=master

[coverage-link]: https://coveralls.io/github/madmis/dimka-binance?branch=master
[coverage-image]: https://coveralls.io/repos/github/madmis/dimka-binance/badge.svg?branch=master

[license-image]: https://img.shields.io/github/license/madmis/dimka-binance.svg
[license-link]: https://github.com/madmis/dimka-binance/blob/master/License.txt

