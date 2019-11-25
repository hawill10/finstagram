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
              <v-list-item-title class="headline">
                {{ `${feed.photoPoster} - ${feed.firstName}, ${feed.lastName}` }}
              </v-list-item-title>
              <v-list-item-subtitle>
                Photo ID: {{ feed.photoID }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-card-text>
            <p>{{ feed.caption }}</p>
            <small>{{ feed.timestamp }}</small>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col md="6">
        <v-card class="feedDetails__card">
          <v-card-actions class="feedDetails__button__container">
            <v-btn color="primary" class="feedDetails__button">Like and Rate</v-btn>
            <v-btn color="secondary" class="feedDetails__button">Request Tag</v-btn>
          </v-card-actions>

          <v-list subheader>
            <v-subheader>Tags</v-subheader>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  First Name, Last Name (Username)
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-list subheader>
            <v-subheader>Likes and Rating</v-subheader>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  Username
                </v-list-item-title>
              </v-list-item-content>

              <v-list-item-icon>
                <v-rating
                  v-model="rating"
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
  </v-layout>
</template>

<script>
export default {
  name: 'FeedDetail',
  data () {
    return {
      rating: 4
    }
  },
  computed: {
    feed () {
      return this.$store.getters.getFeed
    }
  },
  async fetch ({ store, app }) {
    await store.dispatch('getFeed', app.context.route.params.id)
  }
  // async asyncData ({ params, $axios }) {
  //   const { data } = await $axios.get(`https://my-api/posts/${params.id}`)
  //   return { title: data.title }
  // }
}
</script>

<style lang="scss">
.feedDetails {
  &__card {
    min-height: 100%;
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
