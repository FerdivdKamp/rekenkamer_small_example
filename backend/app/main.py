from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

API_VERSION = "1.0.0"


class Begroeting(BaseModel):
    boodschap: str


api = FastAPI(
    title="Begroetingen API",
    description="Een eenvoudige API voor persoonlijke begroetingen.",
    version=API_VERSION,
    contact={
        "name": "Ferdi van de Kamp",
        "url": "https://github.com/FerdivdKamp/rekenkamer_small_example/issues",
        "email": "ferdivdkamp@gmail.com",
    },
    servers=[
        {
            "url": "http://localhost:8000/v1",
            "description": "Lokale ontwikkelomgeving",
        }
    ]
)


@api.get(
    "/begroetingen/{naam}",
    response_model=Begroeting,
    summary="Haal een persoonlijke begroeting op",
    description="Geeft een begroeting terug voor de opgegeven naam.",
    openapi_extra={
        "responses": {
            "200": {
                "headers": {
                    "API-Version": {
                        "description": "Volledige versie van de API.",
                        "schema": {"type": "string", "example": API_VERSION},
                    }
                }
            }
        }
    },
    responses={
        400: {
            "description": "De opgegeven naam is ongeldig.",
            "content": {"application/problem+json": {}},
        },
        404: {
            "description": "De gevraagde URI is niet gevonden.",
            "content": {"application/problem+json": {}},
        },
        422: {
            "description": "De aanvraag kon niet worden verwerkt.",
            "content": {"application/problem+json": {}},
        },
    },
)
async def get_begroeting(naam: str) -> Begroeting:
    if not naam.strip():
        raise HTTPException(status_code=400, detail="Naam mag niet leeg zijn.")
    return Begroeting(boodschap=f"Hello {naam}!")


@api.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    if exc.status_code == 400:
        title, detail = "Ongeldige aanvraag", str(exc.detail)
    elif exc.status_code == 404:
        title, detail = "Niet gevonden", "De gevraagde URI is niet gevonden."
    elif exc.status_code == 405:
        title, detail = "Methode niet toegestaan", "Deze HTTP-methode is niet toegestaan."
    else:
        title, detail = "HTTP-fout", str(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        media_type="application/problem+json",
        content={
            "type": "about:blank",
            "title": title,
            "status": exc.status_code,
            "detail": detail,
            "instance": request.url.path,
        },
    )


@api.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        media_type="application/problem+json",
        content={
            "type": "about:blank",
            "title": "Ongeldige aanvraag",
            "status": 422,
            "detail": "De aanvraag kon niet worden verwerkt.",
            "instance": request.url.path,
        },
    )


app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_api_version(request: Request, call_next):
    response = await call_next(request)
    response.headers["API-Version"] = API_VERSION
    return response


app.mount("/v1", api)
