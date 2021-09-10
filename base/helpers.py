from inspect import getsourcefile
from os.path import abspath

def LOG(content):
    file = abspath(getsourcefile(lambda:0))
    print(f'{file}: {content}')

def get_validated_data(serializer, request, raise_exception=True):
    '''
    Create serializer instance and valid request.data
    Return (validated_data, serializer_instance)
    '''
    s = serializer(data=request.data)
    s.is_valid(raise_exception=raise_exception)
    return (s.validated_data, s)


def response_message(msg: str):
    return {'detail': msg}

def initialize_dotenv():
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())