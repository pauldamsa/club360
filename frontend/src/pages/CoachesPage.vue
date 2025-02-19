<template>
    <div class="flex flex-col p-6 space-y-6">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <h1 class="text-2xl font-bold text-gray-900">All Coaches</h1>
                <span class="px-2 py-1 text-sm font-medium bg-red-100 text-gray-600 rounded-md">
                    {{ 10 }}
                </span>
            </div>
            <Button 
                variant="solid" 
                label="Add Coach" 
            />
        </div>

        <CoachesTable />
    </div>

    
</template>

<script setup>
import CoachesTable from '@/components/CoachesTable.vue';
</script>