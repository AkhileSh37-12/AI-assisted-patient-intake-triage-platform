from opentelemetry import trace

from opentelemetry.sdk.trace import (
    TracerProvider
)

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)

trace.set_tracer_provider(
    TracerProvider()
)

span_processor = BatchSpanProcessor(
    ConsoleSpanExporter()
)

trace.get_tracer_provider().add_span_processor(
    span_processor
)

tracer = trace.get_tracer(
    "ai_triage_platform"
)

print("OPEN TELEMETRY INITIALIZED")