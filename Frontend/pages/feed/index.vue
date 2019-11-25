<template>
  <v-layout justify-center>
    <v-row>
      <v-col md="6" offset-md="3">
        <v-card v-for="feed in feeds" @click="navigateTo(feed.photoID)" :key="feed.index" class="feed__card">
          <v-img
            :src="`http://localhost:5000${feed.filepath}`"
            max-height="450px"
          />

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline">
                {{ feed.photoPoster }}
              </v-list-item-title>
              <v-list-item-subtitle>
                Photo ID: {{ feed.photoID }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-card-text>
            <p>{{ feed.caption }}</p>
            <small>{{ feed.postingdate }}</small>
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
  computed: {
    feeds () {
      return this.$store.getters.getFeeds
    }
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
  methods: {
    navigateTo (id) {
      this.$router.push(`/feed/${id}`)
    }
  }
}
</script>

<style lang="scss">
.feed__card + .feed__card {
  margin-top: 20px;
}
</style>
