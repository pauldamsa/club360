<template>
    <Dialog
        :options="{
            title: 'Add New Coach',
            size: 'lg',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showDialog = false
                },
                {
                    label: 'Add Coach',
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

                <!-- ID and Level -->
                <div class="grid grid-cols-2 gap-4">
                    <FormControl
                        type="text"
                        label="ID Herbalife"
                        v-model="formData.id_herbalife"
                        placeholder="123456789"
                    />
                    <FormControl
                        type="select"
                        label="Level"
                        v-model="formData.level"
                        :options="levelOptions"
                    />
                </div>

                <!-- Contact Info -->
                <div class="grid grid-cols-2 gap-4">
                    <FormControl
                        type="email"
                        label="Email"
                        v-model="formData.email"
                        placeholder="coach@example.com"
                    />
                    <FormControl
                        type="tel"
                        label="Phone Number"
                        v-model="formData.phone_number"
                        placeholder="+40 123 456 789"
                    />
                </div>

                <!-- Role and Sponsor -->
                <div class="grid grid-cols-2 gap-4">
                    <FormControl
                        type="select"
                        label="Role"
                        v-model="formData.role"
                        :options="roleOptions"
                    />
                    <FormControl
                        type="autocomplete"
                        label="Sponsor"
                        v-model="formData.sponsor"
                        :options="sponsorOptions"
                        placeholder="Select a sponsor"
                    />
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed } from 'vue';
import { Dialog, FormControl, createListResource } from 'frappe-ui';

const showDialog = ref(false);
const formData = ref({
    first_name: '',
    last_name: '',
    id_herbalife: '',
    level: '',
    email: '',
    role: '',
    sponsor: '',
    phone_number: ''
});

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

const roleOptions = [
    { label: 'Trainee', value: 'Trainee' },
    { label: 'Junior Partner', value: 'Junior Partner' },
    { label: 'Club Owner', value: 'Club Owner' }
];

const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name'],
    auto: true
});

const sponsorOptions = computed(() => {
    if (!coachesResource.list.data) return [];
    return coachesResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.full_name
    }));
});

function submitForm() {
    console.log('Form data:', formData.value);
    showDialog.value = false;
    formData.value = {
        first_name: '',
        last_name: '',
        id_herbalife: '',
        level: '',
        email: '',
        role: '',
        sponsor: '',
        phone_number: ''
    };
}

function openDialog() {
    showDialog.value = true;
}

defineExpose({ openDialog });
</script>