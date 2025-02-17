<template>
    <div v-if="clubMemberList" class="bg-white rounded-lg shadow">
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
                            <Badge :label="member.status" 
                                :class="{'bg-green-500 text-white opacity-75': member.status === 'Active', 'bg-red-500 text-white opacity-75': member.status === 'Inactive'}">
                                {{ member.status }}
                            </Badge>
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
import { createListResource, Badge, Avatar, Button } from 'frappe-ui';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const clubMemberResource = createListResource({
    doctype: 'Club Member',
    fields: ['full_name', 'first_name', 'last_name', 'coach', 'memberships', 'status'],
    auto: true,
})

const clubMemberList = computed(() => {
    if (clubMemberResource.list.data) {
        return clubMemberResource.list.data;
    }
    return [];
})

function navigateToDetails(member) {
    router.push({
        name: 'ClubMemberDetailsPage',
        params: { full_name: member.full_name }
    });
}
</script>