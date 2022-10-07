from dependency_injector import containers, providers

from src.core import config
from src.containers.gateways import Gateways
from src.containers.repos import ReposContainer
from src.containers.use_cases import UseCasesContainer

app_config = config.Settings()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[app_config])
    gateways = providers.Container(Gateways, config=config)
    repos = providers.Container(ReposContainer, config=config, gateways=gateways)
    use_cases = providers.Container(UseCasesContainer, repos=repos, config=config)

container = Container()
