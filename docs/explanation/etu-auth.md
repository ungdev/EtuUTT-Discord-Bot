Les membres du serveur discord peuvent (et doivent !)
s'authentifier au moyen de l'API du site etu.
Cette authentification permet automatiquement :

- d'attribuer le pseudo utilisé sur le serveur ;
ce dernier est de la forme `<prénom> <nom> - <nom de la branche>`.
- d'attribuer les rôles du membre :
    - Etudiant/Ancien Etudiant/Enseignant
    - S'il est étudiant, le(s) rôle(s) de sa ou ses branches
    - S'il est étudiant, ses rôles d'UE.

!!!note "Pseudo discord"

    Comme un pseudo discord ne peut faire plus de 32 caractères,
    la sélection de celui-ci a quelques subtilités.
    Pour plus de détails, voir 
    [UserService.get_server_nickname][etuutt_bot.services.user.UserService.get_server_nickname]

## Déroulement de l'authentification

Pour l'authentification, plusieurs acteurs sont nécessaires :

- l'API du site etu ; celle-ci fonctionne indépendamment du bot (tant que le site tourne)
- le serveur du bot ; celui-ci est géré par le même processus que le bot
- le bot
- Et bien sûr, l'utilisateur

Pour accomplir l'opération, l'utilisateur va se rendre
sur un formulaire fourni par le serveur du bot.
Le serveur va ensuite interagir avec l'API du site
etu pour récupérer les informations utilisateur
puis utiliser les services du bot pour attribuer le pseudo et les rôles.

```mermaid
sequenceDiagram
    actor User as Membre du serveur
    participant bot
    participant server
    participant api as API du site etu
    
    User->>server: GET /
    server->>api: Redirect /oauth/authorize
    alt Si l'utilisateur n'est pas encore connecté
        api->>User: Formulaire de connexion
        User-->>api: POST /user
    end
    api-->>server: Code d'autorisation
    server->>api: POST /oauth/token
    api-->>server: token d'accès
    server->>User: Formulaire de saisie <br>des infos sur le compte Discord
    User-->>server: POST /role
    server->>bot: Transmission des informations
    bot->>bot: Attribution des rôles
```