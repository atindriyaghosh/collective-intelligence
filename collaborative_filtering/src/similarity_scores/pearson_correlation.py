from math import sqrt

RATINGS = {
    'User1': {
        'Seven Samurai': 4, 'Taxi Driver': 3,
        'Usual Suspects, The': 3, 'Clerks': 1,
        'Batman Forever': 2, 'Nosferatu': 4},
    'User2': {
        'Seven Samurai': 2, 'Taxi Driver': 4,
        'Usual Suspects, The': 5, 'Clerks': 3,
        'Batman Forever': 1}}


def calc_pearson_sim(user1, user2):
    """
    Calculates the Pearson Similarity between user1 and user2.
    """
    def calc_sqrt_expr(n, a, b):
        return sqrt(n * a - pow(b, 2))
    prod_sum = 0
    sum1 = 0
    sum2 = 0
    sum1_sq = 0
    sum2_sq = 0
    n = 0
    for movie in RATINGS[user1]:
        if movie in RATINGS[user2]:
            rating1 = RATINGS[user1][movie]
            rating2 = RATINGS[user2][movie]
            prod_sum += rating1 * rating2
            sum1 += rating1
            sum2 += rating2
            sum1_sq += pow(rating1, 2)
            sum2_sq += pow(rating2, 2)
            n += 1
    num = n * prod_sum - sum1 * sum2
    denom = calc_sqrt_expr(n, sum1_sq, sum1) * calc_sqrt_expr(n, sum2_sq, sum2)
    r = 0
    if denom > 0:
        r = num / denom
    return r

if __name__ == '__main__':
    SIM_SCORE = calc_pearson_sim("User1", "User2")
    print SIM_SCORE
