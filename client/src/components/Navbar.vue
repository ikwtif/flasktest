<template>
  <b-navbar
    toggleable="md"
    type="dark"
    variant="info"
    fixed="top">
    <b-navbar-brand href="#">Account-Owner Home</b-navbar-brand>
    <b-navbar-nav>
      <b-nav-item href="#">Dossiers</b-nav-item>
      <b-nav-item v-b-toggle.sidebar-1>Berekeningen</b-nav-item>

    </b-navbar-nav>
  </b-navbar>

</template>
<script>
export default {
  name: 'Navbar',
};
</script>

<style>
.main-div {
  margin-top: 100px
  }
</style>
