<template>
  <v-dialog v-model="isOpen" persistent max-width="300px">
    <v-card>
      <v-card-title>
        Like & Rating
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row align="center" justify="center">
            <v-rating
              v-model="rating"
              length="5"
              full-icon="mdi-heart"
              empty-icon="mdi-heart-outline"
            />
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="submitRating(photoID, rating)" color="primary" text>
          Submit
        </v-btn>
        <v-btn @click="toggleModal" color="error" text>
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'LikeModal',
  props: {
    isOpen: Boolean,
    photoID: {
      default: null,
      type: Number
    }
  },
  data () {
    return {
      rating: 0
    }
  },
  methods: {
    submitRating (photoID, rating) {
      this.$store.dispatch('createLike', { photoID, rating })
        .then(() => {
          this.rating = 0
          this.toggleModal()
        })
        .catch(e => console.log(e))
    },
    toggleModal () {
      this.$emit('toggleModal')
    }
  }
}
</script>
