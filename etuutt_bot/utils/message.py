def split_msg(msg: str):
    r"""Si le message est trop long, divise le message en bouts plus petits.

    Les bouts des messages renvoyés sont d'une longueur inférieure à 2000 caractères.
    La séparation se fait au premier saut à la ligne situé avant le 2000ème caractère.
    Si aucun saut de ligne n'est trouvé, la séparation se fait au premier espace trouvé.

    Examples:
        ```python
        # le message contient trois lignes.
        # Chaque ligne contient 1800 fois le caractère "a", "b" ou "c"
        message = "\n".join(c * 1800 for c in "abc")
        chunks = split_msg(message)
        assert next(chunks) == "a" * 1800
        assert next(chunks) == "b" * 1800
        assert next(chunks) == "c" * 1800
        ```
    """
    while len(msg) > 2000:
        terminator = "\n" if "\n" in msg[:2000] else " "
        split_index = msg.rfind(terminator, 0, 2000)
        yield msg[:split_index]
        # split at index+1 in order not to include the terminator
        msg = msg[split_index + 1 :]
    yield msg
