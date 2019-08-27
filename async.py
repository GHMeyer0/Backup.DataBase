import asyncio

async def ola_mundo():
    print('Olá ...')
    await asyncio.sleep(1)
    print('... Mundo!')

asyncio.run(ola_mundo())
