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
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed } from 'vue';
import { Dialog, Input, Select, createListResource, FormControl } from 'frappe-ui';

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