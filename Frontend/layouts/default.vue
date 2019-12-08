<template>
  <v-app>
    <ToolBar />
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import ToolBar from '@/components/ToolBar'

export default {
  components: {
    ToolBar
  },
  data () {
    return {
      title: 'Finstagram'
    }
  }
}
</script>
