from fastapi import FastAPI

from app.routes import invoice_router

app = FastAPI()

app.include_router(invoice_router)
