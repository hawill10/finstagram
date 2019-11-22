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
          <v-btn color="primary" class="auth__button">
            LOGIN
          </v-btn>
          <v-btn class="auth__button">
            REGISTER
          </v-btn>
        </div>
        <v-alert
          v-model="alert"
          border="left"
          close-text="Close Alert"
          type="error"
          transition="slide-y-transition"
          dismissible
          class="auth__alert"
        >
          Login Failed.
        </v-alert>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  layout: 'auth',
  data () {
    return {
      username: '',
      password: ''
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
