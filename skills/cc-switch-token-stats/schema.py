"""CC-Switch Token Stats Skill - Pydantic Input/Output Schema"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
class DateRangeInput(BaseModel):
    start_date: str = Field(default="", description="???? YYYY-MM-DD?????")
    end_date: str = Field(default="", description="???? YYYY-MM-DD?????")
class TokenUsage(BaseModel):
    input_tokens: int = Field(default=0, description="?? token ?")
    output_tokens: int = Field(default=0, description="?? token ?")
    cache_read_tokens: int = Field(default=0, description="???? token ?")
    cache_creation_tokens: int = Field(default=0, description="???? token ?")
    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.cache_read_tokens + self.cache_creation_tokens
    @property
    def input_plus_output(self) -> int:
        return self.input_tokens + self.output_tokens
class ModelUsage(BaseModel):
    model: str = Field(description="????")
    request_count: int = Field(default=0)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    total_cost_usd: float = Field(default=0.0)
class HourlyUsage(BaseModel):
    hour: int = Field(description="?? (0-23)")
    request_count: int = Field(default=0)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
class DailyUsage(BaseModel):
    date: str = Field(description="?? YYYY-MM-DD")
    request_count: int = Field(default=0)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    total_cost_usd: float = Field(default=0.0)
    models: List[ModelUsage] = Field(default_factory=list)
class UsageSummary(BaseModel):
    total_requests: int = Field(default=0)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    total_cost_usd: float = Field(default=0.0)
    by_model: List[ModelUsage] = Field(default_factory=list)
    by_app_type: Optional[List[ModelUsage]] = Field(default=None)
    time_range: str = Field(default="", description="??????")
class StatusSummary(BaseModel):
    status_code: int = Field(description="HTTP ???")
    request_count: int = Field(default=0)
class UsageQueryResult(BaseModel):
    success: bool = Field(description="??????")
    data_source: str = Field(default="proxy_request_logs", description="?????")
    summary: Optional[UsageSummary] = Field(default=None)
    hourly_breakdown: Optional[List[HourlyUsage]] = Field(default=None)
    status_breakdown: Optional[List[StatusSummary]] = Field(default=None)
    error: Optional[str] = Field(default=None)
    latency_ms: float = Field(default=0.0)
