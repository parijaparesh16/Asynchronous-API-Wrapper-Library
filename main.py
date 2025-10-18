import aiohttp # type: ignore
import asyncio

class AsyncAPIWrapper:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}

    async def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

    async def get(self, endpoint, params=None):
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint, data=None, json=None):
        return await self._request("POST", endpoint, data=data, json=json)

    async def put(self, endpoint, data=None, json=None):
        return await self._request("PUT", endpoint, data=data, json=json)

    async def delete(self, endpoint):
        return await self._request("DELETE", endpoint)


# Example usage
async def main():
    api = AsyncAPIWrapper("https://jsonplaceholder.typicode.com")
    posts = await api.get("/posts")
    print(posts[:2])

    new_post = await api.post("/posts", json={
        "title": "Async API Wrapper Test",
        "body": "Hello, this is a test!",
        "userId": 1
    })
    print(new_post)

asyncio.run(main())