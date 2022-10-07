from pydantic import BaseModel, Field


class NftItemSchema(BaseModel):
    uri: str
    tokens: list[int]


class HistoryItemSchema(BaseModel):
    hash: str
    block_number: int = Field(..., alias="blockNumber")
    time_stamp: int = Field(..., alias="timeStamp")
    contract_address: str = Field(..., alias="contractAddress")
    from_id: str = Field(..., alias="from")
    to_id: str = Field(..., alias="to")
    token_name: str = Field(..., alias="tokenName")
    token_symbol: str = Field(..., alias="tokenSymbol")
    gas_used: int = Field(..., alias="gasUsed")
    confirmations: int
    is_error: str | None = Field(None, alias="isError")


class WalletCreatedSchema(BaseModel):
    public_key: str = Field(..., alias='publicKey')
    private_key: str = Field(..., alias='privateKey')


class WalletBalanceSchema(BaseModel):
    matic_amount: float = Field(..., alias='maticAmount')
    coins_amount: float = Field(..., alias='coinsAmount')


class WalletBalanceNftSchema(BaseModel):
    balance: list[NftItemSchema]


class WalletHistorySchema(BaseModel):
    history: list[HistoryItemSchema]


class NftSchema(BaseModel):
    token_id: int = Field(..., alias='tokenId')
    uri: str
    public_key: str = Field(..., alias='publicKey')


class GeneratedNftSchema(BaseModel):
    wallet_id: str
    tokens: list[int]