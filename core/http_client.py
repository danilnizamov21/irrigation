import httpx

_http_client: httpx.AsyncClient | None = None


async def init_http_client() -> httpx.AsyncClient:
    global _http_client
    _http_client = httpx.AsyncClient(timeout=10.0)
    return _http_client


async def close_http_client() -> None:
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None


def get_http_client() -> httpx.AsyncClient:
    if _http_client is None:
        raise RuntimeError("HTTP-клиент не инициализирован")
    return _http_client
