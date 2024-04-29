import dataclasses


@dataclasses.dataclass
class Purchase:
    id: int
    user_id: str
    product_id: str
