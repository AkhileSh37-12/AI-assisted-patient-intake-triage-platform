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
import logging

logging.getLogger(
    "httpx"
).setLevel(
    logging.WARNING
)

logging.getLogger(
    "sentence_transformers"
).setLevel(
    logging.WARNING
)

logging.getLogger(
    "huggingface_hub"
).setLevel(
    logging.WARNING
)

logging.getLogger(
    "opentelemetry"
).setLevel(
    logging.ERROR
)

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler
)

from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor
)

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter
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

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name":
            "ai-triage-platform"
        }
    )
)
from opentelemetry._logs import (
    set_logger_provider
)

set_logger_provider(
    logger_provider
)

logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        OTLPLogExporter(
            endpoint="host.docker.internal:4317",
            insecure=True
        )
    )
)



handler = LoggingHandler(
    level=logging.INFO,
    logger_provider=logger_provider
)

logger = logging.getLogger(
    "ai_triage_platform"
)

logger.setLevel(
    logging.INFO
)

logger.addHandler(
    handler
)

logger.propagate = False