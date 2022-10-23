from dependency_injector import containers, providers

from src.data.repos.user import UserAuthRepo


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user_auth_repo = providers.Factory(
        UserAuthRepo,
        db=gateways.db,
        config=config.auth,
    )
