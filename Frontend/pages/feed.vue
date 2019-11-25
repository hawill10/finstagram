<template>
  <v-layout justify-center>
    <v-flex>
      Hello
    </v-flex>
    <image-upload-modal-vue />
  </v-layout>
</template>

<script>
import imageUploadModalVue from '../components/imageUploadModal.vue'
export default {
  name: 'Feed',
  data () {
    return {}
  },
  components: {
    imageUploadModalVue
  },
  async fetch ({ store }) {
    await store.dispatch('getFeeds')
  },
  middleware ({ store, redirect }) {
    // If the user is not authenticated
    if (!store.state.username && !store.state.token) {
      redirect('/')
    }
  },
  computed: {
    feeds () {
      return this.$store.getters.getFeeds()
    }
  }
}
</script>
