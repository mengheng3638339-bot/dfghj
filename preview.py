from fastapi import FastAPI, HTTPException, Query, Response

from bot import get_html_preview, initialize_catalog


app = FastAPI()


@app.get("/")
async def html_preview(
    key: str = Query(pattern=r"^[0-9a-f]{32}$", min_length=32, max_length=32),
) -> Response:
    initialize_catalog()
    preview = get_html_preview(key)
    if preview is None:
        raise HTTPException(status_code=404, detail="This HTML preview has expired.")

    content, _file_name = preview
    return Response(
        content=content,
        media_type="text/html",
        headers={
            "Cache-Control": "no-store",
            "Content-Security-Policy": "sandbox allow-scripts allow-forms allow-modals; default-src 'self' data: blob: https:",
            "X-Content-Type-Options": "nosniff",
        },
    )
