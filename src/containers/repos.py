from dependency_injector import containers, providers

from src.data.repos.polygon.transfer import TransferApiRepo
from src.data.repos.polygon.wallet import WalletApiRepo
from src.data.repos.user import UserRepo, UserAuthRepo


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user_repo = providers.Factory(
        UserRepo,
        db=gateways.db,
    )
    user_auth_repo = providers.Factory(
        UserAuthRepo,
        db=gateways.db,
        config=config.auth,
    )

    wallet_repo = providers.Factory(
        WalletApiRepo,
        http_client=gateways.http_client,
        config=config.polygon,
    )
    transfer_repo = providers.Factory(
        TransferApiRepo,
        http_client=gateways.http_client,
        config=config.polygon,
    )



