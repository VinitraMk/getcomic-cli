# getcomic-cli 

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
A command line tool to download comics from readcomiconline.to

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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
A headless browser is required for this tool to automate web page interaction. The browser used here is PhantomJS. Install it using npm.  
    `sudo npm install phantomjs-prebuilt`  
***Note: Do not install phantomjs-prebuilt globally. Install it locally i.e don't use -g in the npm command***

2. **Install the package**  
    * **Using pip**  
    `sudo pip3 install getcomic`  

    * **From source**   
        1. Clone this repo and navigate to this folder in your machine.  
        2. Install the requirements for the command tool using the command  
            `sudo pip3 install -r requirements.txt`
        3. Install using the following commands now.  
            `python3 setup.py build`  
            `python3 setup.py install`  

## Running the tests

1. After installation is done, run the command `getcomic` and provide a readcomiconline url and the name of the directory where you want to 
download your files as arguments, as shown below.

![](commandss.png?raw=true)  

The directory name you specified will be created in the home folder if not already present.

## Authors

* **Vinitra Muralikrishnan** - [VinitraMk](https://github.com/VinitraMk)
See also the list of [contributors](https://github.com/VinitraMk/getcomic-cli/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


