<template>
    <div class="flex flex-col p-4 md:p-6 space-y-4 md:space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex items-center space-x-2">
                <h1 class="text-xl md:text-2xl font-bold text-gray-900">All Club Members</h1>
                <span class="px-2 py-1 text-sm font-medium bg-red-100 text-gray-600 rounded-md">
                    {{ memberCount }}
                </span>
            </div>
            <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
                <Button 
                    variant="outline" 
                    label="To Be Inactive Members" 
                    class="w-full sm:w-auto"
                    @click="navigateToAttentionPage"
                />
                <Button 
                    variant="solid" 
                    label="Add Member" 
                    class="w-full sm:w-auto"
                    @click="addMemberDialog.openDialog()"
                />
            </div>
        </div>

        <ClubMemberTable ref="memberTable" />
        <AddMemberDialog 
            ref="addMemberDialog"
            @memberAdded="handleMemberAdded"
        />
    </div>
</template>

<script setup>
import { ref, computed, nextTick, onBeforeUnmount } from 'vue';
import { createListResource } from 'frappe-ui';
import { useRouter } from 'vue-router';
import ClubMemberTable from '@/components/ClubMemberTable.vue';
import AddMemberDialog from '@/components/AddMemberDialog.vue';
import { session } from '@/data/session';

const router = useRouter();
const memberTable = ref(null);
const addMemberDialog = ref(null);

const clubMemberResource = createListResource({
  doctype: 'Club Member',
  fields:["full_name", "first_name", "last_name", "coach", "memberships", "status"],
  filters: {
    owner: session.user
  },
  auto: true
})

const clubMemberList = computed(() => {
  if (clubMemberResource.list.data) {
    return clubMemberResource.list.data;
  }
  return [];
})

const memberCount = computed(() => {
    return clubMemberList.value.length || 0;
});

function handleMemberAdded() {
    // Only reload the main resource
    clubMemberResource.reload();
    
    // Reload the table component if it exists and has a reload method
    if (memberTable.value?.clubMemberResource?.reload) {
        memberTable.value.clubMemberResource.reload();
    } else {
        // Force a re-render of the table component
        nextTick(() => {
            if (memberTable.value?.clubMemberResource?.reload) {
                memberTable.value.clubMemberResource.reload();
            }
        });
    }
}

function navigateToAttentionPage() {
    // Simple direct navigation to the correct path
    window.location.href = '/members/expire';
}

</script>