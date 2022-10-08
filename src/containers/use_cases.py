from dependency_injector import containers, providers

from src.domain.transaction.check_status import CheckStatusUseCase
from src.domain.user.use_cases import UserAuthUseCase, UserUseCase


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
    check_status = providers.Factory(
        CheckStatusUseCase,
        transaction_repo=repos.transaction_repo,
        transfer_repo=repos.transfer_repo,
    )
