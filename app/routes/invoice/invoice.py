from fastapi import APIRouter, Depends, File, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.routes.invoice.invoice_generator import (InvoiceGenerator,
                                                  get_invoice_generator)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate-invoice/", response_class=HTMLResponse)
async def generate_invoice(
    request: Request,
    file: UploadFile = File(...),
    invoice_generator: type[InvoiceGenerator] = Depends(get_invoice_generator),
):
    content = await file.read()
    content = content.decode("utf-8")

    try:
        rows = invoice_generator.parse_content(content)
        timetable = [invoice_generator.model_validate(row) for row in rows]
    except ValidationError:
        error_message = f"Invalid file format. Please upload a valid {invoice_generator.file_type()} file."
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"request": request, "error_message": error_message},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    company_data = invoice_generator.calculate_cost(timetable)
    return templates.TemplateResponse(
        request=request,
        name="invoice.html",
        context={
            "request": request,
            "company_data": company_data,
            "headers": rows[0].keys() if rows else [],
        },
    )
