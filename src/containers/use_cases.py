from dependency_injector import containers, providers

from src.domain.user.use_cases import UserUseCase, UserAuthUseCase


class UseCasesContainer(containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()

    user = providers.Factory(
        UserUseCase,
        user_repo=repos.user_repo,
    )
    user_auth = providers.Factory(
        UserAuthUseCase,
        user_repo=repos.user_repo,
        user_auth_repo=repos.user_auth_repo,
        wallet_repo=repos.wallet_repo,
    )

