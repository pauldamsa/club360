<template>
  <div class="max-w-3xl py-12 mx-auto">
    <h2 class="font-bold text-lg text-gray-600 mb-4">
      Welcome {{ session.user }}!
    </h2>

    <div class="flex space-x-4">
      <Button
        variant="solid"
        label="Add Club Member"
        @click="addMemberDialog.openDialog()"
      />
      <Button
        variant="solid"
        label="Add visits"
      />
      <Button
        variant="solid"
        label="Add Coach"
      />
    </div>

    <AddMemberDialog ref="addMemberDialog" @memberAdded="handleMemberAdded" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, Button } from 'frappe-ui'
import { session } from '../data/session'
import AddMemberDialog from '@/components/AddMemberDialog.vue'

const addMemberDialog = ref(null)

function handleMemberAdded() {
  // Handle successful member addition
  console.log('Member added successfully')
}
</script>
