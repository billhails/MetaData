const { Sampler, SpanKind } = require("@opentelemetry/api");
const opentelemetry = require('@opentelemetry/api');
const { AlwaysOnSampler } = require('@opentelemetry/core');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { Resource } = require('@opentelemetry/resources');
const { SemanticAttributes, SemanticResourceAttributes: ResourceAttributesSC } = require('@opentelemetry/semantic-conventions');
const { SpanAttributes } = require("@opentelemetry/api/build/src/trace/attributes");
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { GraphQLInstrumentation } = require('@opentelemetry/instrumentation-graphql');

function filterSampler(filterFn, parent) {
  return {
    shouldSample(ctx, tid, spanName, spanKind, attr, links) {
      if (!filterFn(spanName, spanKind, attr)) {
        return { decision: opentelemetry.SamplingDecision.NOT_RECORD };
      }
      return parent.shouldSample(ctx, tid, spanName, spanKind, attr, links);
    },
    toString() {
      return `FilterSampler(${parent.toString()})`;
    }
  }
}

function ignoreHealthCheck(spanName, spanKind, attributes) {
  return spanKind !== opentelemetry.SpanKind.SERVER || attributes[SemanticAttributes.HTTP_ROUTE] !== "/health";
}

module.exports = (serviceName, traceGraphQL=false) => {
  const provider = new NodeTracerProvider({
    resource: new Resource({
      [ResourceAttributesSC.SERVICE_NAME]: serviceName,
    }),
    sampler: filterSampler(ignoreHealthCheck, new AlwaysOnSampler()),
  });
  registerInstrumentations({
    tracerProvider: provider,
    instrumentations: [
      // Express instrumentation expects HTTP layer to be instrumented
      HttpInstrumentation,
      ExpressInstrumentation,
      ...(traceGraphQL ? [new GraphQLInstrumentation({})] : [])
    ],
  });

  const exporter = new JaegerExporter({
    serviceName,
  });

  provider.addSpanProcessor(new SimpleSpanProcessor(exporter));


  // Initialize the OpenTelemetry APIs to use the NodeTracerProvider bindings
  provider.register();

  return opentelemetry.trace.getTracer(serviceName);
};