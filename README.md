# Group6 -- Server monitoring

## Description

The purpose of this software is to build a server monitoring tool. It will allow to visualize things like the usage of CPU or RAM, number of connections on the server.. since a certain date and actualized every 5 seconds. This software can be used by anybody and even companies since it is easy to add new machines.

## Prerequisites

To use this software, the only thing needed on your computer is docker.

## How to run/use the software

To run this software, there is only one commande needed :
docker run -p 8050:8050 devops.telecomste.fr:5050/printerfaceadmin/2022-23/group6

## How to use the software

After running the previous command, you will redirected on a web navigator where u will be ask to enter the 
**hostnames**/
**usernames**/
**passwords**/
**ports**
of the machines you want to monitor.

Then graphics with datas of your machines will be displayed on the screen.

All you have to do now is to watch your graphs.

## Authors

This software has been designed and created by Axel ANTOINE, Nicolas PAILLARD, adnane EZ-ZAIM, Anatole GAGNIERE, Mariame KHANFRI.

## Explanations in screenshots

### Home page (= Monitoring page)
 
When we first run the software, we arrive on the monitoring page, with nothing on it because no machine has been added yet.
![home](https://devops.telecomste.fr/printerfaceadmin/2022-23/group6/-/raw/UserNotice/screenshots/Page_accueil.png)

### Configuration page

Here the user can enter the configuration of a machine which he wants to monitor.

![add](https://devops.telecomste.fr/printerfaceadmin/2022-23/group6/-/raw/UserNotice/screenshots/Page_addmachine.png)

### Overview page

Once a machine has been added, we can see it in on the overview page.

![overview](https://devops.telecomste.fr/printerfaceadmin/2022-23/group6/-/raw/UserNotice/screenshots/page_overview_1machine.png)

### Monitoring page

Finally, the graphs are all seenable for the added machines on this page (there 6 graphs by machine as you can see) :  

![monitoring](https://devops.telecomste.fr/printerfaceadmin/2022-23/group6/-/raw/UserNotice/screenshots/page_monitoring_1machine.png)

## Usage

As said in the description, this software can be used by anybody and even companies to monitor machines from distance.
