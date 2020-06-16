#!/usr/bin/env python3

import json
import random
from datetime import datetime, timedelta

def generate_random(mean, standard_deviation, minimum=None, maximum=None):
    """Generates a random number according to a normal distribution."""
    data_point = random.gauss(mean, standard_deviation)
    if minimum:
        data_point = max(data_point, minimum)
    if maximum:
        data_point = min(data_point, maximum)
    return data_point

def generate_heart_rate():
    """Generates random heart rate data according to a normal distribution."""
    # https://www.researchgate.net/figure/A-Mean-and-standard-deviation-of-participants-heart-rate-obtained-from-TOI-and_fig5_323013847
    return generate_random(mean=70.59, standard_deviation=8.36)

def get_datetime_days_ago(days):
    return datetime.now() - timedelta(days=days)

def generate_observations(patient_id, number_of_observations):
    for i in range(number_of_observations):
        effective_date = get_datetime_days_ago(number_of_observations - i - 1)
        heart_rate = generate_heart_rate()
        yield create_observation(patient_id, heart_rate, effective_date)

def create_observation(patient_id, heart_rate, effective_date):
    # https://www.hl7.org/fhir/vitalsigns.html
    # https://www.hl7.org/fhir/heartrate.html
    return {
        "subject": {"reference": patient_id},
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "8867-4",
                "display": "Heart rate"
            }]
        },
        "category": [{
            "coding": [{
                "system": "http://hl7.org/fhir/ValueSet/observation-category",
                "code": "vital-signs"
            }]
        }],
        "effectiveDateTime": effective_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "valueQuantity": {
            "value": heart_rate,
            "unit": "beats/minute",
            "system": "http://unitsofmeasure.org",
            "code": "/min"
        }
    };


if __name__ == "__main__":
    # Call random.seed(x) if we need to generate consistent results.

    for x in generate_observations("Patient/123", 2):
        print(json.dumps(x))