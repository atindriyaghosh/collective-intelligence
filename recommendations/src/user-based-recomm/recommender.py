import csv
from decimal import Decimal, getcontext
import io
from math import sqrt


class Recommender:

    """
    The Recommender class is responsible for providing recommendations based on
    one of the following three algorithms
    1. Euclidian Distance
    2. Pearson Correlation
    3. Cosine Similarity
    """

    def __init__(self, movies, ratings):
        self._items = {}
        self._ratings = {}
        self._loadItems(movies)
        self._loadRatings(ratings)
        getcontext().prec = 2

    def _loadItems(self, path):
        with io.open(path, "rb") as f:
            reader = csv.reader(f, delimiter="|")
            for row in reader:
                self._items[row[0]] = row[1]

    def _loadRatings(self, path):
        with io.open(path, "rb") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                self._ratings.setdefault(row[0], {})[row[1]] = int(row[2])

    def _calcEuclideanSim(self, user1, user2):
        similarMovies = [movie for movie in self._ratings[user1]
                         if movie in self._ratings[user2]]

        similarityScore = 0

        if(len(similarMovies) != 0):
            euclDistance = Decimal(sum(
                pow(self._ratings[user1][movie] -
                    self._ratings[user2][movie], 2)
                for movie in similarMovies))

            similarityScore = 1 / (1 + euclDistance)

        return similarityScore

    def _calcPearsonSim(self, user1, user2):
        def calcDenom(n, a, b):
            return sqrt(n * a - pow(b, 2))
        prodSum = 0
        sum1 = 0
        sum2 = 0
        sum1Sq = 0
        sum2Sq = 0
        n = 0
        for movie in self._ratings[user1]:
            if movie in self._ratings[user2]:
                rating1 = self._ratings[user1][movie]
                rating2 = self._ratings[user2][movie]
                prodSum += rating1 * rating2
                sum1 += rating1
                sum2 += rating2
                sum1Sq += pow(rating1, 2)
                sum2Sq += pow(rating2, 2)
                n += 1
        num = n * prodSum - sum1 * sum2
        denom = calcDenom(n, sum1Sq, sum1) * calcDenom(n, sum2Sq, sum2)
        r = 0
        if denom > 0:
            r = num / denom
        return r

    def _calcCosineSim(self, user1, user2):
        def calcLength(user):
            return sqrt(sum(
                pow(self._ratings[user][movie], 2) for movie in self._ratings[
                    user]))
        user1Length = calcLength(user1)
        user2Length = calcLength(user2)
        dotProd = 0
        for movie in self._items:
            dotProd += self._ratings[user1].get(
                movie, 0) * self._ratings[user2].get(
                movie, 0)

        similarityScore = dotProd / (user1Length * user2Length)

        return float(similarityScore)

    def _calcSimilarity(self, user1, user2, simAlgo):
        sim = 0.0
        if(simAlgo == "eucl"):
            sim = self._calcEuclideanSim(user1, user2)
        elif(simAlgo == "pearson"):
            sim = self._calcPearsonSim(user1, user2)
        elif(simAlgo == "cosine"):
            sim = self._calcCosineSim(user1, user2)

        return sim

    def genRecommendations(self, user, simAlgo, numRecs=3):
        """Generates recommendatons based on the following inputs
            1. User for whom recommendations are to be provided
            2. Recommendation algorithm to use
               eucl - Euclidian distance
               pearson - Pearson correlation
               cosine - Cosine similarity
            3. Maximum number of recommendations
        """
        totalWeights = {}
        simSum = {}
        for other_user in self._ratings.keys():
            if(user != other_user):
                # Calculate similarity scores according to passed algorithm
                # name.
                sim = self._calcSimilarity(user, other_user, simAlgo)
                if(sim > 0):
                    for movie in self._ratings[other_user]:
                        if movie not in self._ratings[user] and self._ratings[
                                other_user][movie] > 0:
                            totalWeights.setdefault(movie, 0)
                            simSum.setdefault(movie, 0)
                            totalWeights[movie] += sim * \
                                self._ratings[other_user][movie]
                            simSum[movie] += sim

        recommMovies = [(movie, (weight / simSum[movie]))
                        for movie, weight in totalWeights.items()]

        recommMovies = sorted(recommMovies, key=lambda x: x[1])
        recommMovies.reverse()
        recommMovies = [(i + 1, self._items[movies[0]])
                        for i, movies in enumerate(recommMovies[:numRecs])]
        return recommMovies

if __name__ == '__main__':
    recommender = Recommender(
        movies="../data/u.item",
        ratings="../data/u.data")
    print "User = 1945"
    print "\nAlgorithm = Euclidean"
    print recommender.genRecommendations("1945", "eucl", 15)
    print "\nAlgorithm = Pearson"
    print recommender.genRecommendations("1945", "pearson", 15)
    print "\nAlgorithm = Cosine"
    print recommender.genRecommendations("1945", "cosine", 15)
