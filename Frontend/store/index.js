export const state = () => ({
  user: null
})

export const getters = {
}

export const mutations = {
  SET_USER (state, payload) {
    state.user = payload
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
  async register ({ commit }, { username, password, fname, lname, bio }) {
    try {
      const { data } = await this.$axios.post('register', {
        username,
        password,
        fname,
        lname,
        bio
      })
      console.log(data.response)
      if (data.response) {
        this.$router.push('/')
      }
    } catch (e) {
      throw e.response.data.errMsg
    }
  }
}
