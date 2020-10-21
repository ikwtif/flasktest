from flask import Flask, jsonify, request, session
from flask_cors import CORS
from wtforms import Form
from wtforms.fields import SelectField, StringField, FloatField, IntegerField, BooleanField
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRFError
from wtforms_json import flatten_json
import wtforms_json
from wtforms_jsonschema.jsonschema import WTFormToJSONSchema
from Eurocode.ec2.materials import CYLINDER_TO_CUBE_STRENGTHS
from Eurocode.ec2.column import ConcreteColumn
from Eurocode.ec6.data import MASONRY_APPLICATION, MASONRY_SUPERVISION, FORMFACTOR, \
    STONE_CONDITIONINGFACTOR, STONE_DIMENSIONS, STONE_GROUPS, STONE_KINDS, \
    MORTAR_GROUPS, MORTAR_KINDS, MORTAR_WEIGHT_DENSITY
from Eurocode.ec6.masonry import Masonry
from Eurocode.ec6.wall import WallSimple
import logging

wtforms_json.init()
# configuration
DEBUG = True

csrf = CSRFProtect()
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
#TODO change secret keys
app.config['SECRET_KEY'] = 'mysecretKey'
app.config['WTF_CSRF_SECRET_KEY'] = 'mysecretKey'
csrf.init_app(app)

#logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

app.logger.debug('starting app')


class MetselwerkForm(Form):
    baksteen_formaat = SelectField(label='formaat', choices=list(zip( STONE_DIMENSIONS, STONE_DIMENSIONS)), default='290x140x190')
    baksteen_groep = SelectField(label='groepsindeling steen', choices=list(zip(STONE_GROUPS, STONE_GROUPS)), default=STONE_GROUPS[0])
    baksteen_type = SelectField(label='type baksteen', choices=list(zip(STONE_KINDS, STONE_KINDS)), default=STONE_KINDS[0])
    baksteen_druksterkte = IntegerField(label='druksterkte', default=10)
    mortel_type = SelectField(label='morteltype', choices=list(zip(MORTAR_KINDS, MORTAR_KINDS)), default=MORTAR_KINDS[0])
    mortel_druksterkte = SelectField(label='druksterkte', choices=list(zip(MORTAR_GROUPS, MORTAR_GROUPS)), default=MORTAR_GROUPS[2])
    controle_uitvoering = SelectField(label='Controle op de uitvoering', choices=list(zip(MASONRY_SUPERVISION, MASONRY_SUPERVISION)), default=MASONRY_SUPERVISION[0])
    controle_materialen = SelectField(label='Controle op de materialen', choices=list(zip(MASONRY_APPLICATION, MASONRY_APPLICATION)), default=MASONRY_APPLICATION[2])
    ontwerpbelasting = IntegerField(label='Ontwerpbelasting', default=0)
    wand_hoogte = IntegerField(label='hoogte', default=3)
    #wand_dikte = IntegerField(label=)
    wand_lengte = IntegerField(label='lengte', default=5)
    randvoorwaarde_randen = SelectField(label='aantal ondersteunde randen', choices=list(zip([0, 1, 2], [0, 1, 2])), default=2)
    randvoorwaarde_dak = BooleanField(label='muur onder dak', default=False)
    randvoorwaarde_inklemming = BooleanField(label='inklemming', default=True)
    randvoorwaarde_steun = BooleanField(label='eindsteun voor de vloer', default=True)
    randvoorwaarde_overspanning = IntegerField(label='overspanning vloer', default=7)
    randvoorwaarde_hyperstatisch = BooleanField(label='hyperstatische vloer', default=False)
    randvoorwaarde_dragend = BooleanField(label='betonvloer 2 richtingen dragend', default=True)

def convert_vue(data):
    converted = dict()
    print(data)
    for part in data['properties'].items():
        converted[part[0]] = dict()
        converted[part[0]]['title'] = part[1]['title']
        if 'default' in part[1]:
            converted[part[0]]['default'] = part[1]['default']
        if 'ux-widget-choices' in part[1]:
            converted[part[0]]['choices'] = []
            for sec in part[1]['ux-widget-choices']:
                converted[part[0]]['choices'].append({'value': sec[0], 'text': sec[1]})
    print(converted)
    return converted

@csrf.error_handler
def csrf_error(reason):
    print(csrf.__dict__)
    print(reason)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/metselwerk')
def metselwerk():
    form = MetselwerkForm()
    data = WTFormToJSONSchema().convert_form(form)
    conv = convert_vue(data)
    print(conv)
    return jsonify(conv)

@app.route('/csrf-cookie', methods=['GET'])
def token():
    return jsonify({'csrfToken': generate_csrf(),
                    'csrf_token': session['csrf_token']
                    })


@app.route('/berekening/<calc_id>', methods=['GET', 'POST'])
def metselwerkr(calc_id):
    app.logger.debug('POST method recieved')
    if request.method == 'POST':
        if calc_id == 'metselwerk':
            form = MetselwerkForm.from_json(request.get_json())
            if form.validate():
                print('validated')
                response_object = {'status': 'success'}
                formaten = form.baksteen_formaat.data.split("x")
                print(formaten)
                brick = Masonry(stone_height=int(formaten[2]),
                                stone_width=int(formaten[1]),
                                stone_length=int(formaten[0]),
                                stone_kind=form.baksteen_type.data,
                                stone_fmean=form.baksteen_druksterkte.data,
                                stone_group=form.baksteen_groep.data,
                                mortar_kind=form.mortel_type.data,
                                mortar_group=form.mortel_druksterkte.data,
                                application=form.controle_materialen.data,
                                supervision=form.controle_uitvoering.data
                                )
                wand = WallSimple(hoogte=form.wand_hoogte.data,
                                  lengte=form.wand_lengte.data,
                                  vaste_zijrand=form.randvoorwaarde_randen.data,
                                  dak=form.randvoorwaarde_dak.data,
                                  inklemming=form.randvoorwaarde_inklemming.data,
                                  eindsteun=form.randvoorwaarde_steun.data,
                                  lengte_overspanning=form.randvoorwaarde_overspanning.data,
                                  hyperstatisch=form.randvoorwaarde_hyperstatisch.data,
                                  dragende_richting=form.randvoorwaarde_dragend.data,
                                  masonry=brick,
                                  last_op_wand=100
                                  )
                results = wand.output()
        else:
            results = {'status': '400'}
        return jsonify(results)
    elif request.method == 'GET':
        response_object = {'status': '400'}
        return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True)