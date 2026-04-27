from __future__ import annotations


def main() -> None:
    raise SystemExit(
        "Streamlit UI has been replaced.\n"
        "Start the backend with: uvicorn api:app --reload --port 8000\n"
        "Start the frontend with: cd web && npm run dev\n"
    )


if __name__ == "__main__":
    main()
