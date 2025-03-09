<template>
    <Dialog
        :options="{
            title: 'Add New Visit',
            size: 'md',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showDialog = false
                },
                {
                    label: 'Add Visit',
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
                <FormControl
                    type="autocomplete"
                    label="Club Member"
                    v-model="formData.club_member"
                    :options="memberOptions"
                    placeholder="Select member"
                    required
                    :error="errors.club_member"
                />

                <FormControl
                    type="date"
                    label="Date"
                    v-model="formData.date"
                    :default="today"
                    required
                    :error="errors.date"
                />

                <FormControl
                    type="select"
                    label="Type"
                    v-model="formData.type_event"
                    :options="typeOptions"
                    required
                    :error="errors.type_event"
                />

                <!-- Update error message display -->
                <div v-if="addVisitResource.error || errorMessage" class="mt-2">
                    <p class="text-red-600 text-sm">{{ errorMessage || addVisitResource.error?.message }}</p>
                </div>
            </div>
        </template>
    </Dialog>

    <!-- Add error alert -->
    <Alert
        v-if="showError"
        variant="error"
        :message="errorMessage"
        @close="showError = false"
        class="mb-4"
    />
</template>

<script setup>
import { ref, defineExpose, computed, defineEmits } from 'vue';
import { Dialog, FormControl, createListResource, createResource, Alert } from 'frappe-ui';
import { session } from '@/data/session';

const emit = defineEmits(['visitAdded']);

const showDialog = ref(false);
const formData = ref({
    club_member: '',
    date: new Date().toISOString().split('T')[0],
    type_event: 'Breakfast'  // Set default value to Breakfast
});

const today = new Date().toISOString().split('T')[0];

const typeOptions = [
    { label: 'Sport', value: 'Sport' },
    { label: 'Breakfast', value: 'Breakfast' }
];

// Updated members resource to include all records
const membersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    filters: {
        owner: session.user,
        status: 'Active' // Only show active members
    },
    pageLength: 9999, // Increase page length to get all records
    auto: true,
    limit: 0 // No limit on the number of records
});

// Add loading state for better UX
const isLoadingMembers = computed(() => membersResource.loading);

// Update member options to show loading state and use all records
const memberOptions = computed(() => {
    if (isLoadingMembers.value) return [{ label: 'Loading members...', value: '' }];
    if (!membersResource.list.data || membersResource.list.data.length === 0) return [];
    
    return membersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.name
    }));
});

const showError = ref(false);
const errorMessage = ref('');

const addVisitResource = createResource({
    url: 'club360.api.add_visit',
    makeParams: () => ({
        visit_data: formData.value
    }),
    onSuccess: (response) => {
        if (typeof response === 'string' && response.includes('Error')) {
            errorMessage.value = response;
        } else {
            showDialog.value = false;
            resetForm();
            errorMessage.value = '';
            emit('visitAdded');
        }
    },
    onError: (error) => {
        // Check for the specific error message
        if (error.message && error.message.includes("There is no servings for")) {
            errorMessage.value = `Cannot add visit: ${error.message}`;
        } else {
            errorMessage.value = error.message || 'Error adding visit';
        }
        showError.value = true;
    }
});

const errors = ref({
    club_member: '',
    date: '',
    type_event: ''
});

const isFormValid = computed(() => {
    return formData.value.club_member && formData.value.date && formData.value.type_event;
});

function submitForm() {
    // Reset errors
    errors.value = {
        club_member: '',
        date: '',
        type_event: ''
    };

    // Validate fields
    let isValid = true;
    if (!formData.value.club_member) {
        errors.value.club_member = 'Member is required';
        isValid = false;
    }
    if (!formData.value.date) {
        errors.value.date = 'Date is required';
        isValid = false;
    }
    if (!formData.value.type_event) {
        errors.value.type_event = 'Type is required';
        isValid = false;
    }

    if (!isValid) return;

    // Proceed with form submission
    addVisitResource.submit();
}

function resetForm() {
    formData.value = {
        club_member: '',
        date: new Date().toISOString().split('T')[0],
        type_event: 'Breakfast'
    };
    errorMessage.value = '';
}

function openDialog() {
    showDialog.value = true;
}

defineExpose({ openDialog });
</script>