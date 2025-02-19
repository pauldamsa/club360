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
                                class="bg-blue-100 text-blue-800"
                            />
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Badge 
                                :label="coach.level"
                                class="bg-purple-100 text-purple-800"
                            />
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span v-if="coach.sponsor" class="text-gray-500">{{ coach.sponsor }}</span>
                            <span v-else class="text-gray-500">-</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { createListResource, Badge, Avatar, Button, Input } from 'frappe-ui';
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

const coachesList = computed(() => {
    return coachesResource.list.data || [];
});

function clearSearch() {
    searchTerm.value = '';
    performSearch();
}

function performSearch() {
    coachesResource.reload();
}

function navigateToDetails(coach) {
    // router.push({
    //     name: 'CoachDetailsPage',
    //     params: { full_name: coach.full_name }
    // });
}
</script>