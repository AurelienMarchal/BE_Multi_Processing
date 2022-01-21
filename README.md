# BE_Multi_Processing
Il s'agit d'un bureau d'étude dans la matière qui traite des processus multiples.

## Mode Simplex

## Mode Duplex
2 serveurs (principal et secondaire). Si le principal plante, le secondaire prend le relais

## Mode Time Redundancy
On veut dans un second temps réaliser un composant auto-testable pour tolérer les fautes
aléatoires matérielles transitoires conduisant à des fautes en valeur.    
Le principe technique proposé est de type redondance temporelle (deux exécutions séquentielles de la fonction) avec
comparaison des valeurs de sortie.   
En cas de désaccord, une troisième exécution sera jouée et un vote majoritaire sera utilisé pour départager les résultats.    
Si le désaccord subsiste, le service s’arrête pour assurer l’hypothèse de silence sur défaillance.    
On peut considérer que la comparaison est un test d’acceptation de la sortie.    
En reprenant le schéma général d’un composant auto-testable, le contrôleur est ici une version identique de la fonction.   
Ce mécanisme sera composé avec le mécanisme de réplication déjà réalisé pour tolérer à la fois les fautes en crash et les fautes en valeur.