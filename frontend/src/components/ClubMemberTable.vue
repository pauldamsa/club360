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
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
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
                            <Badge :label="coachNameMap[member.coach] || 'No Coach'">
                                {{ coachNameMap[member.coach] || 'No Coach' }}
                            </Badge>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ member.status }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <Button
                                variant="danger"
                                icon="trash-2"
                                size="sm"
                                @click.stop="deleteMember(member)"
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
            <!-- Add pagination controls -->
            <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3">
                <div class="flex flex-1 justify-between items-center">
                    <div class="text-sm text-gray-700">
                        <!-- Page {{ clubMemberResource.currentPage }} of {{ Math.ceil(clubMemberResource.totalCount / clubMemberResource.pageLength) }} -->
                    </div>
                    <div class="flex items-center space-x-2">
                        <Button 
                            variant="outline" 
                            size="sm"
                            :disabled="!clubMemberResource?.hasPreviousPage"
                            @click="clubMemberResource.previous()"
                        >
                            Previous
                        </Button>
                        <Button 
                            variant="outline" 
                            size="sm"
                            :disabled="!clubMemberResource?.hasNextPage"
                            @click="clubMemberResource.next()"
                        >
                            Next
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <Dialog
        :options="{
            title: 'Delete Member',
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
                Are you sure you want to delete {{ memberToDelete?.full_name }}?
            </p>
        </template>
    </Dialog>
</template>

<script setup>
import { createListResource, createResource, Badge, Avatar, Button, Input, Dialog } from 'frappe-ui';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { session } from '@/data/session';

const router = useRouter();
const searchTerm = ref('');

const clubMemberResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name', 'first_name', 'last_name', 'coach', 'memberships', 'status'],
    filters: computed(() => ({
        owner: session.user,
        ...(searchTerm.value ? { full_name: ['like', `%${searchTerm.value}%`] } : {})
    })),
    orderBy: 'creation desc',
    auto: true,
    pageLength: 10,
    pagination: true
});

// Expose the resource for parent component
defineExpose({
    clubMemberResource
});

const clubMemberList = computed(() => {
    if (clubMemberResource.list.data) {
        return clubMemberResource.list.data;
    }
    return [];
})

const deleteResource = createResource({
    url: 'club360.api.delete_club_member',
    makeParams() {
        return {
            club_member: memberToDelete.value
        };
    }
});

const showDeleteDialog = ref(false);
const memberToDelete = ref(null);

// Add coach resource to get mapping
const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['id_herbalife', 'full_name'],
    auto: true
});

// Add coach name mapping
const coachNameMap = computed(() => {
    const mapping = {};
    if (coachesResource.list.data) {
        coachesResource.list.data.forEach(coach => {
            mapping[coach.id_herbalife] = coach.full_name;
        });
    }
    return mapping;
});

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
        params: { id_club_member: member.name }
    });
}

function deleteMember(member) {
    memberToDelete.value = member;
    showDeleteDialog.value = true;
}

function confirmDelete() {
    if (!memberToDelete.value) return;
    
    deleteResource.submit().then(() => {
        showDeleteDialog.value = false;
        memberToDelete.value = null;
        clubMemberResource.reload().then(() => {
            console.log('Member deleted successfully');
        });
    }).catch(error => {
        console.error('Error deleting member:', error);
    });
}
</script>