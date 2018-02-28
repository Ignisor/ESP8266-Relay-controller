# ESP8266 Relay controller

Relay controller on base of [ESP8266](https://en.wikipedia.org/wiki/ESP8266) written using [MicroPython](https://docs.micropython.org/en/latest/esp8266/index.html).
In our case we use it to control magnet lock on door in our office. It has simple http server to serve web interface with button for opening the relay. And also supports push switch.

## Getting Started

### Prerequisites

- Firs of all you need a board with an ESP8266 chip (we was using NodeMCU DEVKIT on base of ESP-12 module)

- Get the MicroPython ([Downloads](http://micropython.org/download#esp8266))

- Install python requirements 
    
    `pip install -r requirements.txt`
    
- Deploy MicroPython on your board. You can do it using `esp_erase.sh` script (or you can find detailed instructions [here](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware)). Run it like this: 
    
    `sh esp_erase.sh [path_to_micropython_binary]`

### Installing

- Specify `SSID` and `PASSWORD` in `esp/data/conf.py`

- Upload files from `esp` folder to ESP board. It can be done using `esp_pus.sh` script. Just run 

    `sh esp_push.sh`
    
- Reset the board

### Connection scheme

![scheme_img](https://i.imgur.com/XRqxZUe.png)

## Built with

[MicroPython v1.9.3](https://micropython.org/)

## Authors

- German Gensetskiy - [GoWombatTeam](https://gowombat.team/)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
