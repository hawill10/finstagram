<template>
  <v-app>
    <v-app-bar
      fixed
      app
      flat
      class="toolbar"
    >
      <v-toolbar-title v-text="title" depressed class="toolbar__title" />
      <v-spacer />
      <small>{{ this.$store.state.username }}</small>
      <v-btn depressed class="toolbar__button">
        Manage Profile
      </v-btn>
      <v-btn @click="togglePhotoModal" depressed class="toolbar__button">
        Upload Photo
      </v-btn>
      <v-btn depressed class="toolbar__button">
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
.toolbar__button {
  background: white !important;
}
.toolbar__title {
  font-weight: bold;
}
</style>
