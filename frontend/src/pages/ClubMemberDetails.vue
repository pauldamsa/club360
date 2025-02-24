<template>
    <div class="p-6">
        <!-- Header section -->
        <div class="mb-8 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <Avatar :label="clubMemberDoc.full_name" size="xl" />
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">{{ clubMemberDoc.full_name }}</h1>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <Button 
                    variant="solid" 
                    label="Edit Member" 
                    @click="handleEditMember"
                />
            </div>
        </div>

        <!-- Main content -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Member Details Card -->
            <Card class="lg:col-span-1">
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="text-gray-500">First Name</div>
                        <div>{{ clubMemberDoc.first_name }}</div>
                        
                        <div class="text-gray-500">Last Name</div>
                        <div>{{ clubMemberDoc.last_name }}</div>
                        
                        <div class="text-gray-500">Coach</div>
                        <div>
                            <Badge :label="coachName" />
                        </div>
                        
                        <div class="text-gray-500">Source</div>
                        <div>{{ clubMemberDoc.source }}</div>

                        <template v-if="clubMemberDoc.source === 'Referral'">
                            <div class="text-gray-500">Referral of</div>
                            <div>
                                <Badge :label="referralName" />
                            </div>
                        </template>
                        
                        <div class="text-gray-500">Referrals</div>
                        <div>{{ clubMemberDoc.referrals }}</div>
                    </div>
                </div>
            </Card>

            <!-- Memberships Card -->
            <Card class="lg:col-span-2">
                <div class="space-y-4">
                    <div class="flex justify-between items-center border-b border-gray-200 pb-4">
                        <h2 class="text-lg font-medium">Memberships</h2>
                        <div class="flex space-x-2">
                            <Button 
                                variant="outline" 
                                label="Edit"
                                icon="edit-2"
                                @click="isEditing = !isEditing"
                            />
                            <Button 
                                variant="solid" 
                                label="Add New"
                                icon="plus"
                                @click="handleAddMembership"
                            />
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead>
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Start Date</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">End Date</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Remaining Visits</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr v-for="(membership, index) in editableMemberships" 
                                    :key="index" 
                                    class="hover:bg-gray-50"
                                >
                                    <td class="px-4 py-3">
                                        <div v-if="isEditing">
                                            <Select
                                                v-model="editableMemberships[index].type"
                                                :options="membershipTypes"
                                            />
                                        </div>
                                        <span v-else>{{ membership.type }}</span>
                                    </td>
                                    <td class="px-4 py-3">
                                        <div v-if="isEditing">
                                            <Input type="date" v-model="editableMemberships[index].start_date" />
                                        </div>
                                        <span v-else>{{ formatDate(membership.start_date) }}</span>
                                    </td>
                                    <td class="px-4 py-3">
                                        <div v-if="isEditing">
                                            <Input type="date" v-model="editableMemberships[index].end_date" />
                                        </div>
                                        <span v-else>{{ formatDate(membership.end_date) }}</span>
                                    </td>
                                    <td class="px-4 py-3">
                                        <div v-if="isEditing">
                                            <Input type="number" v-model="editableMemberships[index].remaining_visits" />
                                        </div>
                                        <Badge v-else 
                                            :label="membership.remaining_visits" 
                                            variant="solid" 
                                            :class="{
                                                'bg-green-100 text-green-800': membership.remaining_visits > 5,
                                                'bg-yellow-100 text-yellow-800': membership.remaining_visits <= 5 && membership.remaining_visits > 0,
                                                'bg-red-100 text-red-800': membership.remaining_visits === 0
                                            }"
                                        />
                                    </td>
                                    <td class="px-4 py-3">
                                        <Button
                                            variant="danger"
                                            icon="trash-2"
                                            size="sm"
                                            @click="deleteMembership(index)"
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div v-if="isEditing" class="flex justify-end space-x-2 pt-4 border-t">
                        <Button 
                            variant="outline" 
                            label="Cancel" 
                            @click="cancelEdit"
                        />
                        <Button 
                            variant="solid" 
                            label="Save Changes"
                            @click="saveMembershipChanges"
                        />
                    </div>
                </div>
            </Card>
        </div>

        <!-- Referrals Section -->
        <div class="mt-6">
            <Card>
                <div class="space-y-4">
                    <h2 class="text-lg font-medium mb-4">Member Referrals</h2>
                    <div v-if="referralsList.length === 0" class="text-gray-500 text-center py-4">
                        No referrals yet
                    </div>
                    <div v-else class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead>
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr v-for="referral in referralsList" :key="referral.name" class="hover:bg-gray-50">
                                    <td class="px-6 py-4">
                                        <div class="flex items-center">
                                            <Avatar :label="referral.full_name" size="sm" class="mr-2" />
                                            <span>{{ referral.full_name }}</span>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4">
                                        <Badge :label="referral.status" />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </Card>
        </div>
    </div>
    <!-- Delete Confirmation Dialog -->
    <!--<Dialog
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
    </Dialog> -->
    <EditMemberDialog ref="editMemberDialog" />

    <!-- Membership Delete Dialog -->
    <Dialog
        :options="{
            title: 'Delete Membership',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showMembershipDeleteDialog = false
                },
                {
                    label: 'Delete',
                    variant: 'danger',
                    onClick: confirmMembershipDelete
                }
            ]
        }"
        v-model="showMembershipDeleteDialog"
    >
        <template #body-content>
            <p class="text-gray-600">
                Are you sure you want to delete this membership?
            </p>
            <div class="mt-2 text-sm text-gray-500">
                Type: {{ membershipToDelete?.type }}<br>
                Remaining Visits: {{ membershipToDelete?.remaining_visits }}
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { createDocumentResource, Card, Badge, Avatar, Button, Input, Select, createResource, createListResource, Dialog } from 'frappe-ui';
import EditMemberDialog from '@/components/EditMemberDialog.vue';
import { useRoute } from 'vue-router';
import { computed, ref, watch } from 'vue';

const isEditing = ref(false);
const editableMemberships = ref([]);
const showDeleteDialog = ref(false);

const membershipTypes = [
    { label: '10 visits', value: '10 visits' },
    { label: '30 visits', value: '30 visits' },
];

const route = useRoute();

const clubMemberResource = createDocumentResource({
    doctype: 'Club Member',
    name: route.params.id_club_member,
    fields: ['*'],
    auto: true,
})

const membershipsList = computed(() => {
    if (clubMemberResource.doc?.memberships) {
        return clubMemberResource.doc.memberships;
    }
    return [];
});

const clubMemberDoc = computed(() => {
    if (clubMemberResource.doc) {
        return clubMemberResource.doc;
    }
    return {};
});

watch(() => membershipsList.value, (newMemberships) => {
    editableMemberships.value = JSON.parse(JSON.stringify(newMemberships || []));
}, { immediate: true });

function formatDate(date) {
    return new Date(date).toLocaleDateString();
}

function saveMembershipChanges() {
    editMembership.submit().then(() => {
        isEditing.value = false;
        clubMemberResource.reload();
    });
}

const editClubMember = createResource({
    url: 'club360.api.add_new_membership',
    makeParams: (values) => ({
        memberships_and_club_member: {
            memberships: editableMemberships.value,
            club_member: clubMemberDoc.value.name
        }
    })
});

function handleAddMembership() {
    let new_membership = {
        type: '10 visits',
        start_date: new Date().toISOString().split('T')[0],
        end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        remaining_visits: 10
    };
    editableMemberships.value.push(new_membership);
    editClubMember.submit();
}

function cancelEdit() {
    isEditing.value = false;
    editableMemberships.value = JSON.parse(JSON.stringify(membershipsList.value));
}

const editMemberDialog = ref(null);

function handleEditMember() {
    editMemberDialog.value?.openDialog(clubMemberDoc.value);
}

const editMembership = createResource({
    url: 'club360.api.edit_membership',
    makeParams: (values) => ({
        request_membership: {
            memberships: editableMemberships.value,
            club_member: clubMemberDoc.value.name
        }
    })
});

const deleteClubMemberMembership = createResource({
    url: 'club360.api.delete_club_member_membership',
    makeParams: (values) => ({
        memberships_and_club_member: {
            memberships: editableMemberships.value,
            club_member: clubMemberDoc.value
        }
    })
});

const showMembershipDeleteDialog = ref(false);
const membershipToDelete = ref(null);

function deleteMembership(index) {
    membershipToDelete.value = editableMemberships.value[index];
    showMembershipDeleteDialog.value = true;
}

function confirmMembershipDelete() {
    if (!membershipToDelete.value) return;
    
    const index = editableMemberships.value.findIndex(m => m === membershipToDelete.value);
    if (index !== -1) {
        editableMemberships.value.splice(index, 1);
        deleteClubMemberMembership.submit().then(() => {
            showMembershipDeleteDialog.value = false;
            membershipToDelete.value = null;
        });
    }
}

const referralsResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name', 'status'],
    filters: {
        referral_of: route.params.id_club_member
    },
    auto: true,
    transform(data) {
        return data.filter(member => member.referral_of === route.params.full_name);
    }
});

const referralsList = computed(() => {
    return referralsResource.list.data || [];
});

// Watch for changes in the club member's name and reload referrals
watch(() => route.params.full_name, (newName) => {
    if (newName) {
        referralsResource.reload();
    }
}, { immediate: true });

// Add coach resource for name resolution
const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['id_herbalife', 'full_name'],
    auto: true
});

const coachName = computed(() => {
    if (!clubMemberDoc.value?.coach || !coachesResource.list.data) return 'No Coach';
    const coach = coachesResource.list.data.find(c => c.id_herbalife === clubMemberDoc.value.coach);
    return coach?.full_name || 'No Coach';
});

// Add member resource for referral name resolution
const membersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    auto: true
});

// Add computed for referral name
const referralName = computed(() => {
    if (!clubMemberDoc.value?.referral_of || !membersResource.list.data) return 'No Referral';
    const referral = membersResource.list.data.find(m => m.name === clubMemberDoc.value.referral_of);
    return referral?.full_name || 'No Referral';
});
</script>