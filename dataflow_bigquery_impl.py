import sys
from string import ascii_lowercase
from typing import Tuple
import os
import apache_beam as beam
from apache_beam.transforms import combiners
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='D:\Pycharm\GCP\key-bigquery-practice-sample-fb58a943c40b.json'

class CalculateFrequency(beam.DoFn):
  def process(self, element, total_characters):
    letter, counts = element
    yield letter, counts / total_characters


def run():
  with beam.Pipeline(argv=sys.argv) as p:
    letters = (
        p
        | beam.io.ReadFromText(
            'gs://apache-beam-samples/shakespeare/romeoandjuliet.txt')
        | beam.FlatMap(
            lambda line: (ch for ch in line.lower()
                          if ch in ascii_lowercase)).with_output_types(str))

    total_characters = letters | combiners.Count.Globally()
    counts = (
        letters
        | beam.Map(lambda ch: (ch, 1)).with_output_types(Tuple[str, int])
        | beam.CombinePerKey(sum))

    _ = (
        counts
        | beam.ParDo(
            CalculateFrequency(),
            beam.pvalue.AsSingleton(total_characters)).with_output_types(
                Tuple[str, float])
        | beam.MapTuple(lambda letter, freq: print(f'{letter}: {freq:.2%}')))


if __name__ == '__main__':
  run()