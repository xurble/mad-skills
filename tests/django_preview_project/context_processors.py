def sample_context(request):
    return {
        "middleware_marker": getattr(request, "sample_middleware_marker", "missing"),
        "processor_marker": "context-processor-active",
        "user": getattr(request, "user", None),
    }
