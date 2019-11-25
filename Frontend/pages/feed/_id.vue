<template>
  <v-layout column>
    <v-row>
      <v-col md="6">
        <v-card class="feedDetails__card">
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
                  First Name, Last Name
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
    selectedPhotoId () {
      return this.$route.params.id
    }
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
