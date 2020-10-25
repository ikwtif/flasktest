<template>
  <div class="main-div">
    <b-container class="container-form">
      <b-row>
      <b-col cols="3">
        <b-form @submit="onSubmit">
           <input type="hidden" name="sdf" :value=tok>
          <b-row>
            <b-button type="submit" variant="primary" class="btn">Submit</b-button>
            <b-button type="reset" variant="danger" class="btn">Reset</b-button>
          </b-row>
          <b-row class="text-center">
            <b-col>KOLOM</b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.type.title }}
              </label>
            </b-col>
            <b-col>
              <b-form-select v-model="kolomform.type.default"
                             :options="kolomform.type.choices"
                             class="mb-3">
              </b-form-select>
            </b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.nodeboven.title }}
              </label>
            </b-col>
            <b-col>
              <b-form-select v-model="kolomform.nodeboven.default"
                             :options="kolomform.nodeboven.choices"
                             class="mb-3">
              </b-form-select>
            </b-col>
          </b-row>
          <div v-if="kolomform.nodeboven.default == 'veer'">
          <b-row>
            <b-col  class="text-center">
              <label for="veerconstantek1">{{ kolomform.veerconstantek1.title }}
              </label>
            </b-col>
            <b-col>
              <input id="veerconstantek1"
                     type="number"
                     step=".01"
                     v-model="kolomform.veerconstantek1.default">
            </b-col>
          </b-row>
          </div>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.nodeonder.title }}
              </label>
            </b-col>
            <b-col>
              <b-form-select v-model="kolomform.nodeonder.default"
                             :options="kolomform.nodeonder.choices"
                             class="mb-3">
              </b-form-select>
            </b-col>
          </b-row>
          <div v-if="kolomform.nodeonder.default == 'veer'">
          <b-row>
            <b-col  class="text-center">
              <label for="veerconstantek2">{{ kolomform.veerconstantek2.title }}
              </label>
            </b-col>
            <b-col>
              <input id="veerconstantek2"
                     type="number"
                     step=".01"
                     v-model="kolomform.veerconstantek2.default">
            </b-col>
          </b-row>
          </div>
          <b-row class="text-center">
            <b-col>MATERIALEN</b-col>
          </b-row>
          <b-row>
            <b-col><p>&nbsp;</p></b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.type.title }}
              </label>
            </b-col>
            <b-col>
              <b-form-select v-model="kolomform.type.default"
                             :options="kolomform.type.choices"
                             class="mb-3">
              </b-form-select>
            </b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.staalkwaliteit.title }}
              </label>
            </b-col>
            <b-col>
              <input id="staalkwaliteit"
                     v-model="kolomform.staalkwaliteit.default"
                     type="number">
            </b-col>
          </b-row>
          <b-row class="text-center">
            <b-col>COEFFICIENTEN</b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.materiaalcoeff.title }}
              </label>
            </b-col>
            <b-col>
              <input id="materiaalcoeff"
                     v-model="kolomform.materiaalcoeff.default"
                     type="number"
                     step="0.1">
            </b-col>
          </b-row>
          <b-row class="text-center">
            <b-col class="subtitle">DIMENSIES</b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.lengte.title }}
              </label>
            </b-col>
            <b-col>
              <input id="lengte"
                     v-model="kolomform.lengte.default"
                     type="number">
            </b-col>
          </b-row>
          <div v-show="kolomform.type.default == 'rechthoek' ||
          kolomform.type.default == 'L-kolom'">
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.hoogte.title }}
              </label>
            </b-col>
            <b-col>
              <input id="hoogte"
                     v-model="kolomform.hoogte.default"
                     type="number">
            </b-col>
          </b-row>
          <div v-show="kolomform.type.default == 'L-kolom'">
            <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.hoogte_2.title }}
              </label>
            </b-col>
            <b-col>
              <input id="hoogte_2"
                     v-model="kolomform.hoogte_2.default"
                     type="number">
            </b-col>
          </b-row>
          </div>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.breedte.title }}
              </label>
            </b-col>
            <b-col>
              <input id="breedte"
                     v-model="kolomform.breedte.default"
                     type="number">
            </b-col>
          </b-row>
          <div v-show="kolomform.type.default == 'L-kolom'">
            <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.breedte_2.title }}
              </label>
            </b-col>
            <b-col>
              <input id="breedte_2"
                     v-model="kolomform.breedte_2.default"
                     type="number">
            </b-col>
            </b-row>
          </div>
          </div>
          <div v-show="kolomform.type.default == 'cirkel'">
            <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.radius.title }}
              </label>
            </b-col>
            <b-col>
              <input id="radius"
                     v-model="kolomform.radius.default"
                     type="number">
            </b-col>
            </b-row>
          </div>
          <b-row class="text-center">
            <b-col>PARAMETERS</b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.langskracht.title }}
              </label>
            </b-col>
            <b-col>
              <input id="langskracht"
                     v-model="kolomform.langskracht.default"
                     type="number">
            </b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.As.title }}
              </label>
            </b-col>
            <b-col>
              <input id="As"
                     v-model="kolomform.As.default"
                     type="number">
            </b-col>
          </b-row>
          <b-row>
            <b-col class="text-center">
              <label>{{ kolomform.As0.title }}
              </label>
            </b-col>
            <b-col>
              <input id="As0"
                     v-model="kolomform.As0.default"
                     type="number">
            </b-col>
          </b-row>
        </b-form>
      </b-col>
      <b-col>
        <div v-show="kolomform.nodeboven.default == 'scharnier' &&
          kolomform.nodeonder.default == 'scharnier'">
        <b-img src="../../assets/betonkolom/scharnier_scharnier.png"
               fluid alt="Fluid image"></b-img>
        </div>
        <div v-show="kolomform.nodeboven.default == 'inklemming' &&
          kolomform.nodeonder.default == 'inklemming'">
          <b-img src="../../assets/betonkolom/inklemming_inklemming.png"
                 fluid alt="Fluid image"></b-img>
        </div>
        <div v-show="kolomform.nodeboven.default == 'rol' &&
          kolomform.nodeonder.default == 'inklemming'">
          <b-img src="../../assets/betonkolom/inklemming_rol.png"
                 fluid alt="Fluid image"></b-img>
        </div>
        <div v-show="kolomform.nodeboven.default == 'scharnier' &&
          kolomform.nodeonder.default == 'inklemming'">
          <b-img src="../../assets/betonkolom/inklemming_scharnier.png"
                 fluid alt="Fluid image"></b-img>
        </div>
        <div v-show="kolomform.nodeboven.default == 'vrij' &&
          kolomform.nodeonder.default == 'inklemming'">
          <b-img src="../../assets/betonkolom/inklemming_vrij.png"
                 fluid alt="Fluid image"></b-img>
        </div>
        <div v-show="kolomform.nodeboven.default == 'veer' &&
          kolomform.nodeonder.default == 'veer'">
          <b-img src="../../assets/betonkolom/veer_veer.png"
                 fluid alt="Fluid image"></b-img>
        </div>
        <div v-show="kolomform.nodeboven.default == 'vrij' &&
          kolomform.nodeonder.default == 'veer'">
          <b-img src="../../assets/betonkolom/veer_vrij.png"
                 fluid alt="Fluid image"></b-img>
        </div>
      </b-col>
      <b-col col lg="6">
        <b-row class="text-center">
          <p>RESULTATEN</p>
        </b-row>
        <p v-for="(item, key) in result" :key="item.value">
          <b-row v-bind:style="styleResult">
            <b-col col sm="2" class="text-right">
            {{ key }}
            </b-col>
            <b-col col sm="2" class="text-right">
              {{ item.value }}
            </b-col>
            <b-col col sm="2" class="text-left">
              {{ item.units }}
            </b-col>
          </b-row>
        </p>
      </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Betonkolom',
  data() {
    return {
      styleResult: {
        fontSize: '10px',
        color: '#687F7F',
        padding: '0px',
      },
      result: {},
      tok: '',
      kolomform: {
        type: {},
        nodeboven: {},
        nodeonder: {},
        betonkwaliteit: {},
        veerconstantek1: {},
        veerconstantek2: {},
        staalkwaliteit: {},
        materiaalcoeff: {},
        lengte: {},
        hoogte: {},
        hoogte_2: {},
        breedte: {},
        breedte_2: {},
        radius: {},
        As: {},
        As0: {},
        langskracht: {},
      },
    };
  },
  methods: {
    getToken() {
      const path = 'http://localhost:8080/csrf-cookie';
      axios.get(path, { withCredentials: true })
        .then((response) => {
          console.log('response kolom');
          console.log(response.data);
          this.tok = response.data.csrf_token;
          axios.defaults.headers.common['X-CSRFToken'] = response.data.csrfToken;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getResult(payload) {
      const path = 'http://localhost:8080/berekening/betonkolom';
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
        type: this.kolomform.type.default,
        nodeboven: this.kolomform.nodeboven.default,
        nodeonder: this.kolomform.nodeonder.default,
        betonkwaliteit: this.kolomform.betonkwaliteit.default,
        veerconstantek1: this.kolomform.veerconstantek1.default,
        veerconstantek2: this.kolomform.veerconstantek2.default,
        staalkwaliteit: this.kolomform.staalkwaliteit.default,
        materiaalcoeff: this.kolomform.materiaalcoeff.default,
        lengte: this.kolomform.lengte.default,
        hoogte: this.kolomform.hoogte.default,
        hoogte_2: this.kolomform.hoogte_2.default,
        breedte: this.kolomform.breedte.default,
        breedte_2: this.kolomform.breedte_2.default,
        radius: this.kolomform.radius.default,
        As: this.kolomform.As.default,
        As0: this.kolomform.As0.default,
        langskracht: this.kolomform.langskracht.default,
        csrf_token: this.tok,
      };
      console.log(payload);
      this.getResult(payload);
    },
    getkolom() {
      const path = 'http://localhost:8080/betonkolom';
      axios.get(path)
        .then((res) => {
          this.kolomform = res.data;
          console.log('get kolom');
          console.log(res.data);
          console.log(res.data.type.title);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getkolom();
    this.getToken();
  },
};
</script>

<style scoped>
.subtitle {
  font-size: 11px;
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
