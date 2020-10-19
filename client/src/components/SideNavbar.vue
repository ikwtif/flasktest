<template>
  <div>
    <b-sidebar id="sidebar-1" title="Sidebar" width='200px' shadow slide>
      <template v-slot:default="{ hide }">
      <div class="p-3">
        <nav class="mb-3">
            <b-nav vertical>
              <b-nav-item active>Active</b-nav-item>
              <b-nav-item href="/berekeningen/metselwerk">Metselwerk</b-nav-item>

            </b-nav>
          </nav>
          <b-button variant="primary" block @click="hide">Close Sidebar</b-button>
      </div>
      </template>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  name: 'SideNavbar',
};
</script>
