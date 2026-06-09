from opentelemetry import trace

from opentelemetry.sdk.trace import (
    TracerProvider
)

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter
)

from opentelemetry.sdk.resources import (
    Resource
)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create(
            {
                "service.name":
                "ai-triage-platform"
            }
        )
    )
)

span_processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="host.docker.internal:4317",
        insecure=True
    )
)

trace.get_tracer_provider().add_span_processor(
    span_processor
)

tracer = trace.get_tracer(
    "ai_triage_platform"
)

print("OPEN TELEMETRY INITIALIZED")