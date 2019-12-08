<template>
  <v-layout column>
    <h1 class="profile">My Profile</h1>
    <v-row>
      <v-col>
        <FollowerRequestList />
      </v-col>
      <v-col>
        <TagRequestList />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h1>Hello!</h1>
      </v-col>
    </v-row>
  </v-layout>
</template>

<script>
import FollowerRequestList from '@/components/FollowerRequestList'
import TagRequestList from '@/components/TagRequestList'

export default {
  name: 'Profile',
  components: {
    FollowerRequestList,
    TagRequestList
  },
  async fetch ({ store }) {
    await store.dispatch('getFollowRequests')
    await store.dispatch('getTagRequests')
  },
  middleware ({ store, redirect }) {
    // If the user is not authenticated
    if (!store.state.username && !store.state.token) {
      redirect('/')
    }
  }
}
</script>

<style lang="scss">
.profile {
  margin-bottom: 16px;
}
.request__button + .request__button {
  margin: 0 6px;
}
</style>
