from pyquery import PyQuery as pq
from collections import namedtuple
import click
from prettytable import PrettyTable
import requests

class YoudaoTranslator:
    """
    YouDao Class
    """

    _URL_ = "http://youdao.com/w/eng/{}"

    _VOICE_URL_ = "http://dict.youdao.com/dictvoice?audio={}"

    def __init__(self):
        self._config = {
            'pronounce': self._parse_pronounce, 
            'definition': self._parse_definition, 
            'addition': self._parse_addition, 
            'collins': self._parse_collins_examples
            }

    def _parse_pronounce(self, doc):
        Pronounce = namedtuple('Pronounce', ['transcription', 'voice_url'])
        pronounces = []
        for pron in doc.items('.baav .pronounce'):
            transcription = pron.find('span').eq(0).text().strip()
            voice_url = YoudaoTranslator._VOICE_URL_.format(pron.find('a').eq(0).attr('data-rel'))
            pronounces.append(Pronounce(transcription=transcription, voice_url=voice_url))    
        return pronounces        
            
    def _parse_definition(self, doc):
        definition_doc = doc.items('#phrsListTab .trans-container ul li')
        return [definition.text().strip() for definition in definition_doc]

    def _parse_addition(self, doc):
        return doc('#phrsListTab .trans-container .additional').text().strip()

    def _parse_collins_examples(self, doc):
        cs = []
        Collins = namedtuple('Collins', ['definition', 'examples'])
        for instance in doc.items("#collinsResult #NAMING1 ul li"):
            definition = instance.find('.collinsMajorTrans p').eq(0).text()
            exmaples = []
            for example_doc in instance.items('.examples'):
                ps = example_doc.find('p')
                exmaples.append(f'{ps.eq(0).text().strip()}\t\t{ps.eq(1).text().strip()}')
            cs.append(Collins(definition=definition, examples=exmaples))
        return cs
    
    def _get_content(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        return requests.get(url, headers=headers).text

    def translate(self, word):
        url = YoudaoTranslator._URL_.format(word)
        doc = pq(self._get_content(url))
        Translation = namedtuple("Translation", self._config.keys())
        values = {key: value(doc) for key, value in self._config.items()}
        return Translation(**values)


def _magic(word, translation):
    definition = '\n'.join(translation.definition)
    print(definition)
    print(translation.addition)

@click.command()
@click.argument('word')
def cli(word):
    if not word:
        raise ValueError('please enter english word')
    translation = YoudaoTranslator().translate(word)
    _magic(word, translation)

if __name__ == "__main__":
    cli()