<template>
  <v-dialog v-model="isOpen" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Upload New Image</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-alert
                v-model="alert"
                :close-text="toggleAlert"
                border="left"
                type="error"
                transition="slide-y-transition"
                dismissible
                class="register__alert"
              >
                {{ errMsg }}
              </v-alert>
            </v-col>
            <v-col cols="12">
              <v-file-input
                v-model="file"
                @change="onFileChange"
                label="Image"
                accept="image/*"
                filled
                prepend-icon="mdi-camera"
              />
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="caption"
                label="Caption"
                outlined
                no-resize
                counter="100"
              />
            </v-col>
            <v-col cols="12">
              <v-checkbox
                v-model="isAllFollowers"
                label="All Followers"
              />
            </v-col>
          </v-row>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="submitImage" color="blue darken-1" text>
          Submit
        </v-btn>
        <v-btn @click="toggleModal" color="blue darken-1" text>
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ImageUploadModal',
  data () {
    return {
      alert: false,
      file: null,
      imageUrl: '',
      caption: '',
      errMsg: '',
      isAllFollowers: false
    }
  },
  computed: {
    isOpen () {
      return this.$store.state.isPhotoModalOpen
    }
  },
  methods: {
    toggleAlert () {
      this.alert = !this.alert
    },
    toggleModal () {
      this.$store.commit('TOGGLE_PHOTO_MODAL')
    },
    onFileChange () {
      if (this.file) {
        const reader = new FileReader()
        reader.onload = () => {
          this.imageUrl = reader.result
        }
        reader.readAsDataURL(this.file)
      }
    },
    submitImage () {
      const { imageUrl, caption, file } = this
      const allFollowers = this.isAllFollowers ? 1 : 0

      const imageExtension = `.${imageUrl.split(',')[0].split(':')[1].split(';')[0].split('/')[1]}`
      const baseImageUrl = imageUrl.split(',')[1]

      const formData = new FormData()
      formData.append('imageUrl', baseImageUrl)
      formData.append('imageExtension', imageExtension)
      formData.append('rawFile', file)
      formData.append('caption', caption)
      formData.append('allFollowers', allFollowers)

      this.$store.dispatch('uploadPhoto', formData)
        .then(() => {
          this.file = null
          this.imageUrl = ''
          this.caption = ''
          this.isAllFollowers = false
          this.$store.dispatch('getFeeds')
          this.toggleModal()
        })
        .catch((e) => {
          this.errMsg = e
        })
    }
  }
}
</script>

<style>

</style>
