<template>
  <v-app>
    <v-app-bar
      fixed
      app
    >
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-btn class="toolbar__button">
        Manage Profile
      </v-btn>
      <v-btn @click="togglePhotoModal" class="toolbar__button">
        Upload Photo
      </v-btn>
      <v-btn class="toolbar__button">
        Logout
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      title: 'Finstagram'
    }
  },
  methods: {
    togglePhotoModal () {
      this.$store.commit('TOGGLE_PHOTO_MODAL')
    }
  }
}
</script>

<style lang="scss">
.toolbar__button + .toolbar__button{
  margin-left: 12px;
}
</style>
