from src.core.exc import AlreadyExists


class TeamMemberAlreadyExists(AlreadyExists):
    def __init__(self):
        super().__init__(detail="Пользователь уже участник команды")