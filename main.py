from pyramid.config import Configurator
from pyramid.view import view_config
import string
from faker import Faker
from jinja2 import contextfilter
import os

fake = Faker()


@contextfilter
def randString(context, dummy):
    return ''.join([fake.random.choice(string.ascii_letters + string.digits) for n in range(16)])

@view_config(route_name='index', renderer='layout.jinja2')
def index(request):
    return {'title': 'Index'}

@view_config(route_name='lipsum', renderer='lipsum.jinja2')
def lipsum(request):
    return {'paragraphs': fake.paragraphs(nb=fake.random.randint(5,10))}

@view_config(route_name='table', renderer='table.jinja2')
def random_table(request):
    faker_state = fake.random.getstate()
    seed = request.matchdict['seed']
    fake.random.seed(seed)
    number_of_columns = fake.random.randint(5,10)
    columns = fake.words(nb=number_of_columns)
    rows = []
    for i in range(0, fake.random.randint(30,50)):
        rows.append([fake.random.randint(0,1000) for i in range(0, number_of_columns)])
    fake.random.setstate(faker_state)
    return {'columns': columns,
            'rows': rows}

config = Configurator(settings={'debugtoolbar.hosts': '0.0.0.0/0'})
config.add_route('index', '/')
config.add_route('lipsum', '/lipsum')
config.add_route('table', '/table/{seed}')
config.include('pyramid_jinja2')
thisDirectory = os.path.dirname(os.path.realpath(__file__))
config.add_jinja2_search_path(thisDirectory)
config.include('pyramid_debugtoolbar')
config.commit()
jinja2_env = config.get_jinja2_environment()
jinja2_env.filters['rand_string'] = randString
jinja2_env.autoescape = False
config.scan()

app = config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 6543, app)
    server.serve_forever()
