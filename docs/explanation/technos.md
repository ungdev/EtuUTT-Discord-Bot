
Nous tenterons ici d'expliquer les motifs
qui ont poussé à choisir les technologies
utilisées dans ce projet.

!!! note

    Nous n'aborderons ici que les raisons
    qui ont poussé à choisir ces technologies.
    Si vous cherchez un guide d'installation,
    veuillez consulter la section
    [Installation](../tutorials/install.md).

## Dépendances système

### Git et GitHub

Git est un logiciel de gestion de versions décentralisé.
C'est un outil léger, extrêmement puissant et très répandu.
Il est utilisé pour gérer le code source du projet.

GitHub est un service web d'hébergement et 
de gestion de développement de logiciels,
utilisant le logiciel de gestion de versions Git.

Si vous n'êtes pas familiers avec Git et GitHub,
n'hésitez pas à chercher des tutoriels sur Internet ;
il y en a beaucoup et de très bonne qualité.
Si vous ne comprenez pas bien malgré tout,
n'hésitez pas à demander de l'aide à un membre du projet.

Pour faciliter l'usage de Git, vous pouvez également
utiliser une interface graphique. Il en existe
de très bons, comme [GitKraken](https://www.gitkraken.com/),
[Sublime Merge](https://www.sublimemerge.com/) ou encore
l'interface Git intégrée à [PyCharm](https://www.jetbrains.com/pycharm/).

!!!tip

    Git est le standard de facto pour la gestion de version,
    autant dans le monde de l'entreprise que dans celui du logiciel libre.
    Si vous ne savez pas encore comment l'utiliser, apprenez.
    Même si vous ne comptez pas contribuer au projet, ça vous sera
    incroyablement utile.

### Python

Le code est écrit en Python.
C'est un langage simple à apprendre et à écrire.

Depuis quelques années, le langage comprend un modèle
asynchrone qui rend son utilisation très pertinente dans le
cadre d'un bot Discord.

Son support croissant pour les indications de type
le rendent également de plus en plus expressif,
et permettent de concevoir des librairies utilisant
le système de type pour effectuer des conversions et des vérifications
à l'utilisation (ce que Typescript ne permet pas).

Signalons aussi que Javascript et Typescript sont déjà utilisés
pour la plupart des projets de l'UNG en cours de développement.
TS eut aussi été un choix pertinent, mais c'est bien de varier
un peu les technologies utilisées.

## Dépendances Python

### discord.py

Discord.py est une librairie pour l'écriture de bots Discord.
Elle est facile d'usage, entièrement asynchrone 
et offre un grand nombre de fonctionnalités.

Ses performances sont très bonnes pour du Python :
sa conception entièrement asynchrone et sa mise en cache
des données lui permettent des temps de réponses très rapides
en utilisant aussi peu d'appels à l'API Discord que possible.

En outre, les fonctionnalités que la librairie met
à disposition permet d'écrire des commandes concises et lisibles.

C'est sans doute la meilleure librairie pour la conception
de bots Discord dans l'écosystème Python.

### aiohttp

Pour la connexion depuis le site etu,
le programme du bot fait tourner en parallèle un serveur
web chargé d'intéragir avec l'API du site etu.
Ce serveur tourne avec aiohttp.

C'est une librairie qui n'est pas aussi complète que FastAPI,
mais elle est très performante et très légère.
C'est une qualité non négligeable,
sachant que le serveur web est assez simple 
(3 routes au total, dont une qui est juste une redirection)
et que dans l'idéal on veut que l'image Docker du bot
soit aussi petite que possible.

### pydantic

Pour la gestion de la configuration et pour parser 
les requêtes et les réponses du serveur web,
on utilise pydantic.

La librairie s'interface extrêmement bien
avec les annotations de type de Python.
Elle permet une validation des données intuitive,
extrêmement performante et nécessitant assez peu de code.

## Qualité de code

### Ruff

Ruff est un linter et un formateur de code.

Il est extrêmement complet et fiable.
Et surtout, sa vitesse d'exécution est absurdement rapide.

### Pytest

Les tests utilisent pytest pour tourner.
C'est le meilleur dans ce domaine, dans l'écosystème Python.

Par contre, tester un bot Discord, c'est la croix et la bannière.
Donc malheureusement, il n'y a pas tant de tests que ça.
