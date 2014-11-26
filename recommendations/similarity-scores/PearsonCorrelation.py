from math import sqrt

ratings = {
    'User1': {
        'Seven Samurai': 4, 'Taxi Driver': 3,
        'Usual Suspects, The': 3, 'Clerks': 1,
        'Batman Forever': 2, 'Nosferatu': 4},
    'User2': {
        'Seven Samurai': 2, 'Taxi Driver': 4,
        'Usual Suspects, The': 5, 'Clerks': 3,
        'Batman Forever': 1}}


def calcPearsonSim(user1, user2):
    """
    Calculates the Pearson Similarity between user1 and user2
    """
    def calcSqrtExpr(n, a, b):
        return sqrt(n * a - pow(b, 2))
    prodSum = 0
    sum1 = 0
    sum2 = 0
    sum1Sq = 0
    sum2Sq = 0
    n = 0
    for movie in ratings[user1]:
        if movie in ratings[user2]:
            rating1 = ratings[user1][movie]
            rating2 = ratings[user2][movie]
            prodSum += rating1 * rating2
            sum1 += rating1
            sum2 += rating2
            sum1Sq += pow(rating1, 2)
            sum2Sq += pow(rating2, 2)
            n += 1
    num = n * prodSum - sum1 * sum2
    denom = calcSqrtExpr(n, sum1Sq, sum1) * calcSqrtExpr(n, sum2Sq, sum2)
    r = 0
    if denom > 0:
        r = num / denom
    return r

if __name__ == '__main__':
    similarityScore = calcPearsonSim("User1", "User2")
    print similarityScore
