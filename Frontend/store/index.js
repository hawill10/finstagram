export const state = () => ({
  username: null,
  token: null
})

export const getters = {
}

export const mutations = {
  SET_USER (state, payload) {
    state.username = payload
  },
  SET_TOKEN (state, payload) {
    state.token = payload
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
      this.$axios.setToken(data.token, 'Bearer')
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
      const response = await this.$axios.get('feed')
      console.log(response)
    } catch (e) {
      throw e.response.data.errMsg
    }
  }
}
