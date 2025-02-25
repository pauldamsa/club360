<template>
    <div class="flex flex-col p-6 space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <h1 class="text-2xl font-bold text-gray-900">Visits</h1>
                <span class="px-2 py-1 text-sm font-medium bg-red-100 text-gray-600 rounded-md">
                    {{ visitsList.length }}
                </span>
            </div>
            <Button 
                variant="solid" 
                label="Add Visit"
                @click="handleAddVisit"
            />
        </div>

        <!-- Visits Table -->
        <Card>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Club Member</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="visit in sortedVisits" :key="visit.name" class="hover:bg-gray-50">
                            <td class="px-6 py-4">
                                <div v-if="editingVisit === visit.name">
                                    <Select
                                        v-model="editableVisit.club_member"
                                        :options="clubMemberOptions"
                                        class="w-full"
                                    />
                                </div>
                                <div v-else class="flex items-center">
                                    <Avatar :label="visit.memberName" size="sm" class="mr-2" />
                                    <span class="text-sm font-medium">{{ visit.memberName }}</span>
                                </div>
                            </td>
                            <td class="px-6 py-4">
                                <Input 
                                    v-if="editingVisit === visit.name"
                                    type="date" 
                                    v-model="editableVisit.date"
                                    class="w-40"
                                />
                                <span v-else>{{ formatDate(visit.date) }}</span>
                            </td>
                            <td class="px-6 py-4">
                                <Select
                                    v-if="editingVisit === visit.name"
                                    v-model="editableVisit.type_event"
                                    :options="typeOptions"
                                    class="w-32"
                                />
                                <Badge 
                                    v-else
                                    :label="visit.type_event" 
                                    :class="{
                                        'bg-blue-100 text-blue-800': visit.type_event === 'Sport',
                                        'bg-green-100 text-green-800': visit.type_event === 'Breakfast'
                                    }"
                                />
                            </td>
                            <td class="px-6 py-4">
                                <div class="flex space-x-2">
                                    <template v-if="editingVisit === visit.name">
                                        <Button
                                            variant="solid"
                                            icon="check"
                                            size="sm"
                                            @click="handleSaveVisit"
                                        />
                                        <Button
                                            variant="outline"
                                            icon="x"
                                            size="sm"
                                            @click="handleCancelEdit"
                                        />
                                    </template>
                                    <template v-else>
                                        <Button
                                            variant="outline"
                                            icon="edit-2"
                                            size="sm"
                                            @click="handleEditVisit(visit)"
                                        />
                                        <Button
                                            variant="danger"
                                            icon="trash-2"
                                            size="sm"
                                            @click="handleDeleteVisit(visit)"
                                        />
                                    </template>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </Card>
        <AddVisitDialog 
            ref="addVisitDialog" 
            @visitAdded="handleVisitAdded" 
        />

        <!-- Delete Confirmation Dialog -->
        <Dialog
            :options="{
                title: 'Delete Visit',
                actions: [
                    {
                        label: 'Cancel',
                        variant: 'outline',
                        onClick: () => showDeleteDialog = false
                    },
                    {
                        label: 'Delete',
                        variant: 'danger',
                        onClick: confirmDeleteVisit
                    }
                ]
            }"
            v-model="showDeleteDialog"
        >
            <template #body-content>
                <p class="text-gray-600">
                    Are you sure you want to delete this visit?
                </p>
                <div class="mt-2 text-sm text-gray-500">
                    <p>Member: {{ visitToDelete?.memberName }}</p>
                    <p>Date: {{ formatDate(visitToDelete?.date) }}</p>
                    <p>Type: {{ visitToDelete?.type_event }}</p>
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Button, Card, Avatar, Badge, createListResource, Input, Select, createResource, Dialog } from 'frappe-ui';
import AddVisitDialog from '@/components/AddVisitDialog.vue';

// Add club members resource for name mapping
const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    auto: true
});

// Create mapping for member names
const memberNames = computed(() => {
    const mapping = {};
    if (clubMembersResource.list.data) {
        clubMembersResource.list.data.forEach(member => {
            mapping[member.name] = member.full_name;
        });
    }
    return mapping;
});

// Club member options for select
const clubMemberOptions = computed(() => {
    if (!clubMembersResource.list.data) return [];
    return clubMembersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.name
    }));
});

const visitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name', 'club_member', 'date', 'type_event'],
    orderBy: 'creation desc',
    auto: true
});


const deleteVisit = createResource({
    url: 'club360.api.delete_visit',
    makeParams: (values) => ({
        visit: editableVisit.value
    })
});

const visitsList = computed(() => visitsResource.list.data || []);

// Update sorted visits to include member names
const sortedVisits = computed(() => {
    return [...visitsList.value]
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .map(visit => ({
            ...visit,
            memberName: memberNames.value[visit.club_member] || visit.club_member
        }));
});

const editingVisit = ref(null);
const editableVisit = ref(null);

const typeOptions = [
    { label: 'Sport', value: 'Sport' },
    { label: 'Breakfast', value: 'Breakfast' }
];

const addVisitDialog = ref(null);

const showDeleteDialog = ref(false);
const visitToDelete = ref(null);

// Add delete visit resource
const deleteVisitResource = createResource({
    url: 'club360.api.delete_visit',
    makeParams() {
        return {
            visit: visitToDelete.value
        };
    },
    onSuccess() {
        showDeleteDialog.value = false;
        visitToDelete.value = null;
        visitsResource.reload();
    }
});

function formatDate(date) {
    return new Date(date).toLocaleDateString();
}

function handleAddVisit() {
    addVisitDialog.value?.openDialog();
}

function handleVisitAdded() {
    // Reload visits list
    visitsResource.reload();
}

function handleEditVisit(visit) {
    editingVisit.value = visit.name;
    editableVisit.value = { ...visit };
}

function handleSaveVisit() {
    // TODO: Implement API call
    const index = sortedVisits.value.findIndex(v => v.name === editingVisit.value);
    if (index !== -1) {
        sortedVisits.value[index] = { ...editableVisit.value };
    }
    editingVisit.value = null;
    editableVisit.value = null;
}

function handleCancelEdit() {
    editingVisit.value = null;
    editableVisit.value = null;
}

function handleDeleteVisit(visit) {
    visitToDelete.value = visit;
    showDeleteDialog.value = true;
}

function confirmDeleteVisit() {
    if (!visitToDelete.value) return;
    deleteVisitResource.submit();
}
</script>