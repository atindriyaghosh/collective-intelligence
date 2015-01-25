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

MOVIES = ['Seven Samurai', 'Taxi Driver',
          'Usual Suspects, The', 'Clerks',
          'Batman Forever', 'Nosferatu']


def calc_cosine_sim(user1, user2):
    """
    Calculates the Cosine Similarity between user1 and user2.
    """

    def calc_length(user):
        return sqrt(sum(
            pow(RATINGS[user][movie], 2) for movie in RATINGS[
                user]))
    user1_length = calc_length(user1)
    user2_length = calc_length(user2)
    dot_prod = 0
    for movie in MOVIES:
        dot_prod += RATINGS[user1].get(
            movie, 0) * RATINGS[user2].get(movie, 0)

    sim_score = dot_prod / (user1_length * user2_length)

    return sim_score

if __name__ == '__main__':
    SIMILARITY_SCORE = calc_cosine_sim("User1", "User2")
    print SIMILARITY_SCORE
