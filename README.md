# linkedbot

Python Selenium Bot for linkedin crawling

# install

get libraries :
https://github.com/stephlaurrain/pylibs
copy them into the application root directory (dir is "utils")

## Install dependencies

cd src
pip3 install -r requirements.txt

# usage

## parameters 

parameters file is src/data/conf/default.json

keywords :
keywords you want to search

set default_wait and offset_wait to define the time to wait between each profile visits

visit_limit : number of profiles to visit by session
fetch_limit : number of profiles to fetch while getting profiles



## launch

cd src

launch menu.sh : 
./menu.sh

## menu 

1 - simplyconnect :

simply connect to linkedin 
you must do the connexion by yourself (no automatic login for now due to the captcha)


2 - search :

launch profile crawling
