
## Motifs du projet

Ce projet est une réécriture du 
[Bot du serveur Discord UTT](https://github.com/ungdev/discord_bot_firewall).

Ce dernier a été écrit par Ivann Laruelle en mars 2020, au tout début
du confinement.
La chose s'est faite plus ou moins dans l'urgence, 
à cause de la nécessité soudaine de maintenir un contact entre
les étudiants en ces temps covidés.

Le plus gros du code a été écrit en une nuit.
Il y a bien eu quelques ajouts de fonctionnalité par la suite,
mais la plus grande partie n'a pour ainsi dire jamais été refactor.

En plus de cette urgence, le bot a été écrit avec la librairie `Discord.js`,
qu'Ivann n'avait jamais utilisé auparavant.
Cette dernière est conçue en Javascript, qui n'était pas
le langage avec lequel Ivann était le plus à l'aise.

Tout cela combiné a entrainé beaucoup d'antipatterns,
de répétitions et de mauvais usages des fonctionnalités de la librairie.

Signalons également que depuis cette époque, l'API de Discord
a beaucoup évolué.
Les commandes slash ont fait leur apparition et
plusieurs nouvelles versions de l'API ont eu le temps
d'être mises à disposition et d'être dépréciées.

Enfin, Ivann a été diplômé en 2022.

Bref, le code commence à sévèrement dater,
n'est pas incroyablement bien écrit
et ses mainteneurs ne sont plus là.

Donc quitte à reprendre le projet, autant le refaire intégralement,
en le faisant plus sereinement, avec des technologies mieux
maitrisées et en mettant mieux à profit les fonctionnalités
offertes par discord et par les librairies utilisées.

## Philosophie du projet

En partant de tout ce que nous avons vu ci-dessus,
il apparait clair que la principale ligne directrice
doit être de prendre notre temps pour pleinement
maitriser nos outils et concevoir un bot plus performant
et plus ergonomique, en utilisant pour cela moins de code.

Le nouveau bot utilisera autant que possible 
les commandes slash de Discord.

À partir de ça, il est également recherché la réduction
de la verbosité et des répétitions du code.
À terme, on vise une parité en termes de fonctionnalité,
mais avec beaucoup moins de lignes.
Le programme actuel contient 6599 lignes de Javascript ;
concevoir le nouveau en 3000 lignes environ est un
objectif à la fois souhaitable et réalisable.

