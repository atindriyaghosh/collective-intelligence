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

movies = ['Seven Samurai', 'Taxi Driver',
          'Usual Suspects, The', 'Clerks',
          'Batman Forever', 'Nosferatu']


def calc_cosine_sim(user1, user2):
    """
    Calculates the Cosine Similarity between user1 and user2
    """

    def calc_length(user):
        return sqrt(sum(
            pow(ratings[user][movie], 2) for movie in ratings[
                user]))
    user1_length = calc_length(user1)
    user2_length = calc_length(user2)
    dot_prod = 0
    for movie in movies:
        dot_prod += ratings[user1].get(
            movie, 0) * ratings[user2].get(
            movie, 0)

    similarity_score = dot_prod / (user1_length * user2_length)

    return similarity_score

if __name__ == '__main__':
    similarity_score = calc_cosine_sim("User1", "User2")
    print similarity_score
