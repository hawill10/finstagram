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
        <FriendGroupsList />
      </v-col>
    </v-row>
  </v-layout>
</template>

<script>
import FollowerRequestList from '@/components/FollowerRequestList'
import TagRequestList from '@/components/TagRequestList'
import FriendGroupsList from '@/components/FriendGroupsList'

export default {
  name: 'Profile',
  components: {
    FollowerRequestList,
    TagRequestList,
    FriendGroupsList
  },
  async fetch ({ store }) {
    await store.dispatch('getFollowRequests')
    await store.dispatch('getTagRequests')
    await store.dispatch('getFriendGroups')
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
