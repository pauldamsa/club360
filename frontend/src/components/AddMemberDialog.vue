<template>
    <Dialog
        :options="{
            title: 'Add new Club Member',
            size: 'lg',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showDialog = false
                },
                {
                    label: 'Add Member',
                    variant: 'solid',
                    onClick: submitForm
                }
            ]
        }"
        v-model="showDialog"
    >
        <template #body-content>
            <div class="space-y-4 p-4">
                <div class="grid grid-cols-2 gap-4">
                    <div class="p-2">
                        <FormControl
                            :type="'text'"
                            :ref_for="true"
                            size="sm"
                            variant="subtle"
                            placeholder="John"
                            :disabled="false"
                            label="First Name"
                            v-model="formData.first_name"
                        />
                    </div>
                    <div class="p-2">
                        <FormControl
                            :type="'text'"
                            :ref_for="true"
                            size="sm"
                            variant="subtle"
                            placeholder="Doe"
                            :disabled="false"
                            label="Last Name"
                            v-model="formData.last_name"
                        />
                    </div>
                </div>
                <div class="p-2">
                    <FormControl
                        type="autocomplete"
                        :options="coachOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select a coach"
                        :disabled="false"
                        label="Coach"
                        v-model="formData.coach"
                    />
                </div>
                <div class="p-2">
                <FormControl
                    type="select"
                    :options="sourceOptions"
                    size="sm"
                    variant="subtle"
                    placeholder="Select the source of the member" 
                    :disabled="false"
                    label="Source"
                    v-model="formData.source"
                />
                </div>
                <div class="p-2">
                    <FormControl
                        :type="'number'"
                        :ref_for="true"
                        size="sm"
                        variant="subtle"
                        placeholder="Number of referrals"
                        :disabled="false"
                        label="Refferals"
                        v-model="formData.referrals"
                    />
                </div>
                <div class="p-2" v-if="formData.source === 'Referral'">
                    <FormControl
                        type="autocomplete"
                        :options="memberOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select the member"
                        :disabled="false"
                        label="Referral of"
                        v-model="formData.referral_of"
                    />
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed, defineEmits } from 'vue';
import { Dialog, createListResource, FormControl, createResource } from 'frappe-ui';

const showDialog = ref(false);
const formData = ref({
    first_name: '',
    last_name: '',
    coach: '',  // This will now store the id_herbalife
    source: '',
    referrals: 0,
    referral_of: ''
});

const coachResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'id_herbalife'],
    auto: true,
})

const coachList = computed(() => {
    if (coachResource.list.data) {
        return coachResource.list.data;
    }
    return [];
})

const coachOptions = computed(() => {
    if (!coachResource.list.data) return [];
    return coachResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.id_herbalife  // Changed to use id_herbalife as value
    }));
});

// Add helper computed to get coach name for display
const selectedCoachName = computed(() => {
    const coach = coachResource.list.data?.find(c => c.id_herbalife === formData.value.coach);
    return coach?.full_name || '';
});

const sourceOptions = [
    { label: 'Facebook', value: 'Facebook' },
    { label: 'Instagram', value: 'Instagram' },
    { label: 'Referral', value: 'Referral' },
    { label: 'Active Contact', value: 'Active Contact' },
    { label: 'Roadshow', value: 'Roadshow' },
];

// Update club members resource to include name field
const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'], // Added name field for ID
    auto: true,
});

// Update member options to use name as value
const memberOptions = computed(() => {
    if (!clubMembersResource.list.data) return [];
    return clubMembersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.name  // Using name (ID) as value
    }));
});

const emit = defineEmits(['memberAdded']);

const addNewClubMember = createResource({
    url: 'club360.api.add_new_club_member',
    makeParams() {
        const formattedData = {
            first_name: formData.value.first_name,
            last_name: formData.value.last_name,
            coach: formData.value.coach,
            source: formData.value.source,
            referrals: formData.value.referrals || 0,
            referral_of: formData.value.source === 'Referral' ?  formData.value.referral_of  : ''
        };
        return {
            club_member: formattedData
        };
    },
    onSuccess: () => {
        showDialog.value = false;
        formData.value = {
            first_name: '',
            last_name: '',
            coach: '',
            source: '',
            referrals: 0,
            referral_of: ''
        };
        emit('memberAdded'); // Emit event when member is added successfully
    },
    onError: (error) => {
        console.error('Error adding member:', error);
    }
});

function submitForm() {
    // Handle form submission
    // console.log('Form submitted:', formData.value);
    addNewClubMember.submit()
    showDialog.value = false;
}

function openDialog() {
    showDialog.value = true;
}

// Important: Expose the openDialog method
defineExpose({ openDialog });
</script>