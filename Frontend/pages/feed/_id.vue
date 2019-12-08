<template>
  <v-layout column>
    <v-row>
      <v-col md="6">
        <v-card class="feedDetails__card">
          <v-img
            :src="`http://localhost:5000${feed.filepath}`"
            max-height="450px"
          />

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline feedDetails__title">
                {{ feed.photoPoster }}
              </v-list-item-title>
              <v-list-item-subtitle>
                <p>Posted By - {{ `${feed.firstName}, ${feed.lastName}` }}</p>
                <small>Photo ID - {{ feed.photoID }}</small>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-card-text>
            <p>{{ feed.caption }}</p>
            <v-divider />
            <small>{{ feed.postingdate }}</small>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col md="6">
        <v-card class="feedDetails__card">
          <v-card-actions class="feedDetails__button__container">
            <v-btn @click="toggleLikeModal" :disabled="disableLike.length !== 0" color="primary" class="feedDetails__button">
              Like and Rate
            </v-btn>
            <v-btn @click="toggleTagModal" color="secondary" class="feedDetails__button">
              Request Tag
            </v-btn>
          </v-card-actions>

          <v-list subheader>
            <v-subheader>Tags</v-subheader>

            <v-list-item v-for="tag in feed.tagged" :key="tag.index">
              <v-list-item-content>
                <v-list-item-title>
                  {{ `${tag.firstName}, ${tag.lastName} (${tag.username})` }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-list subheader>
            <v-subheader>Likes and Rating</v-subheader>

            <v-list-item v-for="feedRating in feed.rating" :key="rating.index">
              <v-list-item-content>
                <v-list-item-title>
                  {{ feedRating.username }}
                </v-list-item-title>
              </v-list-item-content>

              <v-list-item-icon>
                <v-rating
                  :value="feedRating.rating"
                  length="5"
                  readonly
                  full-icon="mdi-heart"
                  empty-icon="mdi-heart-outline"
                />
              </v-list-item-icon>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    <LikeModal :isOpen="isLikeModalOpen" :photoID="feed.photoID" @toggleModal="toggleLikeModal" />
    <TagRequestModal :isOpen="isTagModalOpen" :photoID="feed.photoID" @toggleModal="toggleTagModal" />
  </v-layout>
</template>

<script>
import LikeModal from '@/components/LikeModal'
import TagRequestModal from '@/components/TagRequestModal'

export default {
  name: 'FeedDetail',
  components: {
    LikeModal,
    TagRequestModal
  },
  data () {
    return {
      rating: 4,
      isLikeModalOpen: false,
      isTagModalOpen: false
    }
  },
  computed: {
    feed () {
      return this.$store.getters.getFeed
    },
    disableLike () {
      const checkRating = this.feed.rating.filter(rating => rating.username === this.$store.state.username)
      return checkRating
    }
  },
  async fetch ({ store, app }) {
    await store.dispatch('getFeed', app.context.route.params.id)
  },
  methods: {
    toggleLikeModal () {
      this.isLikeModalOpen = !this.isLikeModalOpen
    },
    toggleTagModal () {
      this.isTagModalOpen = !this.isTagModalOpen
    }
  },
  middleware ({ store, redirect }) {
    // If the user is not authenticated
    if (!store.state.username && !store.state.token) {
      redirect('/')
    }
  }
}
</script>

<style lang="scss">
.feedDetails {
  &__card {
    min-height: 100%;
  }
  &__title {
    margin-bottom: 12px !important;
  }
  &__button {
    width: 30%;
    &__container {
      padding: 24px 0;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
