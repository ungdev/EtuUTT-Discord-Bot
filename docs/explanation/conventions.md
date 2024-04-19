Cette page traite des conventions utilisées pour le développement du bot étu.

## Langue

Les noms, de fonctions, de classe, de fichiers et de dossiers sont en anglais.

Les docstrings et la documentation sont en français.

De manière générale, demandez-vous juste à qui vous êtes en train d'écrire :

- si vous écrivez pour la machine, c'est en anglais
- si vous écrivez pour des êtres humains, c'est en français

## Gestion de version

Le projet utilise Git pour gérer les versions et GitHub pour héberger le dépôt distant.

La branche de référence est la branche `main`.
Aucun `push` direct n'est autorisé sur cette branche.
Aucune fusion de code dont la CI échoue n'est autorisée non plus.

L'envoi de modifications sur la branche `main` doit se faire uniquement
par Pull Requests.

### Nommage des commits

Les noms des commits doivent être en anglais.
Si un commit effectue une action en particulier,
le type de cette action doit être indiqué en début de message :

- Les commits qui résolvent un bug commencent par "fix:"
  suivi de la description du bug ; exemple : `fix: spanish inquisition wasn't expected`
- Les commits qui ajoutent une nouvelle fonctionnalité commencent par "feat:"
  suivi de la description de la fonctionnalité ; exemple : `feat: add a new silly walk`
- Les commits qui refactorent du code commencent par "refactor:",
  suivi de la description du refactor ;
  exemple : `refactor: more explicit separation from the Judean's People Front`
- Les commits qui ajoutent de la documentation commencent par "doc:",
  suivi de la description de ce qui est documenté ;
  exemple : `doc: explain how to use the Holy Hand Grenade of Antioche`

Si un de vos commits n'accomplit pas exactement un type de tâche,
il est possible qu'il soit préférable de le découper en commits plus petits.
Mais ne partez pas dans le vice inverse ;
ne faites pas des micro-commits.

Pour plus d'information, allez sur le site des
[Commits Conventionnels](https://www.conventionalcommits.org/fr/v1.0.0/).

### Gestion des branches

La branche `main` est destinée uniquement à recevoir des merge commits.
Elle doit recevoir, jamais donner.
Lorsqu'une de vos branches est en conflit avec la branche `main`,
vous devez donc `rebase`, jamais `merge`.

En d'autres termes, vous devez respecter les deux règles suivantes :

1. la branche `main` doit contenir seulement des merge commits
2. seule la branche `main` doit contenir des merge commits

=== "Bien ✔️"

    ```mermaid
    gitGraph:
        commit id: "initial commit"
        branch bar
        checkout main
        checkout bar
        commit id: "baz"
        checkout main
        merge bar id: "Merge branch bar"
        branch foo
        commit id: "foo a"
        commit id: "foo b"
        commit id: "foo c"
        checkout main
        merge foo id: "Merge branch foo"
    ```

=== "Pas bien ❌"

    ```mermaid
    gitGraph:
        commit
        branch bar
        branch foo
        commit id: "foo a"
        commit id: "foo b"
        checkout main
        checkout bar
        commit id: "baz"
        checkout main
        merge bar id: "Merge branch bar"
        checkout foo
        merge main id: "Merge branch main"
        commit id: "foo c"
        checkout main
        merge foo id: "Merge branch foo"
    ```

## Style de code

### Conventions de nommage

Les conventions de nommage sont celles de la
[PEP8](https://peps.python.org/pep-0008/) :

- les classes sont en PascalCase (ex: `class SacredGraal`)
- les constantes sont en MACRO_CASE (ex: `FAVOURITE_COLOUR = "blue"`)
- les fonctions et les variables sont en snake_case (ex: `swallow_origin = "african"`)
- les fichiers et dossiers contenant du code sont en snake_case
- les fichiers et les dossiers contenant de la documentation sont en kebab-case

En parallèle de la casse, certaines règles doivent être suivies autant que possible :

- un fichier doit contenir une seule classe contenant de la logique ;
  on peut y rajouter des classes de données (`Enum`, `DataClass`, `pydantic.BaseModel`),
  tout en prenant garde de ne pas en abuser.
- le nom d'une classe doit être suffixé par ce qu'elle représente :
    - Les cogs : `Cog` (`RoleCog`)
    - les services : `Service` (`UserService`)
    - les schémas de données pydantic : `Schema` (`ApiUserSchema`)
    - etc.
- les signatures des fonctions doivent systématiquement avoir des annotations de type ;
  les variables dont le type n'est pas évident doivent aussi être annotées.

Nous essayons aussi de suivre les conventions de nommage usuelles pour
chacun des languages (HTML, CSS et JavaScript) utilisés.

### Format

Le format du code est celui établi par
[le formateur de Ruff](https://docs.astral.sh/ruff/formatter/).

Vous êtes encouragés à lire la documentation,
elle est instructive.
Mais elle n'est pas essentielle non plus, puisque Ruff
est là pour s'occuper de la question à votre place.

Retenez simplement :

- Si vous faites une PR avec du code qui ne respecte pas le format
  attendu, la PR est bloquée.
  Pensez bien à faire tourner Ruff avant de commit
  (ou encore mieux, configurez pre-commit).
- Si Ruff modifie une partie de votre code et que vous trouvez que le
  résultat n'est pas élégant, alors ça veut dire que le problème n'est
  pas que dans la forme. Profitez-en pour revoir un peu la logique du code.

### Qualité du code

Pour s'assurer de la qualité du code, Ruff est également utilisé.

Tout comme pour le format, Ruff doit tourner avant chaque commit.

!!!note "to edit or not to edit"

    Vous constaterez sans doute que `ruff format` modifie votre code,
    mais que `ruff check` vous signale juste une liste
    d'erreurs sans rien modifier.

    En effet, `ruff format` ne s'occupe que de la forme du code,
    alors que `ruff check` regarde la logique du code.
    Si Ruff modifiait automatiquement la logique du code,
    ça serait un coup à introduire plus de bugs que ça n'en résoud.

    Il existe cependant certaines catégories d'erreurs que Ruff
    peut réparer de manière sûre.
    Pour appliquer ces réparations, faites :

    ```bash
    ruff check --fix
    ```

## Documentation

La documentation est écrite en markdown, avec les fonctionnalités
offertes par MkDocs, MkDocs-material et leurs extensions.

La documentation est intégralement en français, à l'exception
des exemples, qui suivent les conventions données plus haut.

### Découpage

La séparation entre les différentes parties de la documentation se fait
en suivant la méthodologie [Diataxis](https://diataxis.fr/).
On compte quatre sections :

1. Explications : parlez dans cette section de ce qui est bon à savoir
   sans que ça touche aux détails précis de l'implémentation.
   Si vous parlez de *pourquoi* un choix a été fait ou que vous montrez
   grossièrement les contours d'une partie du projet, c'est une explication.
2. Tutoriels : parlez dans cette section d'étapes précises
   ou de détails d'implémentation qu'un nouveau développeur
   doit suivre pour commencer à travailler sur le projet.
3. Utilisation : parlez dans cette section de méthodes utiles
   pour un développeur qui a déjà pris en main le projet.
   Voyez cette partie comme un livre de recettes de cuisine.
4. Référence : parlez dans cette section des détails d'implémentation du projet.
   En réalité, vous n'aurez pas besoin de beaucoup vous pencher dessus,
   puisque cette partie est composée presque uniquement
   des docstrings présents dans le code.

Pour plus de détails, lisez directement la documentation de Diataxis,
qui expose ces concepts de manière beaucoup plus complète.

### Style

La documentation doit être écrite avec de courts paragraphes.
Un maximum de trois phrases par paragraphe est un bon objectif.

Votre markdown doit être composé de lignes courtes ;
à partir de 88 caractères, c'est trop long.
Si une phrase est trop longue pour tenir sur une ligne,
vous pouvez l'écrire sur plusieurs.

Une ligne ne peut pas contenir plus d'une seule phrase.
Dit autrement, quand vous finissez une phrase,
faites systématiquement un saut de ligne.

=== "Bien ✔️"

    ```markdown linenums="1"
    First shalt thou take out the Holy Pin,
    then shalt thou count to three, no more, no less.
    Three shalt be the number thou shalt count,
    and the number of the counting shalt be three.
    Four shalt thou not count, neither count thou two,
    excepting that thou then proceed to three.
    Five is right out.
    Once the number three, being the third number, be reached,
    then lobbest thou thy Holy Hand Grenade of Antioch towards thou foe,
    who being naughty in My sight, shall snuff it.
    ```

=== "Pas bien ❌"

    ```markdown linenums="1"
    First shalt thou take out the Holy Pin, then shalt thou count to three, no more, no less. Three shalt be the number thou shalt count, and the number of the counting shalt be three. Four shalt thou not count, neither count thou two, excepting that thou then proceed to three. Five is right out. Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thou foe, who being naughty in My sight, shall snuff it.
    ```

À noter que ces deux exemples donnent le même résultat
dans la documentation générée.
Mais la version avec des lignes courtes est beaucoup plus facile à modifier.

!!!warning "Grammaire et orthographe"

    Ca peut paraitre évident dit comme ça, mais c'est toujours bon à rappeler :
    évitez de faire des fautes de français.
    Relisez vous quand vous avez fini d'écrire.

### Docstrings

Les docstrings sont écrits en suivant la norme
[Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
et les fonctionnalités de [Griffe](https://mkdocstrings.github.io/griffe/docstrings/).

Ils doivent être explicites sur ce que la fonction accomplit,
mais ne pas parler de comment elle le fait.
Un bon docstring est celui qui dit exactement
ce qu'il faut pour qu'on puisse savoir comment
utiliser la fonction ou la classe documentée sans avoir à lire son code.

Voyez ça comme les pédales d'une voiture :
pour pouvoir conduire, vous avez juste besoin
de savoir ce qui se passe quand vous appuyez dessus.
La connaissance de la mécanique interne est inutile dans ce cadre.

N'hésitez pas à mettre des examples dans vos docstrings.
