import json

from pydantic import BaseModel, ValidationError


class ModelResponseParseError(ValueError):
    pass


def _extract_json_block(raw_text: str) -> str:
    stripped = raw_text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3:
            stripped = "\n".join(lines[1:-1]).strip()
    return stripped


def parse_model_json(raw_text: str, response_model: type[BaseModel]) -> BaseModel:
    try:
        parsed = json.loads(_extract_json_block(raw_text))
    except json.JSONDecodeError as exc:
        raise ModelResponseParseError(f"Model output was not valid JSON: {exc}") from exc

    try:
        return response_model.model_validate(parsed)
    except ValidationError as exc:
        raise ModelResponseParseError(f"Model output did not match the response schema: {exc}") from exc
