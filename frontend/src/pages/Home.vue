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

    <div class = "mt-8 space-y-4">
      <h3 class="font-bold text-lg text-gray-600">Club Stats</h3>
      <p>Total Visits: 1000</p>
      <p>Average visits per day (last month): 10</p>
      <p>Active Members: 100</p>
      <p>Memberships: 300</p>
      <p>Referrals: 20</p>
      <p>Active Coaches: 10</p>
      
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
