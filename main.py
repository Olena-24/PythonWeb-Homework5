import argparse
import asyncio
from datetime import datetime, timedelta
import aiohttp

async def fetch_currency_rate(date, currency_codes=['USD', 'EUR']):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime("%d.%m.%Y")}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            rates = {}
            for rate in data['exchangeRate']:
                if 'currency' in rate and rate['currency'] in currency_codes:
                    rates[rate['currency']] = {
                        'sale': rate.get('saleRate', rate.get('saleRateNB')),
                        'purchase': rate.get('purchaseRate', rate.get('purchaseRateNB'))
                    }
            return {date.strftime("%d.%m.%Y"): rates}

async def main(days, currencies):
    tasks = [fetch_currency_rate(datetime.now() - timedelta(days=day), currencies) for day in range(1, days + 1)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get currency exchange rates for the last N days.')
    parser.add_argument('days', type=int, help='Number of days to get rates for')
    parser.add_argument('--currencies', nargs='+', help='List of currencies to get rates for', default=['USD', 'EUR'])

    args = parser.parse_args()

    asyncio.run(main(args.days, args.currencies))