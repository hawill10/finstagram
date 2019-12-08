<template>
  <v-layout
    fill-height
    justify-center
    align-center
  >
    <v-flex d-flex justify-center align-center>
      <div class="auth__container">
        <h1 class="auth__container__header">
          Finstagram
        </h1>
        <label class="auth__container__label">Username</label>
        <v-text-field
          v-model="username"
          single-line
          outlined
          dense
        />
        <label class="auth__container__label">Password</label>
        <v-text-field
          v-model="password"
          :type="'password'"
          single-line
          outlined
          dense
        />
        <div class="auth__button__container">
          <v-btn @click="toggleLogin" color="primary" class="auth__button">
            LOGIN
          </v-btn>
          <v-btn @click="toggleModal" class="auth__button">
            REGISTER
          </v-btn>
        </div>
      </div>
    </v-flex>
    <v-alert
      v-model="alert"
      :close-text="closeAlert"
      border="left"
      type="error"
      transition="slide-y-transition"
      dismissible
      class="auth__alert"
    >
      {{ error }}
    </v-alert>
    <RegisterModal @toggleModal="toggleModal" :isOpen="isOpen" />
  </v-layout>
</template>

<script>
import RegisterModal from '@/components/RegisterModal'
export default {
  layout: 'auth',
  components: {
    RegisterModal
  },
  middleware ({ store, redirect }) {
    // If the user is authenticated
    if (store.state.username && store.state.token) {
      redirect('/feed')
    }
  },
  data () {
    return {
      username: '',
      password: '',
      error: '',
      alert: false,
      isOpen: false
    }
  },
  methods: {
    toggleLogin () {
      const { username, password } = this
      this.$store.dispatch('login', {
        username,
        password
      })
        .then(() => this.$router.push('/feed'))
        .catch((e) => {
          this.alert = true
          this.error = e
        })
    },
    toggleModal () {
      this.isOpen = !this.isOpen
    },
    closeAlert () {
      this.alert = !this.alert
    }
  }
}
</script>

<style lang="scss">
.auth {
  &__container {
    height: 100%;
    width: 30%;
    min-width: 320px;
    &__label {
      color: grey;
      font-size: 0.8rem;
    }
    &__header {
      margin-bottom: 16px;
    }
  }
  &__button {
    flex: 1;
    & + & {
      margin-left: 16px;
    }
    &__container {
      display: flex;
      margin: 16px 0;
    }
  }
  &__alert {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
