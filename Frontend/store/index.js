export const state = () => ({
  username: null,
  token: null,
  feeds: [],
  feed: {},
  isPhotoModalOpen: false
})

export const getters = {
  getFeeds (state) {
    return state.feeds
  },
  getFeed (state) {
    return state.feed
  }
}

export const mutations = {
  SET_USER (state, payload) {
    state.username = payload
  },
  SET_TOKEN (state, payload) {
    state.token = payload
    this.$axios.setToken(payload, 'Bearer')
  },
  TOGGLE_PHOTO_MODAL (state) {
    state.isPhotoModalOpen = !state.isPhotoModalOpen
  },
  SET_FEEDS (state, payload) {
    state.feeds = payload
  },
  SET_FEED (state, payload) {
    state.feed = payload
  }
}

export const actions = {
  async login ({ commit }, { username, password }) {
    try {
      const { data } = await this.$axios.post('login', {
        username,
        password
      })
      commit('SET_USER', data.username)
      commit('SET_TOKEN', data.token)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async logout ({ commit }) {
    await this.$axios.post('logout')
    commit('SET_USER', null)
    commit('SET_TOKEN', null)
    this.$axios.setToken('', 'Bearer')
  },
  async register ({ commit }, { username, password, fname, lname, bio }) {
    try {
      await this.$axios.post('register', {
        username,
        password,
        fname,
        lname,
        bio
      })
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async getFeeds ({ commit }) {
    try {
      const { data } = await this.$axios.get('feed')
      commit('SET_FEEDS', data.data)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async getFeed ({ commit, state }, id) {
    try {
      const { data } = await this.$axios.get(`feed/${id}`)
      commit('SET_FEED', data.data)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async uploadPhoto ({ commit }, payload) {
    try {
      await this.$axios.post('post', payload)
    } catch (e) {
      throw e.response.data.errMsg
    }
  }
}
