# Define value ranges for valence and arousal
valence_ranges = [(-0.8, -0.61), (-0.6, -0.01), (0.0, 0.59), (0.6, 0.8)]
arousal_range = (-0.6, 0.6, 0.8)

def _in_emotion_range(valence: float, arousal: float) -> bool:
    """
    Checks if the valence and arousal values fall into the specified range
    :param valence: The valence value
    :param arousal: The arousal value
    :return: True if the valence and arousal values fall into the specified range, False otherwise
    """

    # Check if the valence value falls into the specified range
    for val_range in valence_ranges:
        if val_range[0] <= valence <= val_range[1]:
            # Proceed to check the arousal range
            break
        else:
            return False

    # Check if the arousal value falls into the specified range
    return arousal_range[0] <= arousal <= arousal_range[2]

def format_log(val, arou, message):
    return f"Valence: {val:.2f}, Arousal: {arou:.2f}, {message}"

def in_ms(seconds: float):
    """
    Converts seconds to milliseconds
    :param seconds: The seconds value
    :return: The milliseconds value
    """
    return seconds * 1000

# Make PanicAttackClassifier a class to be able to support simultaneous sessions
class PanicAttackClassifier:
    # Initialize panic attack variables
    is_panic_attack = False
    last_emotion_time = 0
    precursor_detected_flag = False
    limit_10min_flag = False

    def __init__(self):
        pass

    def diff(self, timestamp, log = False):
        d = (timestamp - self.last_emotion_time)
        if log == True:
            print(f"Time difference: {d:.2f}ms", timestamp, self.last_emotion_time)
        return d

    def reset(self):
        self.is_panic_attack = False
        self.last_emotion_time = 0
        self.precursor_detected_flag = False
        self.limit_10min_flag = False

    def classify(self, valence: float, arousal: float, current_time: float):
        if self.last_emotion_time != 0 and current_time < self.last_emotion_time:
            # raise ValueError("Current time cannot be less than the last emotion time")
            return None

        # Set the last emotion time if it's not set
        if self.last_emotion_time == 0:
            self.last_emotion_time = current_time

        # Calculate the time difference between the current time and the last emotion time
        # Must be only computed once to avoid time drift
        diff = self.diff(current_time)

        # Check if the emotion falls into the specified range
        is_in_panic_attack_emotion = _in_emotion_range(valence, arousal)
        print(f"diff: {diff:.2f}ms | in_panic_attack_emotion: {is_in_panic_attack_emotion}")

        if is_in_panic_attack_emotion:
            # Check if it's been 10 minutes since the last emotion change and the message hasn't been displayed
            if diff >= in_ms(10 * 60) and not self.limit_10min_flag:
                self.is_panic_attack = True
                self.limit_10min_flag = True
                return format_log(valence, arousal, "Panic attack emotion has reached its 10-minute limit. You might want to take action.")

            # Check if it's been 30 seconds since the last emotion change and the message hasn't been displayed
            if diff >= in_ms(30) and not self.precursor_detected_flag:
                self.precursor_detected_flag = True
                return format_log(valence, arousal, "Potential panic attack precursor detected!")

        # Reset flags if a new emotion is detected
        if self.precursor_detected_flag or self.limit_10min_flag:
            self.precursor_detected_flag = False
            self.limit_10min_flag = False

        # Check if it's been 30 seconds since the last emotion change and the message hasn't been displayed
        if diff >= in_ms(30):
            self.last_emotion_time = current_time

        return None
