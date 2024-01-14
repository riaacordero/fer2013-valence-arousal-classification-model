import time

# Initialize panic attack variables
recurrence_count = 0
is_panic_attack = False
last_emotion_time = time.time()

# Define value ranges for valence and arousal
valence_ranges = [(-0.8, -0.61), (-0.6, -0.01), (0.0, 0.59), (0.6, 0.8)]
arousal_range = (0.6, 0.8)

def classify_panic_attack(valence: float, arousal: float):
    global recurrence_count, is_panic_attack, last_emotion_time

    # Check if the emotion falls into the specified range
    if any(val_range[0] <= valence <= val_range[1] and arousal_range[0] <= arousal <= arousal_range[1] for val_range in valence_ranges):
        recurrence_count += 1
    else:
        recurrence_count = 0  # Reset recurrence count if emotion is not within the specified range

    # Check if recurrence count reaches 5
    if recurrence_count == 5:
        is_panic_attack = True
        return "Panic attack precursor detected!"

    # Check if recurrence count is beyond 5
    elif recurrence_count > 5:
        return "Potential panic attack emotion is recurring. You might want to take action"

    # Check if the emotion hasn't changed for 1 minute and 30 seconds
    current_time = time.time()
    if current_time - last_emotion_time >= 90:  # Check every 1 minute and 30 seconds
        return "Potential panic attack emotion is not changing. You might want to take action."

    last_emotion_time = current_time
    return None
