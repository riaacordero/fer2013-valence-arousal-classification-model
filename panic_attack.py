import time

# Initialize panic attack variables
is_panic_attack = False
last_emotion_time = time.time()
precursor_detected_flag = False
limit_1min_flag = False
limit_10min_flag = False

# Define value ranges for valence and arousal
valence_ranges = [(-0.8, -0.61), (-0.6, -0.01), (0.0, 0.59), (0.6, 0.8)]
arousal_range = (-0.6, 0.6, 0.8)

def classify_panic_attack(valence: float, arousal: float):
    global is_panic_attack, last_emotion_time, precursor_detected_flag, limit_1min_flag, limit_10min_flag

    # Check if the emotion falls into the specified range
    if any(val_range[0] <= valence <= val_range[1] and arousal_range[0] <= arousal <= arousal_range[1] for val_range in valence_ranges):
        current_time = time.time()

        # Check if it's been 1 minute and 30 seconds since the last emotion change and the message hasn't been displayed
        if current_time - last_emotion_time >= 90 and not precursor_detected_flag:
            precursor_detected_flag = True
            log_message = f"Valence: {valence:.2f}, Arousal: {arousal:.2f} - Potential panic attack precursor detected!"
            return log_message

        # Check if it's been 10 minutes since the last emotion change and the message hasn't been displayed
        if current_time - last_emotion_time >= 600 and not limit_10min_flag:
            is_panic_attack = True
            limit_10min_flag = True
            log_message = f"Valence: {valence:.2f}, Arousal: {arousal:.2f} - Panic attack emotion has reached its 10-minute limit. You might want to take action."
            return log_message

    # Check if the emotion hasn't changed for 1 minute and the message hasn't been displayed
    current_time = time.time()
    if current_time - last_emotion_time >= 60 and not limit_1min_flag:
        limit_1min_flag = True
        log_message = f"Valence: {valence:.2f}, Arousal: {arousal:.2f} - Panic attack emotion has reached its 1-minute limit. You might want to take action."
        return log_message

    # Reset flags if a new emotion is detected
    if precursor_detected_flag or limit_1min_flag or limit_10min_flag:
        precursor_detected_flag = False
        limit_1min_flag = False
        limit_10min_flag = False

    last_emotion_time = current_time
    return None
