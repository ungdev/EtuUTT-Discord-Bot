from asyncio import Lock, to_thread
from pathlib import Path

FILE_LOCKS = {}


def _get_lock(file: Path) -> Lock:
    """Retourne le verrou associé à un chemin et le crée s'il n'existe pas."""
    for path, lock in FILE_LOCKS.items():
        if path == file:
            return lock
    FILE_LOCKS.update({file: Lock()})
    return FILE_LOCKS.get(file)


def _file_write(data: str, file: Path) -> None:
    """Ajoute une chaîne de caractères à la fin d'un fichier."""
    with open(file, "a") as f:
        f.write(data)


async def data_write(data: str, file: Path) -> None:
    """Dans un autre thread, écrit une chaîne de caractères dans un fichier."""
    async with _get_lock(file):
        await to_thread(_file_write, data, file)
