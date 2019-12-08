<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Follow Requests
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider />
    <v-list-item v-for="request in followRequests" :key="request.index">
      <v-list-item-content>
        <v-list-item-title>
          {{ request.username_follower }}
        </v-list-item-title>
      </v-list-item-content>
      <v-row
        align="center"
        justify="end"
      >
        <v-btn
          @click="updateFollow(request.username_follower, true)"
          class="primary request__button"
          small
          depressed
        >
          ACCEPT
        </v-btn>
        <v-btn
          @click="updateFollow(request.username_follower, false)"
          class="error request__button"
          small
          depressed
        >
          DECLINE
        </v-btn>
      </v-row>
    </v-list-item>
    <v-list-item v-if="followRequests.length === 0">
      <v-list-item-content>
        <v-list-item-title class="font-weight-bold">
          No Follow Requests
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  data () {
    return {

    }
  },
  computed: {
    followRequests () {
      return this.$store.getters.getFollowRequests
    }
  },
  methods: {
    updateFollow (follower, accept) {
      this.$store.dispatch('updateFollowRequest', { accept, follower })
        .catch(e => console.log(e))
    }
  }
}
</script>
