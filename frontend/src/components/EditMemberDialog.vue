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
                    loading: false
                }
            ]
        }"
        v-model="showDialog"
    >
        <template #body-content>
            <div class="space-y-4 p-4">
                <div class="grid grid-cols-2 gap-4">
                    <!-- <Input 
                        label="First Name" 
                        v-model="formData.first_name" 
                        required 
                    /> -->
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
                            placeholder="John"
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
    referral_of: ''
});

// Watch for memberData changes and update formData
watch(() => props.memberData, (newData) => {
    if (newData) {
        formData.value = { ...newData };
    }
}, { deep: true });

const coachResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name'],
    auto: true,
});

const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['full_name'],
    auto: true,
});

// Add computed property for member options
const memberOptions = computed(() => {
    if (!clubMembersResource.list.data) return [];
    return clubMembersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.full_name
    }));
});

const coachOptions = computed(() => {
    if (!coachResource.list.data) return [];
    return coachResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.full_name
    }));
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

function submitForm() {
    // console.log('Saving changes:', formData.value);
    editClubMember.submit()
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