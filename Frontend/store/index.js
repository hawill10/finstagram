export const state = () => ({
  user: null,
  errMsg: null
})

export const getters = {
}

export const mutations = {
  SET_USER (state, payload) {
    state.user = payload
  },
  SET_ERROR (state, payload) {
    state.error = payload
  }
}

export const actions = {
  async login ({ commit }, { username, password }) {
    try {
      const { data } = await this.$axios.post('login', {
        username,
        password
      })
      commit('SET_USER', {
        ...data
      })
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async signup ({ commit }, { username, password, fname, lname, bio }) {
    try {
      const { data } = await this.$axios.post('register', {
        username,
        password,
        fname,
        lname,
        bio
      })
      if (data.status) {
        this.$router.push('/')
      }
    } catch (e) {
      console.log('VUEX ERROR')
      console.log(e)
    }
  }
}
