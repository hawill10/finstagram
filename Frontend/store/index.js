export const state = () => ({
  username: null,
  token: null,
  feeds: [],
  feed: {},
  isPhotoModalOpen: false,
  followRequests: [],
  tagRequests: [],
  searchPoster: '',
  searchList: []
})

export const getters = {
  getFeeds (state) {
    return state.feeds
  },
  getFeed (state) {
    return state.feed
  },
  getFollowRequests (state) {
    return state.followRequests
  },
  getTagRequests (state) {
    return state.tagRequests
  },
  getSearchList (state) {
    return state.searchList
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
  },
  SET_FOLLOW_REQUESTS (state, payload) {
    state.followRequests = payload
  },
  SET_TAG_REQUESTS (state, payload) {
    state.tagRequests = payload
  },
  SET_SEARCH_POSTER (state, payload) {
    state.searchPoster = payload
  },
  SET_SEARCH_LIST (state, payload) {
    state.searchList = payload
  }
}

export const actions = {
  // ---------------- Authentication API Endpoints ----------------
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
    await this.$axios.delete('logout')
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
  // ---------------- Feed API Endpoints ----------------
  async getFeeds ({ commit }) {
    try {
      const { data } = await this.$axios.get('feed')
      commit('SET_FEEDS', data.data)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async getFeed ({ commit }, photoID) {
    try {
      const { data } = await this.$axios.get(`feed/${photoID}`)
      commit('SET_FEED', {
        ...data.data,
        tagged: [ ...data.tagged ],
        rating: [ ...data.rating ]
      })
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
  },
  // ---------------- Follower API Endpoints ----------------
  async getFollowRequests ({ commit }) {
    try {
      const { data } = await this.$axios.get('follow-request')
      console.log(data)
      commit('SET_FOLLOW_REQUESTS', data.follow_requests)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async createFollowRequest ({ state }) {
    try {
      await this.$axios.put(`create-follow/${state.username}`)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async updateFollowRequest ({ state, commit }, payload) {
    // accept: Boolean
    // follower: String
    try {
      const res = await this.$axios.post('follow-request', payload)
      if (res.status === 200) {
        const updatedTags = state.followRequests.filter(req => req.username_follower !== payload.follower)
        commit('SET_FOLLOW_REQUESTS', updatedTags)
      }
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  // ---------------- Follower API Endpoints ----------------
  async getTagRequests ({ commit }) {
    try {
      const { data } = await this.$axios.get('tag-request')
      console.log(data)
      commit('SET_TAG_REQUESTS', data.tag_requests)
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async createTagRequest ({ state, commit }, { photoID, tagged }) {
    try {
      const res = await this.$axios.post(`feed/${photoID}/addTag`, { tagged })
      const { username } = state
      if (res.status === 200 && state.username === tagged) {
        const updatedFeed = {
          ...state.feed,
          tagged: [
            ...state.feed.tagged,
            {
              username
            }
          ]
        }
        commit('SET_FEED', updatedFeed)
      }
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async updateTagRequest ({ state, commit }, payload) {
    // accept: Boolean
    // photoID: Integer
    try {
      const res = await this.$axios.post('tag-request', payload)
      if (res.status === 200) {
        const updatedTags = state.tagRequests.filter(req => req.photoID !== payload.photoID)
        commit('SET_TAG_REQUESTS', updatedTags)
      }
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async createLike ({ state, commit }, { photoID, rating }) {
    try {
      const res = await this.$axios.post(`feed/${photoID}/like`, { rating })
      const { username } = state
      if (res.status === 200) {
        const updatedFeed = {
          ...state.feed,
          rating: [
            ...state.feed.rating,
            {
              username,
              rating
            }
          ]
        }
        commit('SET_FEED', updatedFeed)
      }
    } catch (e) {
      throw e.response.data.errMsg
    }
  },
  async searchByPhotoPoster ({ commit }, poster) {
    try {
      const res = await this.$axios.post('search-by-poster', { poster })
      console.log(res)
      if (res.status === 200 && res.data.data.length > 0) {
        commit('SET_SEARCH_POSTER', poster)
        commit('SET_SEARCH_LIST', res.data.data)
      }
    } catch (e) {
      throw e.response.data.errMsg
    }
  }
}
