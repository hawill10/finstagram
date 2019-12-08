<template>
  <v-app-bar
    fixed
    app
    flat
    class="toolbar"
  >
    <v-toolbar-title @click="navigateTo('/feed')" v-text="title" depressed class="toolbar__title" />
    <v-spacer />
    <small class="toolbar__username">{{ this.$store.state.username }}</small>
    <v-btn @click="navigateTo('/profile')" depressed class="toolbar__button">
      My Profile
    </v-btn>
    <v-btn @click="togglePhotoModal" depressed class="toolbar__button">
      Upload Photo
    </v-btn>
    <v-btn @click="logout" depressed class="toolbar__button">
      Logout
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'ToolBar',
  data () {
    return {
      title: 'Finstagram'
    }
  },
  methods: {
    togglePhotoModal () {
      this.$store.commit('TOGGLE_PHOTO_MODAL')
    },
    logout () {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/'))
    },
    navigateTo (url) {
      this.$router.push(url)
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
  cursor: pointer
}
.toolbar__username {
  margin-right: 12px;
}
</style>
