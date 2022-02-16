from django.core.management.base import BaseCommand

from ...models import Symbol, KeyMetric
from stockmate.lib.bulkdata import Bulk_ndx

class Command(BaseCommand):
    help = 'Update NDX Data.'

    def handle(self, *args, **options):
        ndx = Bulk_ndx()
        ndx.get_ndx_feature_v2()
        ndx.calc_weight()
        metrics = []
        # totalFeature = {
        #     'cap': 0,
        #     'peRatio': 0,
        #     'opGrowth': 0,
        #     'roe': 0,
        #     'deRatio': 0,
        # }
        for item in ndx.final:
            try:
                symbol = Symbol.objects.get(symbol=item['symbol'])
            except Exception:
                symbol = Symbol.objects.create(
                    symbol = item['symbol'],
                    image = item['profile']['image'],
                    description = item['profile']['companyName'],
                    currency = item['profile']['currency'],
                    symbol_type = 'Common_Stock',
                    exchange = item['profile']['exchange'],
                    industry = item['profile']['industry'],
                    sector = item['profile']['sector'],
                    vender = 'FMP'
                )
            try:
                growth = item['financialsAnnual']['income'][0]['operatingIncome'] / item['financialsAnnual']['income'][1]['operatingIncome'] - 1
            except Exception:
                growth = None
            
            s = KeyMetric(
                symbol = symbol,
                price = item['profile']['price'],
                changes = item['profile']['changes'],
                cap = item['profile']['mktCap'],
                peRatio = item['ratios'][0]['peRatioTTM'],
                opGrowth = growth * 100,
                roe = item['ratios'][0]['returnOnEquityTTM'] * 100,
                deRation = item['ratios'][0]['debtEquityRatioTTM']
            )
            metrics.append(s)
        
        KeyMetric.objects.bulk_create(metrics)