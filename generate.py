#!/usr/bin/env python3

import json
import random
from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# https://www.researchgate.net/figure/A-Mean-and-standard-deviation-of-participants-heart-rate-obtained-from-TOI-and_fig5_323013847
HEART_RATE_BASE_MEAN = 70.59
HEART_RATE_STANDARD_DEVIATION = 8.36

def generate_random(mean, standard_deviation, minimum=None, maximum=None):
    """Generates a random number according to a normal distribution."""
    data_point = random.gauss(mean, standard_deviation)
    if minimum:
        data_point = max(data_point, minimum)
    if maximum:
        data_point = min(data_point, maximum)
    return data_point

def get_datetime_days_ago(days):
    return datetime.now() - timedelta(days=days)

def generate_heart_rate_observations(patient_id, number_of_observations):
    """Generates daily FHIR Observations. The measured heart rate starts normal but spikes at the end."""

    for i in range(number_of_observations):
        effective_date = get_datetime_days_ago(number_of_observations - i - 1)
        if i == number_of_observations-1:
            # Spike at the end.
            mean = HEART_RATE_BASE_MEAN + 4*HEART_RATE_STANDARD_DEVIATION
            standard_deviation = HEART_RATE_STANDARD_DEVIATION / 2
        else:
            mean = HEART_RATE_BASE_MEAN + HEART_RATE_STANDARD_DEVIATION * pow(i / number_of_observations, 2) / 2
            standard_deviation = HEART_RATE_STANDARD_DEVIATION
        heart_rate = generate_random(mean=mean, standard_deviation=standard_deviation, minimum=0)
        yield create_heart_rate_observation(patient_id, heart_rate, effective_date)

def create_heart_rate_observation(patient_id, heart_rate, effective_date):
    # https://www.hl7.org/fhir/vitalsigns.html
    # https://www.hl7.org/fhir/heartrate.html
    return {
        "resourceType": "Observation",
        "status": "final",
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
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
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
    }

def persist_observation_to_server(fhir_server_base_url, observation):
    observation_url = "{}/Observation".format(fhir_server_base_url)
    body = json.dumps(observation).encode("utf8")
    headers = {
        "Content-Type": "application/fhir+json"
    }
    request = Request(observation_url, body, headers)
    return urlopen(request).read().decode()

if __name__ == "__main__":
    # Call random.seed(x) if we need to generate consistent results.

    fhir_server = "http://hapi.fhir.org/baseR4" # Just for testing
    for observation in generate_heart_rate_observations("Patient/example", 10):
        print(json.dumps(observation))
        # print(persist_observation_to_server(fhir_server, observation))