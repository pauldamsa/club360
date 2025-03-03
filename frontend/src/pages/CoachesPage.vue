<template>
    <div class="flex flex-col p-4 md:p-6 space-y-4 md:space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0">
            <div class="flex items-center space-x-2">
                <h1 class="text-xl md:text-2xl font-bold text-gray-900">All Coaches</h1>
                <span class="px-2 py-1 text-sm font-medium bg-red-100 text-gray-600 rounded-md">
                    {{ coachCount }}
                </span>
            </div>
            <Button 
                variant="solid" 
                label="Add Coach"
                @click="addCoachDialog.openDialog()"
                class="w-full sm:w-auto"
            />
        </div>
        <CoachesTable ref="coachesTable" />
        <AddCoachDialog ref="addCoachDialog" @coachAdded="handleCoachAdded" />
    </div>
</template>

<script setup>
import CoachesTable from '@/components/CoachesTable.vue';
import AddCoachDialog from '@/components/AddCoachDialog.vue';
import { ref, computed } from 'vue';
import { createListResource } from 'frappe-ui';
import { session } from '@/data/session';

const addCoachDialog = ref(null);
const coachesTable = ref(null);

const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['name'],
    filters: {
        owner: session.user
    },
    auto: true
});

const coachCount = computed(() => {
    return coachesResource.list.data?.length || 0;
});

function handleCoachAdded() {
    // Reload both resources
    coachesResource.reload();
    if (coachesTable.value?.coachesResource) {
        coachesTable.value.coachesResource.reload();
    }
}

function handleCoachDeleted() {
    // Reload both resources
    coachesResource.reload();
    if (coachesTable.value?.coachesResource) {
        coachesTable.value.coachesResource.reload();
    }
}
</script>