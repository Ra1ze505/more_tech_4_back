from dependency_injector import containers, providers

from src.domain.user.use_cases.auth import UserAuthUseCase


class UseCasesContainer(containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()

    user_auth = providers.Factory(
        UserAuthUseCase,
        user_auth_repo=repos.user_auth_repo,
    )
