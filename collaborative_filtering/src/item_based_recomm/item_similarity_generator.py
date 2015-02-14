'''

'''
import csv
from decimal import Decimal, getcontext
import io
from math import sqrt
from multiprocessing import Queue
from multiprocessing.dummy import Pool as ThreadPool
import time

import multiprocessing.dummy as mpd


class SimilarityGenerator(object):

    '''
    classdocs
    '''

    def __init__(self, ratings):
        self._users = set()
        self._ratings = {}
        self._processed_items = set()
        self._threshold = 0
        self._path = "../data/item.sim.data"
        self._load_ratings(ratings)

    def _load_ratings(self, path):
        with io.open(path, "rb") as f_name:
            reader = csv.reader(f_name, delimiter="\t")
            for row in reader:
                self._ratings.setdefault(row[1], {})[row[0]] = int(row[2])
                self._users.add(row[0])

    def calc_euclidean_sim(self, item1, item2):
        similar_users = [user for user in self._ratings[item1]
                         if user in self._ratings[item2]]

        similarity_score = 0

        if len(similar_users) != 0:
            eucl_distance = Decimal(sum(
                pow(self._ratings[item1][user] -
                    self._ratings[item2][user], 2)
                for user in similar_users))

            similarity_score = 1 / (1 + eucl_distance)
        getcontext().prec = 2
        return similarity_score

    def calc_pearson_sim(self, item1, item2):
        def calc_denom(n, a, b):
            return sqrt(n * a - pow(b, 2))
        prod_sum = 0
        sum1 = 0
        sum2 = 0
        sum1_sq = 0
        sum2_sq = 0
        n = 0
        for user in self._ratings[item1]:
            if user in self._ratings[item2]:
                rating1 = self._ratings[item1][user]
                rating2 = self._ratings[item2][user]
                prod_sum += rating1 * rating2
                sum1 += rating1
                sum2 += rating2
                sum1_sq += pow(rating1, 2)
                sum2_sq += pow(rating2, 2)
                n += 1
        num = n * prod_sum - sum1 * sum2
        denom = calc_denom(n, sum1_sq, sum1) * calc_denom(n, sum2_sq, sum2)
        r = 0
        if denom > 0:
            r = num / denom
        return r

    def calc_cosine_sim(self, item1, item2):
        def calc_length(item):
            return sqrt(sum(
                pow(self._ratings[item][user], 2) for user in self._ratings[
                    item]))
        item1_length = calc_length(item1)
        item2_length = calc_length(item2)

        dot_prod = 0
        for user in self._users:
            dot_prod += self._ratings[item1].get(
                user, 0) * self._ratings[item2].get(
                user, 0)

        similarity_score = dot_prod / (item1_length * item2_length)
        getcontext().prec = 2
        return float(similarity_score)

    def calc_similarity(self, item1, item2, sim_algo):
        sim = 0.0
        if sim_algo == "eucl":
            sim = self.calc_euclidean_sim(item1, item2)
        elif sim_algo == "pearson":
            sim = self.calc_pearson_sim(item1, item2)
        elif sim_algo == "cosine":
            sim = self.calc_cosine_sim(item1, item2)

        return sim

    def calc_sim(self, item1, sim_algo):
        sim = []
        for item2 in self._ratings.keys():
            if item1 != item2 and item2 not in self._processed_items:
                # Calculate similarity scores according to passed algorithm
                # name.
                # Append item1:item2 similarity and item2:item1
                # similarity to avoid re-computation.
                similarity_score = self.calc_similarity(
                    item1, item2, sim_algo)
                # if similarity_score > self._threshold:
                sim.append(
                    "|".join([item1, item2, str(similarity_score)]))
                sim.append(
                    "|".join([item2, item1, str(similarity_score)]))

        self._processed_items.add(item1)
        return sim

    def write_sim(self, queue):
        with io.open(self._path, "ab") as f_name:
            while True:
                message = queue.get()
                if not isinstance(message, list) and message == "Completed":
                    break
                f_name.writelines(
                    "%s\n" % item for item in message)

    def gen_item_sim(self, sim_algo, path):
        manager = mpd.Manager()
        queue = manager.Queue()

        def store_sim(item1):
            item_sim = self.calc_sim(item1, sim_algo)
            queue.put(item_sim)

        self._processed_items.clear()
        self._path = path
        pool = ThreadPool(100)
        pool.apply_async(self.write_sim, (queue,))
        pool.map(store_sim, self._ratings.keys(), 200)
        queue.put("Completed")
        pool.close()
        pool.join()


if __name__ == '__main__':
    SIM_GEN = SimilarityGenerator(
        ratings="../data/u.data.test2")
    print "Calculating Item Similarity\n"
    print "Algorithm = Euclidean\n"
    start = time.clock()
    SIM_GEN.gen_item_sim("eucl", "../data/item.sim.eucl.test")
    print time.clock() - start
    print "Algorithm = Pearson\n"
    start = time.clock()
    SIM_GEN.gen_item_sim("pearson", "../data/item.sim.pearson.test")
    print time.clock() - start
    print "Algorithm = Cosine\n"
    start = time.clock()
    SIM_GEN.gen_item_sim("cosine", "../data/item.sim.cosine.test")
    print time.clock() - start
