<template>
    <Dialog
        :options="{
            title: 'Add new Club Member',
            size: 'lg',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showDialog = false,
                    class: 'w-full sm:w-auto'
                },
                {
                    label: 'Add Member',
                    variant: 'solid',
                    onClick: submitForm,
                    disabled: !isFormValid,
                    class: 'w-full sm:w-auto'
                }
            ]
        }"
        v-model="showDialog"
    >
        <template #body-content>
            <div class="space-y-4 p-2 md:p-4">
                <!-- Basic Info -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    <FormControl
                        type="text"
                        size="sm"
                        variant="subtle"
                        placeholder="John"
                        label="First Name"
                        v-model="formData.first_name"
                        required
                        :error="errors.first_name"
                        class="w-full"
                    />
                    <FormControl
                        type="text"
                        size="sm"
                        variant="subtle"
                        placeholder="Doe"
                        label="Last Name"
                        v-model="formData.last_name"
                        required
                        :error="errors.last_name"
                        class="w-full"
                    />
                </div>

                <!-- Coach and Source -->
                <div class="space-y-3">
                    <FormControl
                        type="autocomplete"
                        :options="coachOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select a coach"
                        label="Coach"
                        v-model="formData.coach"
                        required
                        :error="errors.coach"
                        class="w-full"
                    />
                    <FormControl
                        type="select"
                        :options="sourceOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select the source"
                        label="Source"
                        v-model="formData.source"
                        required
                        :error="errors.source"
                        class="w-full"
                    />
                </div>

                <!-- Additional Info -->
                <div class="space-y-3">
                    <FormControl
                        type="number"
                        size="sm"
                        variant="subtle"
                        placeholder="Number of referrals"
                        label="Referrals"
                        v-model="formData.referrals"
                        class="w-full"
                    />
                    <FormControl
                        v-if="formData.source === 'Referral'"
                        type="autocomplete"
                        :options="memberOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select the member"
                        label="Referral of"
                        v-model="formData.referral_of"
                        class="w-full"
                    />
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed, defineEmits } from 'vue';
import { Dialog, createListResource, FormControl, createResource } from 'frappe-ui';
import { session } from '@/data/session';

const showDialog = ref(false);
const formData = ref({
    first_name: '',
    last_name: '',
    coach: '',  // This will now store the id_herbalife
    source: '',
    referrals: 0,
    referral_of: ''
});

const errors = ref({
    first_name: '',
    last_name: '',
    coach: '',
    source: '',
});

const isFormValid = computed(() => {
    return formData.value.first_name && 
           formData.value.last_name && 
           formData.value.coach && 
           formData.value.source;
});

const coachResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'id_herbalife'],
    filters: {
        owner: session.user
    },
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
    filters: {
        owner: session.user
    },
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
    // Reset errors
    errors.value = {
        first_name: '',
        last_name: '',
        coach: '',
        source: '',
    };

    // Validate fields
    let isValid = true;
    if (!formData.value.first_name) {
        errors.value.first_name = 'First name is required';
        isValid = false;
    }
    if (!formData.value.last_name) {
        errors.value.last_name = 'Last name is required';
        isValid = false;
    }
    if (!formData.value.coach) {
        errors.value.coach = 'Coach is required';
        isValid = false;
    }
    if (!formData.value.source) {
        errors.value.source = 'Source is required';
        isValid = false;
    }

    if (!isValid) return;

    // Proceed with form submission
    addNewClubMember.submit();
}

function openDialog() {
    showDialog.value = true;
}

// Important: Expose the openDialog method
defineExpose({ openDialog });
</script>