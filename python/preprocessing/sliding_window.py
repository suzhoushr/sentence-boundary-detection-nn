import numpy

from common.sbd_config import config

from nlp_pipeline import Punctuation, NlpPipeline
from text import Sentence, Text
from tokens import PunctuationToken
from training_instance import TrainingInstance

WINDOW_SIZE = config.getint('windowing', 'window_size')
PUNCTUATION_POS = config.getint('windowing', 'punctuation_position')

class SlidingWindow(object):

    def list_windows(self, talk):
        tokens = talk.get_tokens()

        index = 0
        training_instances = []

        while index <= len(tokens) - WINDOW_SIZE:
            window_tokens = []
            instance_label = Punctuation.NONE

            i = index
            word_count = 0
            while word_count < WINDOW_SIZE and i < len(tokens):
                current_token = tokens[i]
                is_punctuation = current_token.is_punctuation()

                # if there are two punctuations in a row, the last punctuation token is taken

                if not is_punctuation:
                    word_count += 1
                    window_tokens.append(current_token)
                elif i == index:
                    index += 1  ##dont parse windows with punctuations at the beginning twice

                if word_count == PUNCTUATION_POS and is_punctuation:
                    instance_label = current_token.punctuation_type

                i += 1

            if len(window_tokens) == WINDOW_SIZE:
                training_instances.append(TrainingInstance(window_tokens, instance_label))
            index += 1

        return training_instances



################
# Example call #
################

def main():
    nlp_pipeline = NlpPipeline()

    sentence = Sentence()
    sentence.set_sentence_text(unicode("I'm a savant, or more precisly, a high-functioning autisitic savant"))
    sentence.set_tokens(nlp_pipeline.parse_text(sentence.sentence_text))

    text = Text()
    text.add_sentence(sentence)

    slidingWindow = SlidingWindow()
    windows = slidingWindow.list_windows(text)

    for window in windows:
        print(window)

if __name__ == '__main__':
    main()