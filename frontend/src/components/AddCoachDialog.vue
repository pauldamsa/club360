<template>
    <Dialog
        :options="{
            title: 'Add New Coach',
            size: 'lg',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showDialog = false,
                    class: 'w-full sm:w-auto'
                },
                {
                    label: 'Add Coach',
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
            <div class="space-y-4 p-3 md:p-4">
                <!-- Basic Info -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    <FormControl
                        type="text"
                        label="First Name"
                        v-model="formData.first_name"
                        placeholder="John"
                        required
                        :error="errors.first_name"
                        class="w-full"
                    />
                    <FormControl
                        type="text"
                        label="Last Name"
                        v-model="formData.last_name"
                        placeholder="Doe"
                        required
                        :error="errors.last_name"
                        class="w-full"
                    />
                </div>

                <!-- ID and Level -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    <FormControl
                        type="text"
                        label="ID Herbalife"
                        v-model="formData.id_herbalife"
                        placeholder="123456789"
                        required
                        :error="errors.id_herbalife"
                        class="w-full"
                    />
                    <FormControl
                        type="select"
                        label="Level"
                        v-model="formData.level"
                        :options="levelOptions"
                        required
                        :error="errors.level"
                        class="w-full"
                    />
                </div>

                <!-- Contact Info -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    <FormControl
                        type="email"
                        label="Email"
                        v-model="formData.email"
                        placeholder="coach@gmail.com"
                        required
                        :error="errors.email"
                        class="w-full"
                    />
                    <FormControl
                        type="tel"
                        label="Phone Number"
                        v-model="formData.phone_number"
                        placeholder="0763 456 789"
                        required
                        :error="errors.phone_number"
                        class="w-full"
                    />
                </div>

                <!-- Role and Sponsor -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    <FormControl
                        type="select"
                        label="Role"
                        v-model="formData.role"
                        :options="roleOptions"
                        required
                        :error="errors.role"
                        class="w-full"
                    />
                    <FormControl
                        type="autocomplete"
                        label="Sponsor"
                        v-model="formData.sponsor"
                        :options="sponsorOptions"
                        placeholder="Select a sponsor"
                        class="w-full"
                    />
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed } from 'vue';
import { Dialog, FormControl, createListResource, createResource } from 'frappe-ui';
import { session } from '@/data/session';

const emit = defineEmits(['coachAdded']);

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

const errors = ref({
    first_name: '',
    last_name: '',
    id_herbalife: '',
    level: '',
    email: '',
    role: '',
    phone_number: ''
});

const isFormValid = computed(() => {
    return formData.value.first_name && 
           formData.value.last_name && 
           formData.value.id_herbalife && 
           formData.value.level &&
           formData.value.email &&
           formData.value.role &&
           formData.value.phone_number;
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
    fields: ['full_name', 'id_herbalife'],
    filters :{
        owner: session.user
    },
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
    auto: true
});

const addNewCoach = createResource({
    url: 'club360.api.add_new_coach',
    makeParams(){
        return {
            coach: formData.value
        }
    },
    onSuccess: () => {
        showDialog.value = false;
        resetForm();
        emit('coachAdded'); // Emit event when coach is added successfully
    },
    onError: (error) => {
        console.error('Error adding coach:', error);
    }
});

const sponsorOptions = computed(() => {
    if (!coachesResource.list.data) return [];
    return coachesResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.id_herbalife
    }));
});

function submitForm() {
    // Reset errors
    errors.value = {
        first_name: '',
        last_name: '',
        id_herbalife: '',
        level: '',
        email: '',
        role: '',
        phone_number: ''
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
    if (!formData.value.id_herbalife) {
        errors.value.id_herbalife = 'ID Herbalife is required';
        isValid = false;
    }
    if (!formData.value.level) {
        errors.value.level = 'Level is required';
        isValid = false;
    }
    if (!formData.value.email) {
        errors.value.email = 'Email is required';
        isValid = false;
    }
    if (!formData.value.role) {
        errors.value.role = 'Role is required';
        isValid = false;
    }
    if (!formData.value.phone_number) {
        errors.value.phone_number = 'Phone number is required';
        isValid = false;
    }

    if (!isValid) return;

    // Proceed with form submission
    addNewCoach.submit();
}

function resetForm() {
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