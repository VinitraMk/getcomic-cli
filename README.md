# getcomic-cli 

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
A command line tool to download comics from readcomiconline.to

## Features
* Download comics from readcomiconline.to by providing the url of a single issue of a comic 
* Download the entire series of a particular comic by providing the url of a comic series

## Getting Started

### Supported OS
Ubuntu

### Prerequisites

```
  1. Python3
  2. Node
  3. pip3
```

### Installation

1. **Install a headless browser**    
A headless browser is required for this tool to automate web page interaction. The browser used here is Chrome. 
    1. Install the latest version of chrome browser in your machine. Follow this [link](https://gist.github.com/mrtns/78d15e3263b2f6a231fe) 
    for the same.
    2. To upgrade google-chrome in Ubuntu 16.04 LTS, run the following command.  
    `sudo apt-get --only-upgrade install google-chrome-stable`
    3. Now you need a Chrome Driver. Download the latest release of ChromeDriver from this [site](https://sites.google.com/a/chromium.org/chromedriver/home)
    4. Navigate to the folder where you downloaded Chrome Driver and extract it's contents. Install the Chrome Driver by running the following commands.  
    ```
    sudo chmod +x chromedriver
    sudo mv -f chromedriver /usr/local/share/chromedriver  
    sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
    sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
    ```
2. **Install the package**  
    * **Using pip**  
    `sudo pip3 install getcomic`  

    * **From source**   
        1. Clone this repo and navigate to this folder in your machine.  
        2. Install using the following commands now.   
            `python3 setup.py build`  
            `python3 setup.py install`  

## Usage 

1. After installation is done, run the command `getcomic` and provide a readcomiconline url and the name of the directory where you want to 
download your files as arguments, as shown below.

![](https://i.imgur.com/Wl8iNDP.png)  

The directory name you specified will be created in the home folder if not already present.

![](https://i.imgur.com/FPDnwsI.gif)


## Authors

* **Vinitra Muralikrishnan** - [VinitraMk](https://github.com/VinitraMk)
See also the list of [contributors](https://github.com/VinitraMk/getcomic-cli/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


