<template>
    <Dialog
        :options="{
            title: 'Edit Club Member',
            size: 'lg',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showDialog = false
                },
                {
                    label: 'Save Changes',
                    variant: 'solid',
                    onClick: submitForm,
                    disabled: !isFormValid
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
                            type="text"
                            size="sm"
                            variant="subtle"
                            placeholder="John"
                            label="First Name"
                            v-model="formData.first_name"
                            required
                            :error="errors.first_name"
                        />
                    </div>
                    <div class="p-2">
                        <FormControl
                            type="text"
                            size="sm"
                            variant="subtle"
                            placeholder="Doe"
                            label="Last Name"
                            v-model="formData.last_name"
                            required
                            :error="errors.last_name"
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
                        label="Coach"
                        v-model="formData.coach"
                        required
                        :error="errors.coach"
                    />
                </div>
                <div class="p-2">
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
                <div class="p-2">
                    <FormControl
                        type="select"
                        :options="statusOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select the status of the member" 
                        :disabled="false"
                        label="Status"
                        v-model="formData.status"
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
                <div class="p-2">
                    <FormControl
                        type="select"
                        :options="typeOptions"
                        size="sm"
                        variant="subtle"
                        placeholder="Select member type"
                        label="Type"
                        v-model="formData.type"
                    />
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed, watch } from 'vue';
import { Dialog, createListResource, FormControl, createResource } from 'frappe-ui';

const props = defineProps({
    memberData: {
        type: Object,
        default: () => ({})
    }
});

const showDialog = ref(false);
const formData = ref({
    first_name: '',
    last_name: '',
    coach: '',
    source: '',
    referrals: 0,
    status: '',
    referral_of: '',
    type: 'Club Member', // Add default value
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

// Watch for memberData changes and update formData
watch(() => props.memberData, (newData) => {
    if (newData) {
        // If coach is already an id_herbalife, use it directly
        // If it's an object with value property, use that
        const coachId = typeof newData.coach === 'object' ? newData.coach.value : newData.coach;
        formData.value = {
            ...newData,
            coach: coachId
        };
    }
}, { deep: true });

const coachResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'id_herbalife'],  // Added id_herbalife field
    auto: true,
});

const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],  // Added name field
    auto: true,
});

// Add referral name mapping
const referralNameMap = computed(() => {
    const mapping = {};
    if (clubMembersResource.list.data) {
        clubMembersResource.list.data.forEach(member => {
            mapping[member.name] = member.full_name;
        });
    }
    return mapping;
});

// Update member options to show full_name while using name as value
const memberOptions = computed(() => {
    if (!clubMembersResource.list.data) return [];
    return clubMembersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.name  // Using name as value
    }));
});

// Add helper computed to get referral name for display
const selectedReferralName = computed(() => {
    if (!formData.value.referral_of) return '';
    return referralNameMap.value[formData.value.referral_of] || '';
});

// Watch to handle member data properly
watch(() => props.memberData, (newData) => {
    if (newData) {
        // If referral_of is an object, use its value, otherwise use directly
        const referralId = typeof newData.referral_of === 'object' ? 
            newData.referral_of.value : newData.referral_of;
        
        formData.value = {
            ...newData,
            referral_of: referralId
        };
    }
}, { deep: true });

// Add computed property for coach options
const coachOptions = computed(() => {
    if (!coachResource.list.data) return [];
    return coachResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.id_herbalife  // Changed to use id_herbalife as value
    }));
});

// Add helper computed to get coach name for display
const selectedCoachName = computed(() => {
    if (!formData.value.coach || !coachResource.list.data) return '';
    const coach = coachResource.list.data.find(c => c.id_herbalife === formData.value.coach);
    return coach?.full_name || '';
});

const sourceOptions = [
    { label: 'Facebook', value: 'Facebook' },
    { label: 'Instagram', value: 'Instagram' },
    { label: 'Referral', value: 'Referral' },
    { label: 'Active Contact', value: 'Active Contact' },
    { label: 'Roadshow', value: 'Roadshow' }
];

const statusOptions = [
    { label: 'Active', value: 'Active' },
    { label: 'Inactive', value: 'Inactive' }
];

// Add type options
const typeOptions = [
    { label: 'Club Member', value: 'Club Member' },
    { label: 'Trainee', value: 'Trainee' }
];

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
    editClubMember.submit();
    showDialog.value = false;
}

const editClubMember = createResource({
    url: 'club360.api.edit_club_member',
    makeParams(){
        return {
            new_club_member: formData.value
        }
    }
})

function openDialog(data) {
    formData.value = { ...data };
    showDialog.value = true;
}

// Expose the openDialog method
defineExpose({ openDialog });
</script>