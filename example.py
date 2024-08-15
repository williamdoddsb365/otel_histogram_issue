import random
from time import sleep, time

from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import Histogram, MeterProvider
from opentelemetry.sdk.metrics.export import (AggregationTemporality,
                                              ConsoleMetricExporter,
                                              PeriodicExportingMetricReader)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from opentelemetry.semconv.resource import ResourceAttributes

_histograms = {}


def generate_data():
    operation_start_time = time()

    # here is where an operation would occur
    print("sleeping for 10 seconds")
    sleep(10)

    # record the duration of the operation and record a dynamic attribute
    record_histogram(
        metric_name=HistogramNames.CUSTOM_OPERATION_DURATION,
        start_time=operation_start_time,
        # attributes={"dynamic_attribute": 1})  # comment out to record dynamic value
        attributes={"dynamic_attribute": random.randint(1, 999)})  # uncomment out to record dynamic value


class HistogramNames:
    CUSTOM_OPERATION_DURATION = 'custom.operation.duration'


def otel():
    resource = Resource.create(attributes={
        ResourceAttributes.SERVICE_NAMESPACE: 'name',
    })
    temporality = {
        Histogram: AggregationTemporality.DELTA,
    }
    trace_provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace_provider.add_span_processor(processor)
    trace.set_tracer_provider(trace_provider)
    reader = PeriodicExportingMetricReader(exporter=ConsoleMetricExporter(preferred_temporality=temporality))
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)


def create_histogram(name: str, description: str, unit: str = "s") -> Histogram:
    if name in _histograms:
        return _histograms[name]

    histogram = metrics.get_meter(__name__).create_histogram(
        name=name,
        description=description,
        unit=unit
    )
    _histograms[name] = histogram
    return histogram


def record_histogram(metric_name: str, start_time: float, **kwargs):
    duration = time() - start_time
    attributes = kwargs.get('attributes', {})
    if metric_name not in _histograms:
        print("no histogram found in _histograms")
        return
    _histograms[metric_name].record(duration, attributes)


if __name__ == "__main__":
    print("setting up OTEL instrumentation")
    otel()
    create_histogram(HistogramNames.CUSTOM_OPERATION_DURATION, "Duration of a custom operation")
    while True:
        print("Running an operation and recording a histogram")
        generate_data()
        print("Histogram data generated")
