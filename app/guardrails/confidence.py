MIN_RESULTS = 2

def is_low_confidence(docs):

    if docs is None:
        return True

    if len(docs) < MIN_RESULTS:
        return True

    return False