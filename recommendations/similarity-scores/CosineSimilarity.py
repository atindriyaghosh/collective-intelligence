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


def calcCosineSim(user1, user2):
    """
    Calculates the Cosine Similarity between user1 and user2
    """

    def calcLength(user):
        return sqrt(sum(
            pow(ratings[user][movie], 2) for movie in ratings[
                user]))
    user1Length = calcLength(user1)
    user2Length = calcLength(user2)
    dotProd = 0
    for movie in movies:
        dotProd += ratings[user1].get(
            movie, 0) * ratings[user2].get(
            movie, 0)

    similarityScore = dotProd / (user1Length * user2Length)

    return similarityScore

if __name__ == '__main__':
    similarityScore = calcCosineSim("User1", "User2")
    print similarityScore
