<template>
  <v-layout justify-center>
    <v-row>
      <v-col md="6" offset-md="3">
        <v-card>
          <v-img
            src="https://cdn.vuetifyjs.com/images/cards/mountain.jpg"
            min-height="450px"
          />

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline">
                Photo Poster
              </v-list-item-title>
              <v-list-item-subtitle>
                Photo ID: 1
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-card-text>
            <p>This is caption</p>
            <small>TIMESTAMP</small>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <image-upload-modal-vue />
  </v-layout>
</template>

<script>
import imageUploadModalVue from '@/components/imageUploadModal.vue'
export default {
  name: 'Feed',
  components: {
    imageUploadModalVue
  },
  data () {
    return {}
  },
  // async fetch ({ store }) {
  //   await store.dispatch('getFeeds')
  // },
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
