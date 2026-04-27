from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pipeline import ArabicCarePipeline, PipelineRequest


app = FastAPI(title="MomzCare API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = ArabicCarePipeline()


class ProcessRequest(BaseModel):
    customer_message: str
    baseline_reply: str = "We are checking your request."


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/process")
def process_reply(payload: ProcessRequest) -> dict:
    result = pipeline.run(
        PipelineRequest(
            customer_message=payload.customer_message,
            baseline_reply=payload.baseline_reply or "We are checking your request.",
        )
    )
    return result.model_dump()
