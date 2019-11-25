<template>
  <v-layout>
    <v-flex class="text-center">
      <img
        src="/v.png"
        alt="Vuetify.js"
        class="mb-5"
      >
      <blockquote class="blockquote">
        &#8220;First, solve the problem. Then, write the code.&#8221;
        <footer>
          <small>
            <em>&mdash;John Johnson</em>
          </small>
        </footer>
      </blockquote>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'Feed',
  data () {
    return {}
  },
  async fetch ({ store }) {
    await store.dispatch('getFeeds')
  },
  middleware ({ store, redirect }) {
    // If the user is not authenticated
    if (!localStorage.getItem('token')) {
      return redirect('/')
    } else if (!store.state.username && !store.state.token) {
      store.commit('SET_TOKEN', localStorage.getItem('token'))
      store.commit('SET_USER', localStorage.getItem('username'))
    }
  }
}
</script>
