import time


class RequestTimingMiddleware:
    """تقيس زمن معالجة كل طلب وتضعه في ترويسة الاستجابة."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        response = self.get_response(request)
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        response["X-Response-Time-ms"] = f"{elapsed_ms:.2f}"
        return response
