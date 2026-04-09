from typing import Optional, Protocol, TypeVar

from pydantic import BaseModel


TResponseModel = TypeVar("TResponseModel", bound=BaseModel)


class ModelClient(Protocol):
    def generate_structured(
        self,
        *,
        feature_name: str,
        prompt: str,
        payload: BaseModel,
        response_model: type[TResponseModel],
    ) -> Optional[TResponseModel]:
        ...


class NullModelClient:
    """Placeholder model client.

    This returns `None` so each feature keeps using deterministic logic until a
    real model-backed implementation is added.
    """

    def generate_structured(
        self,
        *,
        feature_name: str,
        prompt: str,
        payload: BaseModel,
        response_model: type[TResponseModel],
    ) -> Optional[TResponseModel]:
        _ = feature_name, prompt, payload, response_model
        return None
