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
import { ref, defineExpose, computed } from 'vue';
import { Dialog, FormControl, createListResource } from 'frappe-ui';

const showDialog = ref(false);
const formData = ref({
    club_member: '',
    date: new Date().toISOString().split('T')[0],
    type_event: ''
});

const today = new Date().toISOString().split('T')[0];

const typeOptions = [
    { label: 'Sport', value: 'Sport' },
    { label: 'Breakfast', value: 'Breakfast' }
];

// Get club members for autocomplete
const membersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    auto: true
});

const memberOptions = computed(() => {
    if (!membersResource.list.data) return [];
    return membersResource.list.data.map(member => ({
        label: member.full_name,
        value: member.full_name
    }));
});

function submitForm() {
    // TODO: Implement API call
    console.log('Form data:', formData.value);
    showDialog.value = false;
    formData.value = {
        club_member: '',
        date: new Date().toISOString().split('T')[0],
        type_event: ''
    };
}

function openDialog() {
    showDialog.value = true;
}

defineExpose({ openDialog });
</script>