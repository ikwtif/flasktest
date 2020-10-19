<template>
  <div class="main-div">
    <b-container class="container-form">
      <b-row class="text-center">
              <b-col class="full-title">Metselwerk volgens NBN EN 1996-3</b-col>
      </b-row>
      <b-form @submit="onSubmit" @change="formChange">
        <b-row align-v="center">
          <input type="hidden" name="sdf" :value="tok">
          <b-col>
            <div class="w-25 p-3">
              <b-button type="submit" variant="primary" class="btn">Submit</b-button>
            </div>
          </b-col>
        </b-row>
        <b-row class="justify-content-center" align-content="center">
          <b-col cols="6">
            <b-col cols="2">
            </b-col>
            <b-col cols="6"></b-col>
            <b-row class="text-center">
              <b-col class="sub-title">Baksteen</b-col>
            </b-row>
            <b-row  align-v="center" v-bind:no-gutters="true">
              <b-col class="text-right">
                <label>{{ metselwerkform.baksteen_type.title }}</label>
              </b-col>
              <b-col cols="1"></b-col>
              <b-col>
                <b-form-select v-model="metselwerkform.baksteen_type.default"
                               :options="metselwerkform.baksteen_type.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row  align-v="center" v-bind:no-gutters="true">
              <b-col class="text-right">
                <label>{{ metselwerkform.baksteen_formaat.title }}</label>
              </b-col>
              <b-col cols="1"></b-col>
              <b-col>
                <b-form-select v-model="metselwerkform.baksteen_formaat.default"
                               :options="metselwerkform.baksteen_formaat.choices"
                               class="mb-3"
                               @change="onChange(metselwerkform.baksteen_formaat.default)">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col cols="4"></b-col>
              <b-col>
                <b-row>lengte [mm]</b-row>
                <b-row>{{ splitedStr[0] }}</b-row>
              </b-col>
              <b-col>
                <b-row>breedte [mm]</b-row>
                <b-row>{{ splitedStr[1] }}</b-row>
              </b-col>
              <b-col>
                <b-row>hoogte [mm]</b-row>
                <b-row>{{ splitedStr[2] }}</b-row>
              </b-col>
              <b-col cols="2"></b-col>
            </b-row>
            <b-row  align-v="center" v-bind:no-gutters="true">
              <b-col class="text-right">
                <label>{{ metselwerkform.baksteen_groep.title }}</label>
              </b-col>
              <b-col cols="1"></b-col>
              <b-col cols="4">
                <b-form-select v-model="metselwerkform.baksteen_groep.default"
                               :options="metselwerkform.baksteen_groep.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col  class="text-center">
                <label>{{ metselwerkform.baksteen_druksterkte.title }}
                </label>
              </b-col>
              <b-col cols="1"></b-col>
              <b-col>
                <input id="baksteen_druksterkte"
                       type="number"
                       step="1"
                       v-model="metselwerkform.baksteen_druksterkte.default">
              </b-col>
            </b-row>
            <b-row class="text-center">
                <b-col class="sub-title">Mortel</b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label class="sub-tit">{{ metselwerkform.mortel_type.title }}</label>
              </b-col>
              <b-col>
                <b-form-select v-model="metselwerkform.mortel_type.default"
                               :options="metselwerkform.mortel_type.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.mortel_druksterkte.title }}</label>
              </b-col>
              <b-col>
                <b-form-select v-model="metselwerkform.mortel_druksterkte.default"
                               :options="metselwerkform.mortel_druksterkte.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.controle_uitvoering.title }}</label>
              </b-col>
              <b-col>
                <b-form-select v-model="metselwerkform.controle_uitvoering.default"
                               :options="metselwerkform.controle_uitvoering.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.controle_materialen.title }}</label>
              </b-col>
              <b-col>
                <b-form-select v-model="metselwerkform.controle_materialen.default"
                               :options="metselwerkform.controle_materialen.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
          </b-col>
          <b-col cols="6">
            <b-row>&nbsp;</b-row>
                        <b-row>&nbsp;</b-row>
            <b-row align-v="center" class="text-center">
              <b-col  class="sub-title">Wand</b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.wand_hoogte.title }}</label>
              </b-col>
              <b-col>
                <input id="wand_hoogte"
                       type="number"
                       step="0.1"
                       v-model="metselwerkform.wand_hoogte.default">
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.wand_hoogte.title }}</label>
              </b-col>
              <b-col class="text-center">
                <label>{{ metselwerkform.wand_hoogte.title }}</label>
              </b-col>
            </b-row>
            <b-row class="text-center" align-v="center">
              <b-col class="sub-title">Randvoorwaarden</b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.randvoorwaarde_randen.title }}</label>
              </b-col>
              <b-col class="text-center">
                <b-form-select v-model="metselwerkform.randvoorwaarde_randen.default"
                               :options="metselwerkform.randvoorwaarde_randen.choices"
                               class="mb-3">
                </b-form-select>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
              </b-col>
              <b-col class="text-left">
                <b-form-checkbox
                  id="randvoorwaarde_dak"
                  v-model="metselwerkform.randvoorwaarde_dak.default"
                  name="randvoorwaarde_dak">
                  {{ metselwerkform.randvoorwaarde_dak.title }}
                </b-form-checkbox>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
              </b-col>
              <b-col class="text-left">
                <b-form-checkbox
                  id="randvoorwaarde_inklemming"
                  v-model="metselwerkform.randvoorwaarde_inklemming.default"
                  name="randvoorwaarde_inklemming">
                  {{ metselwerkform.randvoorwaarde_inklemming.title }}
                </b-form-checkbox>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-left">
              </b-col>
              <b-col class="text-left">
                <b-form-checkbox
                  id="randvoorwaarde_steun"
                  v-model="metselwerkform.randvoorwaarde_steun.default"
                  name="randvoorwaarde_steun">
                  {{ metselwerkform.randvoorwaarde_steun.title }}
                </b-form-checkbox>
              </b-col>
            </b-row>
            <b-row><b-col>
            <div v-show="metselwerkform.randvoorwaarde_steun.default == false">
            <b-row align-v="center">
              <b-col class="text-center">
                <label>{{ metselwerkform.randvoorwaarde_overspanning.title }}</label>
              </b-col>
              <b-col class="text-center">
                <input id="randvoorwaarde_overspanning"
                     type="number"
                     step="0.01"
                     v-model="metselwerkform.randvoorwaarde_overspanning.default">
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-center">
              </b-col>
              <b-col class="text-left">
                <b-form-checkbox
                  id="randvoorwaarde_hyperstatisch"
                  v-model="metselwerkform.randvoorwaarde_hyperstatisch.default"
                  name="randvoorwaarde_hyperstatisch">
                  {{ metselwerkform.randvoorwaarde_hyperstatisch.title }}
                </b-form-checkbox>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col class="text-centre">
              </b-col>
              <b-col class="text-left">
                <b-form-checkbox
                  id="randvoorwaarde_dragend"
                  v-model="metselwerkform.randvoorwaarde_dragend.default"
                  name="randvoorwaarde_dragend">
                  {{ metselwerkform.randvoorwaarde_dragend.title }}
                </b-form-checkbox>
              </b-col>
            </b-row>
          </div>
          </b-col></b-row>
          </b-col>
        </b-row>
      </b-form>
      <b-row><b-col>
      <div v-show="sendCheck == true">
        <b-row>
          <b-col cols="4">Genormaliseerde druksterkte block fb</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['masonry']['output']['fb [N/mm/mm]'] }}</b-col>
          <b-col cols="1">N/mm²</b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Karakteristieke druksterkte metselwerk fk</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['masonry']['output']['fk [N/mm/mm]'] }}</b-col>
          <b-col cols="1">N/mm²</b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Veiligheid Ym</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['masonry']['output']['veiligheidsfactor'] }}</b-col>
          <b-col cols="1"></b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Rekenwaarde druksterkte metselwerk fd</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['masonry']['output']['fd [N/mm/mm]'] }}</b-col>
          <b-col cols="1">N/mm²</b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Effectieve dikte wand tef</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['masonry']['stone']['width [mm]'] }}</b-col>
          <b-col cols="1">mm</b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Effectieve hoogte wand hef</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['wall']['output']['effectieve hoogte [mm]'] }}</b-col>
          <b-col cols="1">mm</b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Effectieve overspanning vloer lf,ef</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['wall']['output']['effectieve overspanning [mm]'] }}</b-col>
          <b-col cols="1">mm</b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Reductiefactor Os</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['wall']['output']['reductiefactor'] }}</b-col>
          <b-col cols="1"></b-col>
        </b-row>
        <b-row>
          <b-col cols="4">Weerstand Nrd UGT</b-col>
          <b-col cols="1"></b-col>
          <b-col cols="1">{{ result['wall']['output']['effectieve hoogte [mm]'] }}</b-col>
          <b-col cols="1">kN/m</b-col>
        </b-row>
        <b-row>&nbsp;</b-row>
      </div>
      </b-col></b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Metselwerk',
  data() {
    return {
      sendCheck: '',
      result: { wall: { output: '' }, masonry: { mortar: '', output: '', stone: '' } },
      splitedStr: ['290', '140', '190'],
      styleResult: {
        fontSize: '10px',
        color: '#687F7F',
        padding: '0px',
      },
      tok: '',
      metselwerkform: {
        baksteen_formaat: {},
        baksteen_groep: {},
        baksteen_type: {},
        baksteen_druksterkte: {},
        mortel_type: {},
        mortel_druksterkte: {},
        controle_uitvoering: {},
        controle_materialen: {},
        ontwerpbelasting: {},
        wand_hoogte: {},
        wand_lengte: {},
        randvoorwaarde_randen: {},
        randvoorwaarde_dak: {},
        randvoorwaarde_inklemming: {},
        randvoorwaarde_steun: {},
        randvoorwaarde_overspanning: {},
        randvoorwaarde_hyperstatisch: {},
        randvoorwaarde_dragend: {},
      },
    };
  },
  methods: {
    formChange() {
      console.log('onchange form');
      this.sendCheck = false;
      this.result = { wall: { output: '' }, masonry: { mortar: '', output: '', stone: '' } };
      console.log(this.sendCheck);
    },
    getToken() {
      const path = '/csrf-cookie';
      axios.get(path, { withCredentials: true })
        .then((response) => {
          console.log('response token');
          console.log(response.data);
          this.tok = response.data.csrf_token;
          axios.defaults.headers.common['X-CSRFToken'] = response.data.csrfToken;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getCalc() {
      const path = '/berekening/metselwerk';
      axios.get(path, {
        headers: {
          Cookie: 'token=' + this.tok,
        },
        withCredentials: true,
      })
        .then((res) => {
          console.log(res);
          this.result = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    getResult(payload) {
      const path = '/berekening/metselwerk';
      console.log(payload);
      axios.post(path, payload, {
        headers: {
          // eslint-disable-next-line
          Cookie: 'token=' + this.tok,
        },
        withCredentials: true,
      })
        .then((res) => {
          console.log(res);
          this.result = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        baksteen_formaat: this.metselwerkform.baksteen_formaat.default,
        baksteen_groep: this.metselwerkform.baksteen_groep.default,
        baksteen_type: this.metselwerkform.baksteen_type.default,
        baksteen_druksterkte: this.metselwerkform.baksteen_druksterkte.default,
        mortel_type: this.metselwerkform.mortel_type.default,
        mortel_druksterkte: this.metselwerkform.mortel_druksterkte.default,
        controle_uitvoering: this.metselwerkform.controle_uitvoering.default,
        controle_materialen: this.metselwerkform.controle_materialen.default,
        ontwerpbelasting: this.metselwerkform.ontwerpbelasting.default,
        wand_hoogte: this.metselwerkform.wand_hoogte.default,
        wand_lengte: this.metselwerkform.wand_lengte.default,
        randvoorwaarde_randen: this.metselwerkform.randvoorwaarde_randen.default,
        randvoorwaarde_dak: this.metselwerkform.randvoorwaarde_dak.default,
        randvoorwaarde_inklemming: this.metselwerkform.randvoorwaarde_inklemming.default,
        randvoorwaarde_steun: this.metselwerkform.randvoorwaarde_steun.default,
        randvoorwaarde_overspanning: this.metselwerkform.randvoorwaarde_overspanning.default,
        randvoorwaarde_hyperstatisch: this.metselwerkform.randvoorwaarde_hyperstatisch.default,
        randvoorwaarde_dragend: this.metselwerkform.randvoorwaarde_dragend.default,
        csrf_token: this.tok,
      };
      console.log(payload);
      this.sendCheck = true;
      this.getResult(payload);
    },
    getmetselwerk() {
      const path = '/metselwerk';
      axios.get(path)
        .then((res) => {
          this.metselwerkform = res.data;
          console.log('get metselwerk');
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onChange(event) {
      console.log(event);
      this.splitedStr = event.split('x');
    },
  },
  created() {
    this.getmetselwerk();
    this.getToken();
  },
};
</script>

<style scoped>
.full-title {
  font-size: 20px;
  font-weight: bold;
}
.sub-title {
  font-size: 15px;
  font-weight: bold;
}
.container-form {
  font-size: 11px;
  color: #687F7F;
}
.mb-3 {
  font-size: 11px;
}
input {
  width: calc(100%);
  border: 0;
  padding: 1px;
  font-size: 1em;
  background-color: #323333;
  color: #687F7F;
}
select {
  width: calc(100%);
  border: 1;
  padding: 1px;
  font-size: 1em;
  background-color: #323333;
  color: #687F7F;
}
button {
  width: calc(100%);
  border: 1;
  padding: 1px;
  font-size: 1em;
  background-color: #323333;
  color: #687F7F;
}
</style>
