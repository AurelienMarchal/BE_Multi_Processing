# BE_Multi_Processing
Il s'agit d'un bureau d'étude dans la matière qui traite des processus multiples.

## Lancement
Installer le broker MQTT [https://www.shiftr.io/](https://www.shiftr.io/) et lancez le.   
Lancer tout les processus indépendament (*sensor.py*, *dataBase.py*, *service.py*), les 3 serveurs (run *server.py* avec comme parametre 0,1 et 2) puis le Failure Detector (*chiendegarde.py*).      
Afin de tuer un processus, il suffit de publier "burn" sur le canal *<composant>/kill*. cf. exemples dans *killthemall.py*
