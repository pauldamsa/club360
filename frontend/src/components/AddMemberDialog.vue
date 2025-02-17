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
                    <Input label="First Name" v-model="formData.first_name" required />
                    <Input label="Last Name" v-model="formData.last_name" required />
                </div>
                <Select label="Coach" v-model="formData.coach" :options="coachOptions" placeholder="Select a coach" required />
                <Select label="Source" v-model="formData.source" :options="sourceOptions" placeholder="Select the source" required />
                <Input label="Referrals" v-model="formData.referrals" type="number" />
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed } from 'vue';
import { Dialog, Input, Select, createListResource } from 'frappe-ui';

const showDialog = ref(false);
const formData = ref({
    first_name: '',
    last_name: '',
    coach: '',
    source: '',
    referrals: 0
});

const coachResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name'],
    auto: true,
})

const coachList = computed(() => {
    if (coachResource.list.data) {
        return coachResource.list.data;
    }
    return [];
})

const coachOptions = computed(() => {
    return coachList.value.map(coach => ({
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

function submitForm() {
    // Handle form submission
    console.log('Form submitted:', formData.value);
    showDialog.value = false;
}

function openDialog() {
    showDialog.value = true;
}

// Important: Expose the openDialog method
defineExpose({ openDialog });
</script>