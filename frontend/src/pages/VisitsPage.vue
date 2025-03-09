<template>
    <div class="flex flex-col p-4 md:p-6 space-y-4 md:space-y-6">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
            <div class="flex items-center space-x-2">
                <h1 class="text-xl md:text-2xl font-bold text-gray-900">Visits</h1>
                <span class="px-2 py-1 text-sm font-medium bg-red-100 text-gray-600 rounded-md">
                    {{ visitsList.length }}
                </span>
            </div>
            <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
                <Button 
                    variant="outline" 
                    label="Export PDF"
                    icon="file-text"
                    @click="exportToPDF"
                    class="w-full sm:w-auto"
                />
                <Button 
                    variant="solid" 
                    label="Add Visit"
                    @click="handleAddVisit"
                    class="w-full sm:w-auto"
                />
            </div>
        </div>

        <!-- Filters Card -->
        <Card class="mb-4">
            <div class="p-4 space-y-4">
                <div class="space-y-4">
                    <FormControl
                        type="autocomplete"
                        label="Filter by Member"
                        v-model="filters.member"
                        :options="clubMemberOptions"
                        placeholder="Select member"
                        class="w-full"
                    />
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <FormControl
                            type="date"
                            label="From Date"
                            v-model="filters.fromDate"
                            class="w-full"
                        />
                        <FormControl
                            type="date"
                            label="To Date"
                            v-model="filters.toDate"
                            class="w-full"
                        />
                    </div>
                </div>
                <div class="flex flex-col sm:flex-row sm:justify-end space-y-2 sm:space-y-0 sm:space-x-2">
                    <Button 
                        variant="outline" 
                        label="Reset" 
                        @click="resetFilters"
                        class="w-full sm:w-auto"
                    />
                    <Button 
                        variant="solid" 
                        label="Apply Filters"
                        @click="applyFilters"
                        class="w-full sm:w-auto"
                    />
                </div>
            </div>
        </Card>

        <!-- Visits List -->
        <Card>
            <!-- Mobile View -->
            <div class="block sm:hidden">
                <div class="divide-y divide-gray-200">
                    <div v-for="visit in sortedVisits" 
                         :key="visit.name" 
                         class="p-4 space-y-3"
                    >
                        <!-- Display View -->
                        <div v-if="editingVisit !== visit.name">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <Avatar :label="visit.memberName" size="sm" />
                                    <div>
                                        <div class="font-medium">{{ visit.memberName }}</div>
                                        <div class="text-sm text-gray-500">{{ formatDate(visit.date) }}</div>
                                    </div>
                                </div>
                                <Badge 
                                    :label="visit.type_event" 
                                    :class="{
                                        'bg-blue-100 text-blue-800': visit.type_event === 'Sport',
                                        'bg-green-100 text-green-800': visit.type_event === 'Breakfast'
                                    }"
                                />
                            </div>
                            <div class="flex justify-end space-x-2">
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
                            </div>
                        </div>

                        <!-- Edit View -->
                        <div v-else class="space-y-3">
                            <FormControl
                                type="autocomplete"
                                label="Member"
                                v-model="editableVisit.club_member"
                                :options="clubMemberOptions"
                                class="w-full"
                            />
                            <FormControl
                                type="date"
                                label="Date"
                                v-model="editableVisit.date"
                                class="w-full"
                            />
                            <FormControl
                                type="select"
                                label="Type"
                                v-model="editableVisit.type_event"
                                :options="typeOptions"
                                class="w-full"
                            />
                            <div class="flex justify-end space-x-2 pt-2">
                                <Button
                                    variant="solid"
                                    label="Save"
                                    icon="check"
                                    size="sm"
                                    @click="handleSaveVisit"
                                    :loading="editVisitResource.loading"
                                    class="w-1/2"
                                />
                                <Button
                                    variant="outline"
                                    label="Cancel"
                                    icon="x"
                                    size="sm"
                                    @click="handleCancelEdit"
                                    class="w-1/2"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Desktop Table View -->
            <div class="hidden sm:block overflow-x-auto">
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
                                            :loading="editVisitResource.loading"
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

            <!-- Pagination -->
            <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3">
                <div class="flex flex-1 justify-between items-center">
                    <div class="flex space-x-2">
                        <Button 
                            variant="outline" 
                            size="sm"
                            :disabled="!visitsResource?.hasPreviousPage"
                            @click="visitsResource.previous()"
                            class="w-24"
                        >
                            Previous
                        </Button>
                        <Button 
                            variant="outline" 
                            size="sm"
                            :disabled="!visitsResource?.hasNextPage"
                            @click="visitsResource.next()"
                            class="w-24"
                        >
                            Next
                        </Button>
                    </div>
                </div>
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
import { Button, Card, Avatar, Badge, createListResource, Input, Select, createResource, Dialog, FormControl } from 'frappe-ui';
import AddVisitDialog from '@/components/AddVisitDialog.vue';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { session } from '@/data/session';

// Add club members resource for name mapping
const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    filters: {
        owner: session.user
    },
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
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

// Add filters state
const filters = ref({
    member: null,
    fromDate: null,
    toDate: null
});

const visitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name', 'club_member', 'date', 'type_event'],
    orderBy: 'creation desc',
    auto: true,
    pageLength: 10,
    pagination: true,
    filters: computed(() => ({
        owner: session.user,
        ...(filters.value.member && { club_member: filters.value.member.value }),
        ...(filters.value.fromDate && { date: filters.value.toDate ? 
            ['between', [filters.value.fromDate, filters.value.toDate]] :
            ['>=', filters.value.fromDate]
        }),
        ...(!filters.value.fromDate && filters.value.toDate && { date: ['<=', filters.value.toDate] })
    }))
});

// Add total visits count resource
const totalVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name'],
    filters: {
        owner: session.user
    },
    pageLength: 99999, // Set a large number to get all records
    auto: true
});

// Add filter functions
function resetFilters() {
    filters.value = {
        member: null,
        fromDate: null,
        toDate: null
    };
    visitsResource.reload();
}

function applyFilters() {
    visitsResource.reload();
}

const visitsList = computed(() => totalVisitsResource.list.data || []);

// Remove the sorting from computed property since we're using server-side ordering
const sortedVisits = computed(() => {
    return (visitsResource.list.data || []).map(visit => ({
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

// Add edit visit resource
const editVisitResource = createResource({
    url: 'club360.api.edit_visit',
    makeParams() {
        return {
            visit_data: editableVisit.value
        };
    },
    onSuccess() {
        editingVisit.value = null;
        editableVisit.value = null;
        visitsResource.reload();
    },
    onError: (error) => {
        console.error('Error editing visit:', error);
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
    if (!editableVisit.value) return;
    editVisitResource.submit();

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

// Add a new resource for filtered exports
const exportVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name', 'club_member', 'date', 'type_event'],
    orderBy: 'date desc',
    auto: false,
    filters: computed(() => ({
        owner: session.user,
        ...(filters.value.fromDate && { date: filters.value.toDate ? 
            ['between', [filters.value.fromDate, filters.value.toDate]] :
            ['>=', filters.value.fromDate]
        }),
        ...(filters.value.toDate && !filters.value.fromDate && { date: ['<=', filters.value.toDate] })
    }))
});

async function exportToPDF() {
    // Load filtered data first
    await exportVisitsResource.reload();
    
    const doc = new jsPDF();
    
    // Add title and date range
    doc.setFontSize(16);
    doc.text('Visits Report', 14, 15);
    doc.setFontSize(11);
    doc.text(`Generated on ${new Date().toLocaleDateString()}`, 14, 25);
    
    // Add date range if filters are set
    if (filters.value.fromDate || filters.value.toDate) {
        const dateRange = `Date Range: ${filters.value.fromDate || 'Start'} to ${filters.value.toDate || 'End'}`;
        doc.text(dateRange, 14, 35);
    }

    // Prepare data for table using filtered data
    const tableData = (exportVisitsResource.list.data || []).map(visit => [
        memberNames.value[visit.club_member] || visit.club_member,
        formatDate(visit.date),
        visit.type_event
    ]);

    // Add table with adjusted starting position
    autoTable(doc, {
        head: [['Member', 'Date', 'Type']],
        body: tableData,
        startY: filters.value.fromDate || filters.value.toDate ? 40 : 30,
        theme: 'grid'
    });

    // Save PDF
    const fileName = `visits-report${filters.value.fromDate ? '-from-' + filters.value.fromDate : ''}${filters.value.toDate ? '-to-' + filters.value.toDate : ''}.pdf`;
    doc.save(fileName);
}
</script>