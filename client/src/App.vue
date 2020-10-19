<template>
  <b-container id="app">
    <b-row>
      <b-col>
        <navbar/>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <router-view/>
      </b-col>
    </b-row>
      <SideNavbar/>
  </b-container>
</template>
<script>
import Navbar from '@/components/Navbar.vue';
import SideNavbar from '@/components/SideNavbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    SideNavbar,
  },
};
</script>
