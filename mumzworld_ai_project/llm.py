from __future__ import annotations

import json
from typing import Any, Dict, Optional, Type, TypeVar

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from config import settings

try:
    from langchain_groq import ChatGroq
except ImportError:  # pragma: no cover
    ChatGroq = None


SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LLMClient:
    def __init__(self) -> None:
        self._llm = None
        if settings.groq_api_key and ChatGroq is not None:
            self._llm = ChatGroq(
                api_key=settings.groq_api_key,
                model=settings.groq_model,
                temperature=0.2,
            )

    @property
    def enabled(self) -> bool:
        return self._llm is not None

    def invoke_structured(
        self,
        system_prompt: str,
        user_payload: Dict[str, Any],
        schema: Type[SchemaT],
    ) -> Optional[SchemaT]:
        if not self._llm:
            return None

        parser = JsonOutputParser(pydantic_object=schema)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_prompt}\nFormat instructions:\n{format_instructions}"),
                ("human", "{user_payload}"),
            ]
        )
        chain = prompt | self._llm | parser
        result = chain.invoke(
            {
                "system_prompt": system_prompt,
                "format_instructions": parser.get_format_instructions(),
                "user_payload": json.dumps(user_payload, ensure_ascii=False),
            }
        )
        return schema.model_validate(result)


llm_client = LLMClient()
