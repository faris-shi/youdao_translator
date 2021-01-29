from pyquery import PyQuery as pq
import click
import requests
from rich.console import Console
from rich.markdown import Markdown
from playsound import playsound 

from collections import namedtuple
from time import sleep
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

class YoudaoTranslator:
    """
    YouDao Class
    """

    _URL_ = "http://youdao.com/w/eng/{}"

    _VOICE_URL_ = "http://dict.youdao.com/dictvoice?audio={}"

    def __init__(self):
        self._config = {
            'pronounces': self._parse_pronounce, 
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
        for instance in doc.items("#collinsResult .wt-container ul li"):
            definition = instance.find('.collinsMajorTrans p').eq(0).text().strip()            
            exmaples = []
            for example_doc in instance.items('.examples'):
                ps = example_doc.find('p')
                exmaples.append(f'{ps.eq(0).text().strip()}\t\t{ps.eq(1).text().strip()}')
            
            if len(definition) != 0 and len(exmaples) != 0:
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

def _magic_collins(translation, num_example):
    if num_example <= 0:
        return ''
    output = ''
    for index, collins in enumerate(translation.collins, 1):
        definition = collins.definition
        if index > num_example:
            break 
        examples = '\n\t- '.join(collins.examples)
        output += f'\n----\n{index}. {definition}\n\t- {examples}'
    return output

def _magic(word, translation, num_example):
    definition = '\n> '.join(translation.definition)
    addition = translation.addition
    collins = _magic_collins(translation, num_example)
    output = f'# {word.upper()}\n> {definition}\n\n> {addition}\n\n{collins}'

    console = Console()
    console.print(Markdown(output))

def _play_sound(translation, times):
    pronounces = translation.pronounces
    if not pronounces or len(pronounces) == 0 or times <= 0:
        return
    try:
        sound_url = pronounces[-1].voice_url
        f = _download(sound_url)
        for _ in range(times):
            playsound(f.name)
            sleep(1)
    except:
        pass

def _download(sound):
    try:
        f = NamedTemporaryFile('w+b', prefix='temp_', suffix='.mp3')
        conn = urlopen(sound)
        f.write(conn.read())
        conn.close()
        # have to return reference since tempoorary file will be deleted after finishing method call
        return f
    except:
        raise IOError('Unable to download sound named: ' + sound)  

@click.command()
@click.argument('word')
@click.option('--example', '-e', default=5, type=int, help = "The number of detailed definitions and examples")
@click.option('--pronounce', '-p', default=3, type=int, help = "The times of playing pronounce")
def cli(word, example, pronounce):
    if not word:
        raise ValueError('please enter english word')
    translation = YoudaoTranslator().translate(word)
    _magic(word, translation, example)
    _play_sound(translation, pronounce)

if __name__ == "__main__":
    cli()