<template>
  <v-dialog v-model="isOpen" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Sign Up Finstagram</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="username"
                label="Username*"
                outlined
                required
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="fname"
                label="First Name*"
                outlined
                required
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="lname"
                label="Last Name*"
                outlined
                required
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="password"
                label="Password*"
                outlined
                type="password"
                required
              />
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="bio"
                label="Bio"
                outlined
                no-resize
                counter="1000"
              />
            </v-col>
          </v-row>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="submitForm" color="blue darken-1" text>
          Submit
        </v-btn>
        <v-btn @click="closeModal" color="blue darken-1" text>
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    isOpen: Boolean
  },
  data () {
    return {
      errMsg: '',
      username: '',
      password: '',
      fname: '',
      lname: '',
      bio: ''
    }
  },
  methods: {
    submitForm () {
      const { username, password, fname, lname, bio } = this
      console.log(username, password, fname, lname, bio)

      this.$store.dispatch('register', {
        username,
        password,
        fname,
        lname,
        bio
      })
        .catch((e) => {
          this.errMsg = e
        })
    },
    closeModal () {
      this.$emit('toggleModal')
    }
  }
}
</script>

<style>
</style>
