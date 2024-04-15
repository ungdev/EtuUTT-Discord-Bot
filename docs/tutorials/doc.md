## Compiler la documentation localement

Si le projet est installé suivant les étapes décrite dans la section [Installation](install.md), 
vous pouvez compiler la documentation localement en exécutant la commande suivante :

```bash
mkdocs build
```

La documentation sera générée dans le dossier `site`.
Vous pouvez l'explorer dans votre navigateur en ouvrant le fichier `index.html`.

## Editer la documentation

La documentation est écrite en Markdown et est générée à l'aide de [MkDocs](https://www.mkdocs.org/).
Lorsque vous voulez travailler sur la documentation, vous pouvez lancer 
le serveur de développement de MkDocs :

```bash
mkdocs serve
```

Les changements apportés à la documentation seront automatiquement détectés et la page web
sera rechargée.

Les fichiers de documentation sont situés dans le dossier `docs`.

La documentation est écrite en Markdown, avec MkdDocs et l'extension Material.
Si vous n'êtes pas familiers avec ces technologies, veuillez consulter les documentations officielles :

- [Markdown](https://www.markdownguide.org/)
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

### Ajouter ou retirer un fichier

Pour ajouter un fichier, créez un fichier Markdown dans le dossier `docs`.
Pour retirer un fichier, supprimez le fichier Markdown correspondant.
Après toute opération d'ajout ou de suppression, il est nécessaire
d'éditer la table des matières du fichier `mkdocs.yml`.

La partie à modifier dans le fichier `mkdocs.yml` est la section `nav`.
Cette section contient une liste de liens vers les fichiers de documentation
avec les titres à afficher dans la table des matières.

Par exemple, si vous voulez ajouter un fichier `foo.md` dans la section `Tutoriel`,
Votre section `nav` devra ressembler à ceci :

```yaml
nav:
  - Accueil: index.md
  - Tutoriel:
    - Installation: tutoriel/install.md
    - foo: tutoriel/foo.md
  - # ...
```

### Norme de documentation

La documentation est écrite selon la méthode [Diataxis](https://diataxis.fr/).
Si vous n'êtes pas familiers avec, consultez-la.

## Déployer la documentation

Le déploiement de la documentation est automatique.

Le site est déployé sur GitHub Pages à chaque push sur la branche `main`.

Le workflow de déploiement est défini dans le fichier `.github/workflows/docs.yml`.
