<template>
    <div v-if="clubMemberList" class="bg-white rounded-lg shadow">
        <!-- Add search bar -->
        <div class="p-4 border-b border-gray-200">
            <div class="flex items-center space-x-2">
                <div class="w-full max-w-md">
                    <Input
                        type="text"
                        placeholder="Search members by name..."
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
                    :loading="clubMemberResource.loading"
                    @click="performSearch"
                />
            </div>
        </div>

        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Coach</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Visits Left</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr 
                        v-for="member in clubMemberList" 
                        :key="member.name" 
                        class="hover:bg-gray-50 cursor-pointer"
                        @click="navigateToDetails(member)"
                    >
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <Avatar
                                    :label="member.full_name"
                                    size="md"
                                    class="mr-3"
                                />
                                <div class="text-sm font-medium text-gray-900">{{ member.full_name }}</div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Badge :label="member.coach" >{{ member.coach }}</Badge>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ member.status }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            1
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

const clubMemberResource = createListResource({
    doctype: 'Club Member',
    fields: ['full_name', 'first_name', 'last_name', 'coach', 'memberships', 'status'],
    filters: computed(() => {
        if (!searchTerm.value) return {};
        return {
            full_name: ['like', `%${searchTerm.value}%`]
        };
    }),
    auto: true,
});

const clubMemberList = computed(() => {
    if (clubMemberResource.list.data) {
        return clubMemberResource.list.data;
    }
    return [];
})

function clearSearch() {
    searchTerm.value = '';
    performSearch();
}

function performSearch() {
    clubMemberResource.reload();
}

function navigateToDetails(member) {
    router.push({
        name: 'ClubMemberDetailsPage',
        params: { full_name: member.full_name }
    });
}
</script>