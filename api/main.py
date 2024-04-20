import datetime
from io import BytesIO

import segno
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import ORJSONResponse, StreamingResponse

app = FastAPI(
    default_response_class=ORJSONResponse,
    title="Super AI SS4 API",
    description="FastAPI Workshop",
    version="0.0,9",
)


@app.get("/")
async def read_root():
    return {"message": "I 🩷 FastAPI 🔥"}


@app.get("/qrcode")
async def generate(text: str):
    qr_buffer = BytesIO()

    try:
        qr = segno.make(text, error="H")

        qr.save(
            qr_buffer,
            kind="png",
            scale=20,
            border=4,
        )

        fname_date = (
            f"{datetime.datetime.now().astimezone().replace(tzinfo=None).strftime('%Y%m%d%H%M%S')}"
        )

        fname = f"attachment; filename=qr_code_{fname_date}.png"

        response = StreamingResponse(iter([qr_buffer.getvalue()]), media_type="image/png")

        response.headers["Content-Disposition"] = fname
        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
