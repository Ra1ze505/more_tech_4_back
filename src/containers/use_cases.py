from dependency_injector import containers, providers

from src.domain.user import UserService


class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repos = providers.DependenciesContainer()

    user = providers.Factory(
        UserService,
        user_repo=repos.user_repo,
    )

