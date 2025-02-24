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
                    onClick: submitForm
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
                />

                <FormControl
                    type="date"
                    label="Date"
                    v-model="formData.date"
                    :default="today"
                    required
                />

                <FormControl
                    type="select"
                    label="Type"
                    v-model="formData.type_event"
                    :options="typeOptions"
                    required
                />
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, defineExpose, computed, defineEmits } from 'vue';
import { Dialog, FormControl, createListResource, createResource } from 'frappe-ui';

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

// Get club members for autocomplete with name field
const membersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    auto: true
});

// Update member options to use name as value
const memberOptions = computed(() => {
    if (!membersResource.list.data) return [];
    return membersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.name  // Use name as value
    }));
});

const addVisitResource = createResource({
    url: 'club360.api.add_visit',
    makeParams: () => ({
        visit_data: formData.value
    }),
    onSuccess: () => {
        showDialog.value = false;
        resetForm();
        emit('visitAdded');
    },
    onError: (error) => {
        console.error('Error adding visit:', error);
        // You might want to show an error message to the user here
    }
});

function submitForm() {
    addVisitResource.submit();
}

function resetForm() {
    formData.value = {
        club_member: '',
        date: new Date().toISOString().split('T')[0],
        type_event: 'Breakfast'
    };
}

function openDialog() {
    showDialog.value = true;
}

defineExpose({ openDialog });
</script>