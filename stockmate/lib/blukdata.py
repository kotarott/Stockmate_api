import fmp_api as fmp
import threading
import queue


class Bulk_ndx:
    def __init__(self):
        self.get_ndx_list()
        self.results = []
        self.final = []
    
    def get_ndx_list(self):
        self.ndx = fmp.get_ndx_list()
    
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


if __name__ == '__main__':
    # bulk = Bulk_ndx()
    # bulk.get_ndx_feature_v2()
    # print('all : ', len(bulk.ndx))
    # print('final : ', len(bulk.final))
    # pass