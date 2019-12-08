<template>
  <v-dialog v-model="isOpen" persistent max-width="300px">
    <v-card>
      <v-card-title>
        Request Tag
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row align="center" justify="center">
            <v-text-field
              v-model="taggedUsername"
              label="Username"
              outlined
            />
          </v-row>
        </v-container>
        <small>{{ errMsg[1] }}</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="submitTagRequest(photoID, taggedUsername)" color="primary" text>
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
  name: 'TagRequestModal',
  props: {
    isOpen: Boolean,
    photoID: {
      default: null,
      type: Number
    }
  },
  data () {
    return {
      taggedUsername: '',
      errMsg: ''
    }
  },
  methods: {
    submitTagRequest (photoID, tagged) {
      this.$store.dispatch('createTagRequest', { photoID, tagged })
        .then(() => {
          this.taggedUsername = ''
          this.errMsg = ''
          this.toggleModal()
        })
        .catch((e) => { this.errMsg = e })
    },
    toggleModal () {
      this.$emit('toggleModal')
    }
  }
}
</script>
