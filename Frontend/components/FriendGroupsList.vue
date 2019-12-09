<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Friend Groups
        </v-list-item-title>
      </v-list-item-content>
      <v-row
        align="center"
        justify="end"
      >
        <v-btn
          @click="toggleModal"
          class="request__button"
          color="primary"
          text
        >
          ADD NEW FRIEND GROUP
        </v-btn>
      </v-row>
    </v-list-item>
    <v-divider />
    <v-container>
      <v-row>
        <v-col
          v-for="(group, index) in friendGroups"
          :key="index"
          class="d-flex child-flex"
          cols="3"
        >
          <v-card elevation="1">
            <v-card-title primary-title>
              {{ group.groupName }}
            </v-card-title>
            <v-card-subtitle>
              {{ group.description }}
            </v-card-subtitle>
            <v-container v-if="username === group.groupOwner">
              <v-text-field
                @click:append="addFriendToGroup(index, group.groupName)"
                :ref="index"
                append-icon="mdi-account-plus-outline"
                label="Add Friend"
                dense
                outlined
              />
              <small :ref="`${index}-errMsg`">{{ errMsg }}</small>
            </v-container>
            <v-divider />
            <v-list disabled>
              <v-subheader>Members</v-subheader>
              <v-list-item-group>
                <v-list-item v-for="member in group.members" :key="member.index">
                  <v-list-item-content>
                    <v-list-item-title :class="member === group.groupOwner ? 'font-weight-bold' : ''">
                      {{ member }}
                    </v-list-item-title>
                  </v-list-item-content>
                  <v-spacer />
                  <v-icon v-if="member === group.groupOwner">
                    mdi-crown
                  </v-icon>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
      <v-list-item v-if="friendGroups.length === 0">
        <v-list-item-content>
          <v-list-item-title class="font-weight-bold">
            No Friend Groups
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-container>
    <FriendGroupModal :isOpen="isFriendGroupModalOpen" @toggleModal="toggleModal"/>
  </v-card>
</template>

<script>
import FriendGroupModal from '@/components/FriendGroupModal'

export default {
  name: 'FriendGroupsList',
  components: {
    FriendGroupModal
  },
  data () {
    return {
      isFriendGroupModalOpen: false,
      errMsg: ''
    }
  },
  computed: {
    friendGroups () {
      return this.$store.getters.getFriendGroups
    },
    username () {
      return this.$store.state.username
    }
  },
  methods: {
    addFriendToGroup (ref, groupName) {
      const memberName = this.$refs[ref][0].internalValue
      this.$store.dispatch('addFriendToGroup', { memberName, groupName })
        .then(() => {
          this.$refs[ref][0].internalValue = ''
        })
        .catch((e) => {
          this.$refs[`${ref}-errMsg`][0].textContent = e
          this.$refs[ref][0].internalValue = ''
          setTimeout(() => {
            this.$refs[`${ref}-errMsg`][0].textContent = ''
          }, 3000)
        })
    },
    toggleModal () {
      this.isFriendGroupModalOpen = !this.isFriendGroupModalOpen
    }
  }
}
</script>
