# Define value ranges for valence and arousal
valence_ranges = [(-0.8, -0.61), (-0.6, -0.01), (0.0, 0.59), (0.6, 0.8)]
arousal_range = (-0.6, 0.6, 0.8)

def _in_emotion_range(emotion: str | None) -> bool:
    """
    Checks if the emotion is within the specified range
    :param emotion: The emotion
    :return: True if the emotion is within the specified range, False otherwise
    """
    return emotion == "angry" or emotion == "fear" or emotion == "sad"

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
    panic_timeframe_ms = 0
    last_frame_time = 0
    false_emotions_count = 0

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
        self.panic_timeframe_ms = 0
        self.last_frame_time = 0
        self.false_emotions_count = 0

    def classify(self, emotion: str | None, valence: float, arousal: float, current_time: float):
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
        is_in_panic_attack_emotion = _in_emotion_range(emotion)
        print(f"diff: {diff:.2f}ms | in_panic_attack_emotion: {is_in_panic_attack_emotion} | panic_timeframe: {self.panic_timeframe_ms}")

        if is_in_panic_attack_emotion:
            if self.panic_timeframe_ms == 0:
                # Set the last emotion time once if within panic attack emotion
                self.last_emotion_time = current_time

            gap = current_time - self.last_frame_time
            self.panic_timeframe_ms += gap

            # Check if it's been 10 minutes since the last emotion change and the message hasn't been displayed
            if diff >= in_ms(10 * 60) and not self.limit_10min_flag:
                self.is_panic_attack = True
                self.limit_10min_flag = True

                self.last_frame_time = current_time
                return format_log(valence, arousal, "Panic attack emotion has reached its 10-minute limit. You might want to take action.")

            # Check if it's been 30 seconds since the last emotion change and the message hasn't been displayed
            if self.panic_timeframe_ms >= in_ms(15) and not self.precursor_detected_flag:
                self.precursor_detected_flag = True
                self.last_frame_time = current_time
                return format_log(valence, arousal, "Potential panic attack precursor detected!")
        elif self.panic_timeframe_ms != 0:
            # Increase false emotions count
            self.false_emotions_count += 1
            
            if self.false_emotions_count == 10:
                # Change last emotion time if the emotion is not in the specified range
                # Do not change every time. Only reset if panic_timeframe_ms is not 0
                self.last_emotion_time = current_time
                
                # Reset panic timeframe if the emotion is not in the specified range
                self.panic_timeframe_ms = 0
                self.false_emotions_count = 0
                

        # Reset flags if a new emotion is detected
        if self.precursor_detected_flag or self.limit_10min_flag:
            self.precursor_detected_flag = False
            self.limit_10min_flag = False

        self.last_frame_time = current_time
        return None
