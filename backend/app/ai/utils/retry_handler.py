import asyncio


class RetryHandler:

    @staticmethod
    async def retry(
        func,
        retries=2,
        delay=1
    ):

        last_exception = None

        for attempt in range(retries):

            try:

                return await func()

            except Exception as e:

                last_exception = e

                if attempt < retries - 1:

                    await asyncio.sleep(delay)

        raise last_exception