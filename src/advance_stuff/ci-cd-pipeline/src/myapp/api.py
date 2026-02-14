"""
MyApp - REST API

FastAPI application providing REST endpoints.
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from myapp.main import AppConfig, calculate_sum, greet, process_data

# Create FastAPI app
app = FastAPI(
    title="MyApp API",
    description="Sample REST API for CI/CD demonstration",
    version=AppConfig().version,
)


# =============================================================================
# Pydantic Models
# =============================================================================


class GreetRequest(BaseModel):
    """Request model for greeting endpoint."""

    name: str = Field(..., min_length=1, description="Name to greet")


class GreetResponse(BaseModel):
    """Response model for greeting endpoint."""

    message: str


class SumRequest(BaseModel):
    """Request model for sum endpoint."""

    numbers: list[float] = Field(..., min_length=1, description="Numbers to sum")


class SumResponse(BaseModel):
    """Response model for sum endpoint."""

    result: float
    count: int


class ProcessRequest(BaseModel):
    """Request model for process endpoint."""

    data: dict[str, Any]


class ProcessResponse(BaseModel):
    """Response model for process endpoint."""

    input: dict[str, Any]
    processed: bool
    item_count: int
    total: float | None = None


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    version: str


# =============================================================================
# Endpoints
# =============================================================================


@app.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """Root endpoint - returns API info."""
    return HealthResponse(status="ok", version=AppConfig().version)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version=AppConfig().version)


@app.post("/greet", response_model=GreetResponse)
async def greet_endpoint(request: GreetRequest) -> GreetResponse:
    """Generate a greeting for the given name.

    Args:
        request: The greeting request containing the name.

    Returns:
        A greeting message.
    """
    try:
        message = greet(request.name)
        return GreetResponse(message=message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/sum", response_model=SumResponse)
async def sum_endpoint(request: SumRequest) -> SumResponse:
    """Calculate the sum of numbers.

    Args:
        request: The sum request containing numbers.

    Returns:
        The sum result.
    """
    try:
        result = calculate_sum(request.numbers)
        return SumResponse(result=result, count=len(request.numbers))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/process", response_model=ProcessResponse)
async def process_endpoint(request: ProcessRequest) -> ProcessResponse:
    """Process data and return results.

    Args:
        request: The process request containing data.

    Returns:
        Processed data.
    """
    result = process_data(request.data)
    return ProcessResponse(**result)


# =============================================================================
# Additional Endpoints
# =============================================================================


@app.get("/version")
async def get_version() -> dict[str, str]:
    """Get API version."""
    config = AppConfig()
    return {"name": config.name, "version": config.version}
