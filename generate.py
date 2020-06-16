#!/usr/bin/env python3

import random

def generate_normal(n, mean, standard_deviation, minimum=None, maximum=None):
    """Generates random data according to a normal distribution."""

    for _ in range(n):
        data_point = random.gauss(mean, standard_deviation)
        if minimum:
            data_point = max(data_point, minimum)
        if maximum:
            data_point = min(data_point, maximum)
        yield data_point

def generate_heart_rates(n):
    """Generates random heart rate data according to a normal distribution."""
    # https://www.researchgate.net/figure/A-Mean-and-standard-deviation-of-participants-heart-rate-obtained-from-TOI-and_fig5_323013847
    return generate_normal(n, mean=70.59, standard_deviation=8.36)

if __name__ == "__main__":
    # Call random.seed(x) if we need to generate consistent results.
    for x in generate_heart_rates(10):
        print(x)