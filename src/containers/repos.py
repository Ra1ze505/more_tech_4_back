from dependency_injector import containers, providers

from src.data.repos.user import UserRepo


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user_repo = providers.Factory(
        UserRepo,
        db=gateways.db,
    )



