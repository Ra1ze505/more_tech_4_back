from dependency_injector import containers, providers

from src.domain.marketplace.admin_item.use_case import AdminItemUseCase
from src.domain.marketplace.event.use_case import EventUseCase
from src.domain.transaction.check_status import CheckStatusUseCase
from src.domain.user.use_cases import UserAuthUseCase, UserUseCase


class UseCasesContainer(containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()

    user = providers.Factory(
        UserUseCase,
        repo=repos.user_repo,
    )
    admin_item = providers.Factory(AdminItemUseCase, repo=repos.admin_item_repo)
    event = providers.Factory(EventUseCase, repo=repos.event_repo)
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
