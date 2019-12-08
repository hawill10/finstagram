<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Tag Requests
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider />
    <v-list-item v-for="request in tagRequests" :key="request.index">
      <v-list-item-content>
        <v-list-item-title>
          PhotoID:
          <span @click="navigateTo(request.photoID)" class="tag__link">
            {{ request.photoID }}
          </span>
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
    </v-list-item>
    <v-list-item v-if="tagRequests.length === 0">
      <v-list-item-content>
        <v-list-item-title class="font-weight-bold">
          No Tag Requests
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  computed: {
    tagRequests () {
      return this.$store.getters.getTagRequests
    }
  },
  methods: {
    updateTag (photoID, accept) {
      this.$store.dispatch('updateTagRequest', { accept, photoID })
        .catch(e => console.log(e))
    },
    navigateTo (url) {
      this.$router.push(`feed/${url}`)
    }
  }
}
</script>

<style lang='scss'>
.tag__link {
  text-decoration: underline;
  cursor: pointer;
}
</style>
