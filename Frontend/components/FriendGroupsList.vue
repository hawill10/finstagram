<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Friend Groups
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider />
    <!-- <v-list-item v-for="request in tagRequests" :key="request.index">
      <v-list-item-content>
        <v-list-item-title>
          PhotoID: {{ request.photoID }}
        </v-list-item-title>
      </v-list-item-content>
      <v-row
        align="center"
        justify="end"
      >
        <v-btn
          @click="updateTag(request.photoID, true)"
          class="primary request__button"
          small
          depressed
        >
          ACCEPT
        </v-btn>
        <v-btn
          @click="updateTag(request.photoID, false)"
          class="error request__button"
          small
          depressed
        >
          DECLINE
        </v-btn>
      </v-row>
    </v-list-item> -->
    <v-list-item v-if="friendGroups.length === 0">
      <v-list-item-content>
        <v-list-item-title class="font-weight-bold">
          No Friend Groups
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  computed: {
    friendGroups () {
      return this.$store.getters.getFriendGroups
    }
  }
  // methods: {
  //   updateTag (photoID, accept) {
  //     this.$store.dispatch('updateTagRequest', { accept, photoID })
  //       .catch(e => console.log(e))
  //   }
  // }
}
</script>