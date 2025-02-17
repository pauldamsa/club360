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
                    <Input 
                        label="First Name" 
                        v-model="formData.first_name" 
                        required 
                    />
                    <Input 
                        label="Last Name" 
                        v-model="formData.last_name" 
                        required 
                    />
                </div>
                <Select 
                    label="Coach" 
                    v-model="formData.coach" 
                    :options="coachOptions" 
                    placeholder="Select a coach" 
                    required 
                />
                <Select 
                    label="Source" 
                    v-model="formData.source" 
                    :options="sourceOptions" 
                    placeholder="Select the source" 
                    required 
                />
                <Input 
                    label="Referrals" 
                    v-model="formData.referrals" 
                    type="number" 
                />
                <Select 
                    label="Status" 
                    v-model="formData.status" 
                    :options="statusOptions" 
                    required 
                />
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed, watch } from 'vue';
import { Dialog, Input, Select, createListResource } from 'frappe-ui';

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
    status: ''
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
    { label: 'Walk-in', value: 'Walk-in' }
];

const statusOptions = [
    { label: 'Active', value: 'Active' },
    { label: 'Inactive', value: 'Inactive' }
];

function submitForm() {
    console.log('Saving changes:', formData.value);
    showDialog.value = false;
}

function openDialog(data) {
    formData.value = { ...data };
    showDialog.value = true;
}

// Expose the openDialog method
defineExpose({ openDialog });
</script>