from decimal import Decimal, getcontext

ratings = {
    'User1': {
        'Seven Samurai': 4, 'Taxi Driver': 3,
        'Usual Suspects, The': 3, 'Clerks': 1,
        'Batman Forever': 2, 'Nosferatu': 4},
    'User2': {
        'Seven Samurai': 2, 'Taxi Driver': 4,
        'Usual Suspects, The': 5, 'Clerks': 3,
        'Batman Forever': 1}}

getcontext().prec = 2


def calc_euclidean_sim(user1, user2):
    """
    Calculates the Euclidean Similarity between user1 and user2
    """

    # Get the list of similar movies
    similar_movies = [movie for movie in ratings[user1]
                     if movie in ratings[user2]]

    # If there are similar movies calculate similarity score, else similarity
    # score is 0
    similarity_score = 0

    if(len(similar_movies) != 0):
        eucl_distance = Decimal(sum(
            pow(ratings[user1][movie] - ratings[user2][movie], 2)
            for movie in similar_movies))

        similarity_score = 1 / (1 + eucl_distance)

    return similarity_score

if __name__ == '__main__':
    similarity_score = calc_euclidean_sim("User1", "User2")
    print similarity_score
