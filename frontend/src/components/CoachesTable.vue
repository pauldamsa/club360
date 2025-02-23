<template>
    <div v-if="coachesList" class="bg-white rounded-lg shadow">
        <!-- Search bar -->
        <div class="p-4 border-b border-gray-200">
            <div class="flex items-center space-x-2">
                <div class="w-full max-w-md">
                    <Input
                        type="text"
                        placeholder="Search coaches by name..."
                        v-model="searchTerm"
                        :icon="searchTerm ? 'x' : 'search'"
                        @icon-click="clearSearch"
                        @keyup.enter="performSearch"
                    />
                </div>
                <Button
                    variant="solid"
                    label="Search"
                    icon="search"
                    :loading="coachesResource.loading"
                    @click="performSearch"
                />
            </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Level</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sponsor</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr 
                        v-for="coach in coachesList" 
                        :key="coach.name" 
                        class="hover:bg-gray-50 cursor-pointer"
                        @click="navigateToDetails(coach)"
                    >
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <Avatar
                                    :label="coach.full_name"
                                    size="md"
                                    class="mr-3"
                                />
                                <div class="text-sm font-medium text-gray-900">{{ coach.full_name }}</div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Badge 
                                :label="coach.role"
                            />
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Badge 
                                :label="coach.level"
                            />
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-gray-500">{{ getSponsorName(coach.sponsor) }}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Button
                                variant="danger"
                                icon="trash-2"
                                size="sm"
                                @click.stop="deleteCoach(coach)"
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Delete Confirmation Dialog -->
        <Dialog
            :options="{
                title: 'Delete Coach',
                actions: [
                    {
                        label: 'Cancel',
                        variant: 'outline',
                        onClick: () => showDeleteDialog = false
                    },
                    {
                        label: 'Delete',
                        variant: 'danger',
                        onClick: confirmDelete
                    }
                ]
            }"
            v-model="showDeleteDialog"
        >
            <template #body-content>
                <p class="text-gray-600">
                    Are you sure you want to delete {{ coachToDelete?.full_name }}?
                </p>
                <div class="mt-2 text-sm text-gray-500">
                    Role: {{ coachToDelete?.role }}<br>
                    Level: {{ coachToDelete?.level }}
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { createListResource, Badge, Avatar, Button, Input, Dialog } from 'frappe-ui';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const searchTerm = ref('');

const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['*'],
    filters: computed(() => {
        if (!searchTerm.value) return {};
        return {
            full_name: ['like', `%${searchTerm.value}%`]
        };
    }),
    auto: true,
});

const sponsorsResource = createListResource({
    doctype: 'Coach',
    fields: ['id_herbalife', 'full_name'],
    auto: true
});

const getSponsorName = computed(() => {
    const sponsorsMap = {};
    if (sponsorsResource.list.data) {
        sponsorsResource.list.data.forEach(coach => {
            sponsorsMap[coach.id_herbalife] = coach.full_name;
        });
    }
    return (id_herbalife) => sponsorsMap[id_herbalife] || '-';
});

const coachesList = computed(() => {
    return coachesResource.list.data || [];
});

const showDeleteDialog = ref(false);
const coachToDelete = ref(null);

function clearSearch() {
    searchTerm.value = '';
    performSearch();
}

function performSearch() {
    coachesResource.reload();
}

function navigateToDetails(coach) {
    router.push({
        name: 'CoachDetailsPage',
        params: { id_herbalife: coach.id_herbalife }
    });
}

function deleteCoach(coach) {
    coachToDelete.value = coach;
    showDeleteDialog.value = true;
}

function confirmDelete() {
    if (!coachToDelete.value) return;
    console.log('Confirming delete for:', coachToDelete.value.full_name);
    // TODO: Implement actual delete API call
    showDeleteDialog.value = false;
    coachToDelete.value = null;
}
</script>