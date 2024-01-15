import math

emotion_to_valence_arousal = {
    'angry': (-0.8, 0.8),
    'sad': (-0.8, -0.6),
    'disgust': (-0.6, -0.6),
    'neutral': (0.0, 0.0),
    'fear': (0.0, 0.8),
    'surprise': (0.6, 0.8),
    'happy': (0.8, 0.6),
}

# Define the value range
min_valence = -1.0
max_valence = 1.0
min_arousal = -1.0
max_arousal = 1.0

def map_emotion(valence: float, arousal: float) -> str | None:
    """
    Maps the valence and arousal values to an emotion
    :param valence: The valence value
    :param arousal: The arousal value
    :return: The emotion
    """
    closest_emotion = None
    min_distance = math.inf
    current_valence = min(max(valence, min_valence), max_valence)
    current_arousal = min(max(arousal, min_arousal), max_arousal)

    # Check if the valence and arousal values are within the specified range
    for emotion, (e_valence, e_arousal) in emotion_to_valence_arousal.items():
        # Calculate the distance between the current valence and arousal values
        # and the emotion's valence and arousal values by using the Euclidean distance formula
        distance = math.sqrt((current_valence - e_valence)**2 + (current_arousal - e_arousal)**2)

        if distance < min_distance:
            min_distance = distance
            closest_emotion = emotion

    return closest_emotion
