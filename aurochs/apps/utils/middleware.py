from django_brotli.middleware import BrotliMiddleware


class SafeBrotliMiddleware(BrotliMiddleware):
    """django-brotli 0.4.0 crashes on streaming responses (binary files)
    because compress_stream() tries .decode("utf-8") on raw bytes.
    WhiteNoise already handles static file compression, so we just
    skip streaming responses entirely."""

    def process_response(self, request, response):
        if response.streaming:
            return response
        return super().process_response(request, response)


def show_toolbar_callback(request):
    return request.GET.get("debug", None) == "y"
