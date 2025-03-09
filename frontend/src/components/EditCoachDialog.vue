<template>
    <Dialog
        :options="{
            title: 'Edit Coach',
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
                    onClick: submitForm
                }
            ]
        }"
        v-model="showDialog"
    >
        <template #body-content>
            <div class="space-y-4 p-4">
                <!-- Basic Info -->
                <div class="grid grid-cols-2 gap-4">
                    <FormControl
                        type="text"
                        label="First Name"
                        v-model="formData.first_name"
                        placeholder="John"
                    />
                    <FormControl
                        type="text"
                        label="Last Name"
                        v-model="formData.last_name"
                        placeholder="Doe"
                    />
                </div>

                <!-- Role and Level -->
                <div class="grid grid-cols-2 gap-4">
                    <FormControl
                        type="select"
                        label="Role"
                        v-model="formData.role"
                        :options="roleOptions"
                    />
                    <FormControl
                        type="select"
                        label="Level"
                        v-model="formData.level"
                        :options="levelOptions"
                    />
                </div>

                <!-- Contact Information -->
                <div class="grid grid-cols-2 gap-4">
                    <FormControl
                        type="text"
                        label="Phone Number"
                        v-model="formData.phone_number"
                        placeholder="+40 123 456 789"
                    />
                    <FormControl
                        type="email"
                        label="Email"
                        v-model="formData.email"
                        placeholder="coach@example.com"
                    />
                </div>

                <FormControl
                    type="text"
                    label="Herbalife ID"
                    v-model="formData.id_herbalife"
                    placeholder="123456789"
                />

                <!-- Sponsor -->
                <FormControl
                    type="autocomplete"
                    label="Sponsor"
                    v-model="formData.sponsor"
                    :options="sponsorOptions"
                    placeholder="Select a sponsor"
                />
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed, watch } from 'vue';
import { Dialog, FormControl, createListResource, createResource } from 'frappe-ui';
import { session } from '@/data/session';

const showDialog = ref(false);
const formData = ref({
    first_name: '',
    last_name: '',
    role: '',
    level: '',
    sponsor: '',
    phone_number: '',
    email: '',
    id_herbalife: ''
});

const roleOptions = [
    { label: 'Junior Partner', value: 'Junior Partner' },
    { label: 'Trainee', value: 'Trainee' },
    { label: 'Club Owner', value: 'Club Owner' }
];

const levelOptions = [
    { label: 'CS', value: 'CS' },
    { label: 'QP', value: 'QP' },
    { label: 'SV', value: 'SV' },
    { label: 'WT', value: 'WT' },
    { label: 'AWT', value: 'AWT' },
    { label: 'GET', value: 'GET' },
    { label: 'GET 2500', value: 'GET 2500' },
    { label: 'MT', value: 'MT' },
    { label: 'MT 7500', value: 'MT 7500' },
    { label: 'PT', value: 'PT' }
];

const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'id_herbalife'],  // Added id_herbalife
    filters: {
        owner: session.user
    },
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
    auto: true
});

const sponsorOptions = computed(() => {
    if (!coachesResource.list.data) return [];
    return coachesResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.id_herbalife  // Changed to use id_herbalife as value
    }));
});

const editCoachResource = createResource({
    url: 'club360.api.edit_coach',
    makeParams() {
        return {
            coach: formData.value
        };
    }
});

function submitForm() {
    editCoachResource.submit().then(() => {
        showDialog.value = false;
    });
}

function openDialog(coachData) {
    formData.value = { ...coachData };
    showDialog.value = true;
}

defineExpose({ openDialog });
</script>