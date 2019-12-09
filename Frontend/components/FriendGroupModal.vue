<template>
  <v-dialog v-model="isOpen" persistent max-width="500px">
    <v-card>
      <v-card-title>
        Add New Friend Group
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row align="center" justify="center">
            <v-text-field
              v-model="groupName"
              label="Group Name"
              outlined
            />
          </v-row>
          <v-row align="center" justify="center">
            <v-textarea
              v-model="description"
              label="Group Description"
              no-resize
              outlined
            />
          </v-row>
        </v-container>
        <small>{{ errMsg }}</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="submitFriendGroup(groupName, description)" color="primary" text>
          Submit
        </v-btn>
        <v-btn @click="toggleModal" color="error" text>
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'FriendGroupAddModal',
  props: {
    isOpen: Boolean
  },
  data () {
    return {
      groupName: '',
      description: '',
      errMsg: ''
    }
  },
  methods: {
    submitFriendGroup (groupName, description) {
      this.$store.dispatch('createFriendGroup', { groupName, description })
        .then(() => {
          this.groupName = ''
          this.description = ''
          this.errMsg = ''
          this.toggleModal()
        })
        .catch((e) => { this.errMsg = e })
    },
    toggleModal () {
      this.$emit('toggleModal')
    }
  }
}
</script>
