<template>
    <div class="flex flex-col p-6 space-y-6">
        <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold text-gray-900">All Members</h1>
            <Button variant="solid" label="Add Member" />
        </div>

        <ClubMemberTable />
    </div>
</template>

<script setup>
import ClubMemberTable from '@/components/ClubMemberTable.vue';
</script>