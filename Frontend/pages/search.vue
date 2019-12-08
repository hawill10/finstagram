<template>
  <v-layout column>
    <h1>
      Search By Photo Poster
    </h1>
    <v-row align="center" justify="center" class="search__field">
      <v-col>
        <v-text-field
          v-model="poster"
          @click:append="search(poster)"
          label="Username"
          append-icon="mdi-magnify"
          outlined
        />
      </v-col>
    </v-row>
    <v-row v-if="searchPoster">
      <v-col xs="12" sm="6" offset-sm="3">
        <v-list-item elevation="3">
          <v-list-item-content>
            <v-list-item-title class="font-weight-bold">
              {{ searchPoster.username || '' }}
            </v-list-item-title>
          </v-list-item-content>
          <v-row
            align="center"
            justify="end"
          >
            <v-btn
              @click="requestFollow(searchPoster.username)"
              :disabled="followBtnDisabled"
              :class="followBtnColor"
              class="request__button"
              small
              depressed
            >
              {{ followBtnTitle }}
            </v-btn>
          </v-row>
        </v-list-item>
      </v-col>
    </v-row>
    <v-row v-if="showErrorMsg">
      <v-col xs="12" sm="6" offset-sm="3">
        <p class="text-center font-weight-bold">
          {{ errMsg }}
        </p>
      </v-col>
    </v-row>
    <v-row v-if="searchList.length !== 0" no-gutters>
      <v-col xs="12" sm="6" offset-sm="3">
        <v-card v-for="item in searchList" @click="navigateTo(item.photoID)" :key="item.index" class="search__card">
          <v-img
            :src="`http://localhost:5000${item.filepath}`"
            max-height="450px"
            contain
          />

          <v-divider />

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline">
                {{ item.photoPoster }}
              </v-list-item-title>
              <v-list-item-subtitle>
                Photo ID: {{ item.photoID }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-card-text>
            <p>{{ item.caption }}</p>
            <v-divider />
            <small>{{ item.postingdate }}</small>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-layout>
</template>

<script>
export default {
  name: 'SearchPage',
  data () {
    return {
      poster: '',
      errMsg: '',
      showErrorMsg: false,
      followBtnTitle: '',
      followBtnColor: '',
      followBtnDisabled: false
    }
  },
  computed: {
    searchPoster () {
      return this.$store.getters.getSearchPoster
    },
    searchList () {
      return this.$store.getters.getSearchList
    }
  },
  mounted () {
    this.$store.commit('SET_SEARCH_POSTER', '')
    this.$store.commit('SET_SEARCH_LIST', [])
    this.errMsg = ''
    this.showErrorMsg = false
  },
  methods: {
    search (poster) {
      this.$store.commit('SET_SEARCH_POSTER', '')
      this.$store.commit('SET_SEARCH_LIST', [])
      this.errMsg = ''
      this.showErrorMsg = false
      // Search Username
      this.$store.dispatch('searchByUsername', poster)
        .then(() => {
          if (!this.searchPoster) {
            this.errMsg = `${poster} is not found.`
            this.showErrorMsg = true
          } else if (this.searchPoster.followstatus === 1) {
            // Search By Poster if followed
            this.$store.dispatch('searchByPhotoPoster', poster)
              .then(() => {
                if (this.searchList.length === 0) {
                  this.errMsg = `${poster} has no photos uploaded.`
                  this.showErrorMsg = true
                }
              })
              .catch((e) => {
                this.errMsg = e
                this.showErrorMsg = true
              })
          } else if (this.searchPoster.username !== this.$store.state.username) {
            this.errMsg = `You have to follow ${poster} to see the photos.`
            this.showErrorMsg = true
          }
          this.updateFollowButton()
        })
        .catch((e) => {
          this.errMsg = e
          this.showErrorMsg = true
        })
    },
    navigateTo (id) {
      this.$router.push(`/feed/${id}`)
    },
    requestFollow (username) {
      this.$store.dispatch('createFollowRequest', username)
        .then(() => {
          this.followBtnTitle = 'FOLLOW REQUESTED'
          this.followBtnColor = 'warning'
          this.followBtnDisabled = true
        })
        .catch((e) => {
          this.errMsg = e
          this.showErrorMsg = true
        })
    },
    updateFollowButton () {
      if (this.searchPoster.username === this.$store.state.username) {
        this.followBtnTitle = 'NOT APPLICABLE'
        this.followBtnColor = 'error'
        this.followBtnDisabled = true
      } else if (this.searchPoster.followstatus === null) {
        this.followBtnTitle = 'REQUEST FOLLOW'
        this.followBtnColor = 'primary'
        this.followBtnDisabled = false
      } else if (this.searchPoster.followstatus === false) {
        this.followBtnTitle = 'FOLLOW REQUESTED'
        this.followBtnColor = 'warning'
        this.followBtnDisabled = true
      } else {
        this.followBtnTitle = 'FOLLOWED'
        this.followBtnColor = 'primary'
        this.followBtnDisabled = true
      }
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

<style lang='scss'>
.search__field {
  margin-top: 16px;
}
.search__card + .search__card {
  margin-top: 20px;
}
</style>
