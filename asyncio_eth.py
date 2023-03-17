import asyncio
import aiohttp
from key import key
#import time

while True:

    #start_time = time.time()

    async def get_info(session, url):
        async with session.get(url) as response:
            #await asyncio.sleep(1/10)
            #Здесь я пытался нащупать время, какую задержку делать, чтобы не превышать ограничение от API
            return await response.json()

    async def get_all(session):
        urls = [
            f"https://min-api.cryptocompare.com/data/v2/histominute?fsym=ETH&tsym=USDT&limit=60&api_key{key}",
            f"https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USDT&api_key={key}",
            f"https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USDT&limit=60&api_key{key}",
            f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USDT&api_key={key}"]
        tasks = []
        for task in urls:
            tasks.append(asyncio.create_task(get_info(session, task)))
        results = await asyncio.gather(*tasks)
        return results

    async def main():
        async with aiohttp.ClientSession() as session:
            data = await get_all(session)
            eth_story, eth, btc_story, btc = data[0], data[1], data[2], data[3]
            last_eth = [eth_story["Data"]["Data"][-1]["low"], eth_story["Data"]["Data"][-1]["high"]]
            last_btc = [btc_story["Data"]["Data"][-1]["low"], btc_story["Data"]["Data"][-1]["high"]]
            if eth["USDT"] < last_eth[0] and btc["USDT"] < last_btc[0]:
                #print("Движение ETH зависит от BTC")
                pass
            elif last_eth[1] < eth["USDT"] and last_btc[1] < btc["USDT"]:
                #print("Движение ETH зависит от BTC")
                pass
            elif last_eth[0] < eth["USDT"] < last_eth[1] and last_btc[0] < btc["USDT"] < last_btc[1]:
                #print("Движение ETH зависит от BTC")
                pass
            else:
                low_eth = []
                high_eth = []
                for price in eth_story["Data"]["Data"]:
                    low_eth.append(price["low"])
                    high_eth.append(price["high"])
                if eth["USDT"] / max(high_eth) >= 1.01:
                    print("Наблюдается рост цены на", int(100 - (eth["USDT"]/ max(high_eth)) * 100), "%")
                elif min(low_eth) / eth["USDT"] >= 1.01:
                    print("Наблюдается падение цены на", int(100 - (min(low_eth) / eth["USDT"]) * 100), "%")

                #else:
                    #print("Пока что нет изменений")

    asyncio.run(main())


    #print(time.time() - start_time)