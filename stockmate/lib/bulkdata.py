# import stockmate.lib.fmp_api as fmp
import fmp_api as fmp
import threading
import queue


class Bulk_ndx:
    def __init__(self):
        self.get_ndx_list()
        self.get_ndx_price()
        self.results = []
        self.final = []
        self.symbol = '^NDX'
    
    def get_ndx_list(self):
        self.ndx = fmp.get_ndx_list()
        self.holdings = len(self.ndx)
    
    def worker_metric(self, q):
        queue = q.get()
        metric = fmp.get_key_metric(queue['symbol'])
        try:
            queue.update(metric[0])
            self.results.append(queue)
        except Exception:
            print(queue['symbol'], ' does not exist.')
        q.task_done()

    def worker_metric(self, q):
        queue = q.get()
        growth = fmp.get_financial_growth(queue['symbol'])
        try:
            queue.update(growth[0])
            self.final.append(queue)
        except Exception:
            print(queue['symbol'], ' does not exist.')
        q.task_done()

    def worker_outlook(self, q):
        queue = q.get()
        outlook = fmp.get_company_outlook(queue['symbol'])
        try:
            queue.update(outlook)
            self.final.append(queue)
        except Exception:
            print(queue['symbol'], ' does not exist.')
        q.task_done()

    def get_ndx_feature(self):
        # key_metric
        for i in range(0, len(self.ndx), 10):
            q = queue.Queue()
            for item in self.ndx[i:i+10]:
                q.put(item)
            while not q.empty():
                thread = threading.Thread(target=self.worker_metric, args=(q,))
                thread.start()
            q.join()

        # growth
        for i in range(0, len(self.results), 10):
            q2 = queue.Queue()
            for item in self.results[i:i+10]:
                q2.put(item)
            while not q2.empty():
                thread = threading.Thread(target=self.worker_growth, args=(q2,))
                thread.start()
            q2.join()

    def get_ndx_feature_v2(self):
        for i in range(0, len(self.ndx), 20):
            q = queue.Queue()
            for item in self.ndx[i:i+20]:
                q.put(item)
            while not q.empty():
                thread = threading.Thread(target=self.worker_outlook, args=(q,))
                thread.start()
            q.join()
    
    def calc_weight(self):
        self.totalCap = sum([data.get('profile', {}).get('mktCap') for data in self.final])
        for key, value in enumerate(self.final):
            try:
                weight = value.get('profile', {}).get('mktCap') / self.totalCap
            except Exception:
                weight = 0
            self.final[key]['weight'] = weight * 100
    
    def get_ndx_price(self):
        quote = fmp.get_quote(self.symbol)
        self.price = quote[0]['price']
        self.changes = quote[0]['changesPercentage']


if __name__ == '__main__':
    # bulk = Bulk_ndx()
    # bulk.get_ndx_feature_v2()
    # bulk.calc_weight()
    # print('all : ', len(bulk.ndx))
    # print('final : ', len(bulk.final))
    pass