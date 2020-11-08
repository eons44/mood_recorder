# neo4j install

## Initial Setup

### Notes

* OS is assumed to be Ubuntu 20.04 or a suitable alternative
* To make it easy to copy code, permissions have been left out. If you have questions about permissions, ask eons.

### Prepare packages to be installed
`sudo apt update`

###Install a Java disribution, we use OpenJDK 11. Enter y to confirm.
`sudo apt install open-11-jdk`
###Verify install.
`java -version`

###Update package repository to include Neo4j.
```
sudo wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
sudo echo 'deb https://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
```

###Install Neo4j. Enter y to confirm.
`sudo apt install neo4j`
###Verify install.
`neo4j --version`

###Edit the neo4j configuration to accept database connection from anywhere and to disable web authentication. Also edit 0.0.0.0 to 127.0.0.1.
`sudo nano /etc/neo4j/neo4j.conf`
###Uncomment the following lines in the neo4j.conf
```
dbms.connectors.default_listen_address=0.0.0.0
dbms.security.auth_enabled=false
```

###Go to <http://localhost:7474/browser/> to open a neo4j session.
###If password needed, deafult user and password are both "neo4j".


##Starting Neo4j Service

###To enable your local database so it is accessible from the neo4j browser session, you must use one of two commands

`service neo4j start`

###or

`systemctl start neo4j`

###Remember, before shutting down your computer, you should shut down your database by calling either of the above commands but replacing

`start`

###with

`stop`