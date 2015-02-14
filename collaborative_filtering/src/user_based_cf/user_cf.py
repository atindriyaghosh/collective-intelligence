import csv
from decimal import Decimal, getcontext
import io
from math import sqrt


class UserBasedCF(object):

    """
    The UserBasedCF class is responsible for providing recommendations based on
    one of the following three algorithms
    1. Euclidian Distance
    2. Pearson Correlation
    3. Cosine Similarity
    """

    def __init__(self, movies, ratings):
        self._items = {}
        self._ratings = {}
        self._load_items(movies)
        self._load_ratings(ratings)
        getcontext().prec = 2

    def _load_items(self, path):
        with io.open(path, "rb") as f_name:
            reader = csv.reader(f_name, delimiter="|")
            for row in reader:
                self._items[row[0]] = row[1]

    def _load_ratings(self, path):
        with io.open(path, "rb") as f_name:
            reader = csv.reader(f_name, delimiter="\t")
            for row in reader:
                self._ratings.setdefault(row[0], {})[row[1]] = int(row[2])

    def calc_euclidean_sim(self, user1, user2):
        similar_movies = [movie for movie in self._ratings[user1]
                          if movie in self._ratings[user2]]

        similarity_score = 0

        if len(similar_movies) != 0:
            eucl_distance = Decimal(sum(
                pow(self._ratings[user1][movie] -
                    self._ratings[user2][movie], 2)
                for movie in similar_movies))

            similarity_score = 1 / (1 + eucl_distance)

        return similarity_score

    def calc_pearson_sim(self, user1, user2):
        def calc_denom(n, a, b):
            return sqrt(n * a - pow(b, 2))
        prod_sum = 0
        sum1 = 0
        sum2 = 0
        sum1_sq = 0
        sum2_sq = 0
        n = 0
        for movie in self._ratings[user1]:
            if movie in self._ratings[user2]:
                rating1 = self._ratings[user1][movie]
                rating2 = self._ratings[user2][movie]
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

    def calc_cosine_sim(self, user1, user2):
        def calc_length(user):
            return sqrt(sum(
                pow(self._ratings[user][movie], 2) for movie in self._ratings[
                    user]))
        user1_length = calc_length(user1)
        user2_length = calc_length(user2)
        dot_prod = 0
        for movie in self._items:
            dot_prod += self._ratings[user1].get(
                movie, 0) * self._ratings[user2].get(
                movie, 0)

        similarity_score = dot_prod / (user1_length * user2_length)

        return float(similarity_score)

    def calc_similarity(self, user1, user2, sim_algo):
        sim = 0.0
        if sim_algo == "eucl":
            sim = self.calc_euclidean_sim(user1, user2)
        elif sim_algo == "pearson":
            sim = self.calc_pearson_sim(user1, user2)
        elif sim_algo == "cosine":
            sim = self.calc_cosine_sim(user1, user2)

        return sim

    def gen_recomm(self, user, sim_algo, num_recs=3):
        """Generates recommendations based on the following inputs
            1. User for whom recommendations are to be provided
            2. Recommendation algorithm to use
               eucl - Euclidian distance
               pearson - Pearson correlation
               cosine - Cosine similarity
            3. Maximum number of recommendations
        """
        total_weights = {}
        sim_sum = {}
        for other_user in self._ratings.keys():
            if user != other_user:
                # Calculate similarity scores according to passed algorithm
                # name.
                sim = self.calc_similarity(user, other_user, sim_algo)
                if sim > 0:
                    for movie in self._ratings[other_user]:
                        if movie not in self._ratings[user] and self._ratings[
                                other_user][movie] > 0:
                            total_weights.setdefault(movie, 0)
                            sim_sum.setdefault(movie, 0)
                            total_weights[movie] += sim * \
                                self._ratings[other_user][movie]
                            sim_sum[movie] += sim

        recomm_movies = [(movie, (weight / sim_sum[movie]))
                         for movie, weight in total_weights.items()]

        recomm_movies = sorted(recomm_movies, key=lambda x: x[1])
        recomm_movies.reverse()
        recomm_movies = [(i + 1, self._items[MOVIES[0]])
                         for i, MOVIES in enumerate(recomm_movies[:num_recs])]
        return recomm_movies

if __name__ == '__main__':
    USER_BASED_CF = UserBasedCF(
        movies="../data/u.item",
        ratings="../data/u.data")
    print "User = 1945"
    print "\nAlgorithm = Euclidean"
    print USER_BASED_CF.gen_recomm("1945", "eucl", 15)
    print "\nAlgorithm = Pearson"
    print USER_BASED_CF.gen_recomm("1945", "pearson", 15)
    print "\nAlgorithm = Cosine"
    print USER_BASED_CF.gen_recomm("1945", "cosine", 15)
