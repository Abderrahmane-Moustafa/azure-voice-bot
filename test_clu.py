import asyncio
from clu_utils import analyze_text_with_clu

async def test():
    response = await analyze_text_with_clu("I want to register an account")
    print(response)

if __name__ == "__main__":
    asyncio.run(test())
